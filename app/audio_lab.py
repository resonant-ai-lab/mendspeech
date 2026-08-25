"""MendSpeech audio lab: interactive clean-versus-damaged comparison console.

Run from the repository root with:
    python app/audio_lab.py
"""

from __future__ import annotations

import sys
from functools import lru_cache
from pathlib import Path
from typing import Dict, List, Tuple

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import gradio as gr
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import torch
import torchaudio

from speechdamagebench.audio_damage import CORRUPTIONS, DamageConfig, apply_damage
from src.audio.loader import load_audio
from src.metrics.audio_metrics import compute_pair_metrics

matplotlib.use("Agg")

BENCHMARK_DIR = REPO_ROOT / "data" / "benchmark"
MANIFEST_PATH = BENCHMARK_DIR / "manifest.csv"

DEFAULT_SEED = 42
SAMPLE_RATE = 16000
SEVERITIES = ("mild", "medium", "severe")
LAUNCH_THEME = gr.themes.Soft(
    primary_hue="blue",
    neutral_hue="slate",
    font=[gr.themes.GoogleFont("Inter"), "ui-sans-serif", "system-ui", "sans-serif"],
)
LAUNCH_CSS = """
.prose h1 { font-size: 1.55rem; letter-spacing: 0; margin-bottom: 0; }
.prose p { margin-top: 0.25rem; opacity: 0.68; }
audio { width: 100%; }
.metrics table { font-size: 0.88rem; }
.source-note code { font-size: 0.78rem; }
.comparison-row {
    display: grid !important;
    gap: 1rem;
    grid-template-columns: repeat(2, minmax(0, 1fr));
}
.comparison-row > * { min-width: 0 !important; }
@media (max-width: 720px) {
    .comparison-row { grid-template-columns: 1fr; }
}
"""


@lru_cache(maxsize=1)
def load_manifest() -> pd.DataFrame:
    """Load the local benchmark manifest.

    Returns:
        DataFrame with one row per benchmark utterance.
    """
    return pd.read_csv(MANIFEST_PATH)


@lru_cache(maxsize=128)
def load_clip(file_path: str) -> Tuple[torch.Tensor, int]:
    """Load and cache a standardized mono waveform.

    Args:
        file_path: Absolute or repository-relative WAV path.

    Returns:
        ``(waveform [1, time], sample_rate Hz)``.
    """
    return load_audio(file_path, target_sr=SAMPLE_RATE, mono=True)


def clip_options() -> Dict[str, str]:
    """Map display labels to manifest file paths.

    Returns:
        Ordered dictionary where keys are ``clip_id (speaker_id)``.
    """
    manifest = load_manifest()
    return {
        f"{row.clip_id} ({row.speaker_id})": row.file_path
        for row in manifest.itertuples()
    }


def plot_waveform(
    waveform: np.ndarray,
    sample_rate: int,
    title: str,
    color: str,
) -> plt.Figure:
    """Plot amplitude against time in seconds."""
    time = np.arange(waveform.shape[0], dtype=np.float64) / sample_rate
    fig, ax = plt.subplots(figsize=(7.2, 2.1), constrained_layout=True)
    ax.plot(time, waveform, linewidth=0.45, color=color)
    ax.set_xlim(0, max(float(time[-1]), 0.01))
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Amplitude")
    ax.set_title(title, fontsize=11, loc="left", pad=8)
    ax.grid(axis="x", alpha=0.14, linewidth=0.6)
    ax.spines[["top", "right"]].set_visible(False)
    return fig


