"""Objective audio quality metrics for clean-versus-corrupted waveform pairs.

Day 5 module. Each metric reduces one aspect of degradation to a scalar.
No single number captures perceptual speech quality; the dataclass returned
by :func:`compute_pair_metrics` keeps all measurements together so the
caller can compare across corruption types, severities, and clips.

All functions accept mono waveforms. Clean and corrupted inputs must have
the same length and sample rate.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Union

import numpy as np
import torch
from numpy.typing import NDArray

from src.audio.features import compute_log_mel
from src.audio.loader import compute_peak, compute_rms, peak_to_dbfs, rms_to_db

Array = NDArray[np.float32]
Waveform = Union[torch.Tensor, Array]

# Sentinel SNR for a pair where corrupted == clean (no residual energy).
SNR_SENTINEL_DB = 100.0


@dataclass
class AudioPairMetrics:
    """Measurements for one clean/corrupted pair.

    Attributes:
        clip_id: Source clip identifier from the benchmark manifest.
        speaker_id: Speaker identifier from the manifest.
        corruption: Operator name applied by SpeechDamageBench.
        severity: Preset level (mild / medium / severe).
        seed: Integer seed used to generate this realization.
        clean_rms_db: RMS of the clean waveform in dBFS.
        corrupted_rms_db: RMS of the corrupted waveform in dBFS.
        clean_peak_dbfs: Peak amplitude of the clean waveform in dBFS.
        corrupted_peak_dbfs: Peak amplitude of the corrupted waveform in dBFS.
        snr_db: Signal-to-noise ratio between clean and corrupted in dB.
            Higher means closer to the original. Sentinel 100.0 when identical.
        log_mel_distance: Mean absolute difference between clean and
            corrupted log-Mel spectrograms. Lower means spectrally closer.
    """

    clip_id: str
    speaker_id: str
    corruption: str
    severity: str
    seed: int
    clean_rms_db: float
    corrupted_rms_db: float
    clean_peak_dbfs: float
    corrupted_peak_dbfs: float
    snr_db: float
    log_mel_distance: float

    def to_dict(self) -> dict:
        """Return a flat dict suitable for csv.DictWriter."""
        return asdict(self)


def _to_numpy(waveform: Waveform) -> Array:
    """Convert a torch tensor or numpy array to a 1-D float32 numpy array."""
    if isinstance(waveform, torch.Tensor):
        return waveform.detach().cpu().numpy().astype(np.float32).flatten()
    return np.asarray(waveform, dtype=np.float32).flatten()


def compute_snr(clean: Waveform, corrupted: Waveform) -> float:
    """Compute signal-to-noise ratio in dB for a known-reference pair.

    SNR = 10 * log10(signal_power / noise_power), where signal_power is the
    mean square of the clean waveform and noise_power is the mean square of
    the residual (corrupted - clean).

    This metric is meaningful for additive noise but misleading for
    non-linear distortions such as clipping, bandwidth reduction,
    dropout, and reverberation; see docs/metric_limitations.md.

    Args:
        clean: Mono clean waveform.
        corrupted: Mono corrupted waveform, same length as clean.

    Returns:
        SNR in decibels. Returns 100.0 if residual power is effectively zero.

    Raises:
        ValueError: If lengths differ.
    """
    clean_np = _to_numpy(clean)
    corrupted_np = _to_numpy(corrupted)
    if clean_np.shape != corrupted_np.shape:
        raise ValueError(
            f"Length mismatch: clean {clean_np.shape[0]} vs corrupted "
            f"{corrupted_np.shape[0]}"
        )

    residual = corrupted_np - clean_np
    signal_power = float(np.mean(clean_np.astype(np.float64) ** 2))
    noise_power = float(np.mean(residual.astype(np.float64) ** 2))

    if noise_power < 1e-12:
        return SNR_SENTINEL_DB
    return float(10.0 * np.log10(max(signal_power, 1e-12) / max(noise_power, 1e-12)))


def compute_log_mel_distance(
    clean: Waveform,
    corrupted: Waveform,
    sample_rate: int,
) -> float:
    """Compute mean absolute difference between log-Mel spectrogram pairs.

    Both waveforms are converted through the same Day 3 log-Mel pipeline
    (80 Mel bands, 16 kHz defaults). The distance averages absolute frame-
    wise differences over every Mel bin and time step.

    Args:
        clean: Mono clean waveform tensor or array.
        corrupted: Mono corrupted waveform tensor or array, same length.
        sample_rate: Sample rate in Hz shared by both waveforms.

    Returns:
        Mean absolute log-Mel difference. 0.0 means spectrally identical.

    Raises:
        ValueError: If shapes differ after conversion to torch tensors.
    """
    clean_t = torch.as_tensor(_to_numpy(clean))
    corrupted_t = torch.as_tensor(_to_numpy(corrupted))
    if clean_t.shape != corrupted_t.shape:
        raise ValueError(
            f"Shape mismatch: clean {tuple(clean_t.shape)} vs corrupted "
            f"{tuple(corrupted_t.shape)}"
        )

    clean_mel, _ = compute_log_mel(clean_t, sample_rate)
    corrupted_mel, _ = compute_log_mel(corrupted_t, sample_rate)

    if clean_mel.shape != corrupted_mel.shape:
        raise ValueError(
            f"Log-Mel shape mismatch: {tuple(clean_mel.shape)} vs "
            f"{tuple(corrupted_mel.shape)}. Check that both waveforms have "
            f"the same number of samples."
        )

    return float(torch.mean(torch.abs(clean_mel - corrupted_mel)).item())


def compute_pair_metrics(
    clean: Waveform,
    corrupted: Waveform,
    sample_rate: int,
    clip_id: str,
    speaker_id: str,
    corruption: str,
    severity: str,
    seed: int,
) -> AudioPairMetrics:
    """Compute all Day 5 metrics for one clean/corrupted waveform pair.

    Args:
        clean: Mono clean waveform (torch tensor or numpy array).
        corrupted: Mono corrupted waveform, same length and sample rate.
        sample_rate: Shared sample rate in Hz.
        clip_id: Source identifier from the benchmark manifest.
        speaker_id: Speaker identifier from the benchmark manifest.
        corruption: SpeechDamageBench operator name.
        severity: Preset severity label.
        seed: Integer seed used by SpeechDamageBench for this realization.

    Returns:
        An :class:`AudioPairMetrics` record with all scalar measurements.
    """
    clean_np = _to_numpy(clean)
    corrupted_np = _to_numpy(corrupted)

    clean_rms = rms_to_db(float(np.sqrt(np.mean(clean_np.astype(np.float64) ** 2))))
    corrupted_rms = rms_to_db(
        float(np.sqrt(np.mean(corrupted_np.astype(np.float64) ** 2)))
    )
    clean_peak = peak_to_dbfs(float(np.max(np.abs(clean_np))))
    corrupted_peak = peak_to_dbfs(float(np.max(np.abs(corrupted_np))))

    snr = compute_snr(clean_np, corrupted_np)
    mel_dist = compute_log_mel_distance(clean_t := torch.as_tensor(clean_np),
                                        torch.as_tensor(corrupted_np), sample_rate)

    return AudioPairMetrics(
        clip_id=clip_id,
        speaker_id=speaker_id,
        corruption=corruption,
        severity=severity,
        seed=seed,
        clean_rms_db=round(clean_rms, 4),
        corrupted_rms_db=round(corrupted_rms, 4),
        clean_peak_dbfs=round(clean_peak, 4),
        corrupted_peak_dbfs=round(corrupted_peak, 4),
        snr_db=round(snr, 4),
        log_mel_distance=round(mel_dist, 6),
    )
