"""Reusable Modal entry point for running MendSpeech ASR on cloud L4 GPUs.

Allows running baseline ASR experiments on Modal's L4 GPU tier or locally with a unified CLI:
    - Cloud execution: modal run infra/modal_asr.py --audio-path data/clean_16k/clean_01.wav
    - Local fallback:  python infra/modal_asr.py --audio-path data/clean_16k/clean_01.wav --local
"""

import io
from pathlib import Path
import sys
REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))
from typing import Dict, Optional, Union

import modal

# Modal application definition
app = modal.App("mendspeech-asr")

# Container image definition with torch, torchaudio, and speech dependencies
asr_image = (
    modal.Image.debian_slim(python_version="3.11")
    .pip_install(
        "torch>=2.0.0",
        "torchaudio>=2.0.0",
        "soundfile>=0.12.0",
        "numpy>=1.24.0",
    )
)


@app.function(image=asr_image, gpu="L4", timeout=300)
def transcribe_remote(audio_bytes: bytes, clip_id: str = "audio") -> Dict[str, Union[str, float, int]]:
    """Runs ASR inference on a remote Modal L4 GPU container.

    Args:
        audio_bytes: Raw audio file bytes.
        clip_id: Identifier for the audio sample.

    Returns:
        Dictionary with transcript, duration, and confidence.
    """
    import io
    import soundfile as sf
    import torch
    import torchaudio

    buffer = io.BytesIO(audio_bytes)
    data, sr = sf.read(buffer, dtype="float32")
    waveform = torch.from_numpy(data)

    if waveform.dim() == 1:
        waveform = waveform.unsqueeze(0)
    elif waveform.dim() == 2 and waveform.shape[0] != 1:
        waveform = torch.mean(waveform, dim=0, keepdim=True)

    bundle = torchaudio.pipelines.WAV2VEC2_ASR_BASE_960H
    model = bundle.get_model().to("cuda")
    labels = bundle.get_labels()

    if sr != bundle.sample_rate:
        resampler = torchaudio.transforms.Resample(orig_freq=sr, new_freq=bundle.sample_rate)
        waveform = resampler(waveform)

    waveform = waveform.to("cuda")
    duration_sec = waveform.shape[-1] / bundle.sample_rate

    with torch.no_grad():
        emissions, _ = model(waveform)

    # CTC greedy decoding inside container
    probs = torch.softmax(emissions[0], dim=-1)
    max_probs, argmax_indices = torch.max(probs, dim=-1)
    argmax_list = argmax_indices.tolist()

    tokens = []
    prev_id = -1
    for t, idx in enumerate(argmax_list):
        if idx == prev_id:
            continue
        prev_id = idx
        if idx == 0:  # blank
            continue
        tokens.append(labels[idx] if idx < len(labels) else "?")

    transcript = "".join(tokens).replace("|", " ").strip()
    avg_conf = float(torch.mean(max_probs).item())

    return {
        "clip_id": clip_id,
        "transcript": transcript,
        "duration_sec": round(duration_sec, 3),
        "average_confidence": round(avg_conf, 4),
        "device": "Modal L4 (CUDA)",
    }


def transcribe_local_cli(audio_path: Path) -> Dict[str, Union[str, float, int]]:
    """Runs ASR inference locally on CPU/GPU."""
    from src.asr.baseline import ASRBaseline

    baseline = ASRBaseline()
    output = baseline.transcribe_file(audio_path)
    return {
        "clip_id": output.clip_id,
        "transcript": output.transcript,
        "duration_sec": output.duration_sec,
        "average_confidence": output.average_confidence,
        "device": str(baseline.device),
    }


@app.local_entrypoint()
def main(audio_path: str = "data/clean_16k/clean_01.wav", local: bool = False):
    """Entrypoint to transcribe an audio clip via Modal L4 or local device."""
    p = Path(audio_path)
    if not p.exists():
        print(f"Error: file not found: {audio_path}")
        return

    print(f"--- MendSpeech ASR Entrypoint ---")
    print(f"Target audio: {p} ({p.stat().st_size / 1024:.1f} KB)")

    if local:
        print(f"Running locally...")
        result = transcribe_local_cli(p)
    else:
        print(f"Submitting job to Modal L4 GPU...")
        audio_bytes = p.read_bytes()
        result = transcribe_remote.remote(audio_bytes=audio_bytes, clip_id=p.stem)

    print("\nResult:")
    for k, v in result.items():
        print(f"  {k}: {v}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="MendSpeech ASR Modal / Local Runner")
    parser.add_argument("--audio-path", type=str, default="data/clean_16k/clean_01.wav")
    parser.add_argument("--local", action="store_true", default=True, help="Run locally")
    args = parser.parse_args()

    main(audio_path=args.audio_path, local=args.local)