def plot_spectrogram(waveform: np.ndarray, sample_rate: int, title: str) -> plt.Figure:
    """Plot an 80-band log-Mel spectrogram on a shared time axis."""
    mel_transform = torchaudio.transforms.MelSpectrogram(
        sample_rate=sample_rate,
        n_fft=1024,
        hop_length=256,
        n_mels=80,
        f_min=0.0,
        f_max=sample_rate // 2,
        power=2.0,
    )
    tensor = torch.from_numpy(np.ascontiguousarray(waveform)).unsqueeze(0)
    mel = mel_transform(tensor)
    log_mel = torchaudio.transforms.AmplitudeToDB(stype="power", top_db=80)(mel)
    image = log_mel.squeeze(0).numpy()
    duration = image.shape[1] * 256 / sample_rate

    fig, ax = plt.subplots(figsize=(7.2, 2.8), constrained_layout=True)
    ax.imshow(
        image[::-1],
        aspect="auto",
        origin="lower",
        cmap="magma",
        extent=(0, duration, 0, sample_rate // 2),
    )
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Frequency (Hz)")
    ax.set_title(title, fontsize=11, loc="left", pad=8)
    return fig


def next_seed(seed: float) -> int:
    """Advance the seed while preserving the operator's determinism contract.

    Args:
        seed: Current seed shown by the UI.

    Returns:
        Next integer seed.
    """
    return int(seed) + 1


def render_lab(
    selected_label: str,
    corruption: str,
    severity: str,
    seed: float,
) -> Tuple:
    """Generate playback, plots, and metrics for one damage realization.

    Args:
        selected_label: Utterance key from :func:`clip_options`.
        corruption: SpeechDamageBench operator name.
        severity: Preset name.
        seed: Integer-valued random seed.

    Returns:
        Component values in the order defined by ``build_demo``.
    """
    options = clip_options()
    if selected_label not in options:
        raise ValueError(f"unknown utterance: {selected_label}")

    file_path = REPO_ROOT / options[selected_label]
    clean_tensor, sample_rate = load_clip(str(file_path))
    clean_wave = clean_tensor.squeeze(0).cpu().numpy().astype(np.float32)
    clip_id = Path(file_path).stem
    integer_seed = int(seed)

    config = DamageConfig(
        corruption=corruption,
        severity=severity,
        seed=integer_seed,
        source_id=clip_id,
    )
    damaged_wave, record = apply_damage(clean_wave.copy(), sample_rate, config)

    speaker_id = str(
        load_manifest().loc[load_manifest()["clip_id"] == clip_id, "speaker_id"].iloc[0]
    )
    metrics = compute_pair_metrics(
        clean=torch.from_numpy(clean_wave),
        corrupted=torch.from_numpy(damaged_wave),
        sample_rate=sample_rate,
        clip_id=clip_id,
        speaker_id=speaker_id,
        corruption=corruption,
        severity=severity,
        seed=integer_seed,
    )
    measurements: List[List[str]] = [
        ["SNR (dB)", f"{metrics.snr_db:.1f}", "Additive noise; misleading for other operators"],
        ["Log-Mel distance", f"{metrics.log_mel_distance:.3f}", "Spectral change; 0 is identical"],
        ["Clean RMS (dBFS)", f"{metrics.clean_rms_db:.1f}", "Source loudness"],
        ["Damaged RMS (dBFS)", f"{metrics.corrupted_rms_db:.1f}", "Output loudness"],
        ["Seed", str(integer_seed), "Realization selector"],
        ["Parameters", str(record.parameters), "Operator values applied"],
    ]

    return (
        (sample_rate, clean_tensor.squeeze(0).numpy()),
        plot_waveform(clean_wave, sample_rate, "Clean waveform", "#2563EB"),
        plot_spectrogram(clean_wave, sample_rate, "Clean spectrogram"),
        (sample_rate, damaged_wave),
        plot_waveform(damaged_wave, sample_rate, f"Damaged waveform - {corruption}", "#DC2626"),
        plot_spectrogram(damaged_wave, sample_rate, f"Damaged spectrogram - {corruption}"),
        measurements,
        (
            f"Speaker `{speaker_id}` | package v{record.package_version} | "
            f"source `{clip_id}` | {record.num_samples} samples @ {sample_rate} Hz"
        ),
    )


def build_demo() -> gr.Blocks:
    """Assemble the Gradio console.

    Returns:
        Configured Gradio Blocks application.
    """
    choices = list(clip_options())
    if not choices:
        raise RuntimeError(f"No benchmark clips found in {MANIFEST_PATH}")

    with gr.Blocks(
        title="MendSpeech Audio Lab",
        elem_id="audio-lab",
    ) as demo:
        gr.Markdown("# MendSpeech Audio Lab\nCompare controlled damage against its source utterance.")
        with gr.Row(equal_height=False):
            with gr.Column(scale=4, min_width=300):
                utterance = gr.Dropdown(choices=choices, value=choices[0], label="Utterance")
                corruption = gr.Radio(list(CORRUPTIONS), value=CORRUPTIONS[0], label="Corruption")
                severity = gr.Radio(SEVERITIES, value="medium", label="Severity")
                with gr.Row():
                    seed = gr.Number(value=DEFAULT_SEED, precision=0, minimum=0, step=1, label="Seed")
                    regenerate = gr.Button("New realization", variant="primary")
            with gr.Column(scale=8):
                with gr.Row(equal_height=True, elem_classes=["comparison-row"]):
                    with gr.Column():
                        clean_audio = gr.Audio(label="Clean", format="wav")
                        clean_waveform = gr.Plot(label="Waveform")
                        clean_spectrogram = gr.Plot(label="Spectrogram")
                    with gr.Column():
                        damaged_audio = gr.Audio(label="Damaged", format="wav")
                        damaged_waveform = gr.Plot(label="Waveform")
                        damaged_spectrogram = gr.Plot(label="Spectrogram")
                metrics = gr.Dataframe(
                    headers=["Metric", "Value", "Reading"],
                    datatype=["str", "str", "str"],
                    interactive=False,
                    wrap=True,
                    label="Measurements",
                    elem_classes=["metrics"],
                )
                source_note = gr.Markdown(elem_classes=["source-note"])

        controls = [utterance, corruption, severity, seed]
        outputs = [
            clean_audio,
            clean_waveform,
            clean_spectrogram,
            damaged_audio,
            damaged_waveform,
            damaged_spectrogram,
            metrics,
            source_note,
        ]
        demo.load(render_lab, inputs=controls, outputs=outputs, show_progress="hidden")
        regenerate.click(next_seed, inputs=seed, outputs=seed).then(
            render_lab,
            inputs=controls,
            outputs=outputs,
            show_progress="hidden",
        )
        for control in controls[:3]:
            control.change(render_lab, inputs=controls, outputs=outputs, show_progress="hidden")
        seed.submit(render_lab, inputs=controls, outputs=outputs, show_progress="hidden")

    return demo


if __name__ == "__main__":
    build_demo().launch(
        server_name="127.0.0.1",
        server_port=7860,
        theme=LAUNCH_THEME,
        css=LAUNCH_CSS,
    )
