"""MendSpeech Audio I/O, Resampling, and Acoustic Feature Utilities.

Day 1 foundational module for robust waveform ingestion, metric computation,
and sample rate standardization.
"""

from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union

import numpy as np
import soundfile as sf
import torch
import torchaudio
import torchaudio.transforms as T


@dataclass
class AudioMetadata:
    """Dataclass holding essential physical and acoustic metadata of an audio file."""
    clip_id: str
    file_path: str
    sample_rate: int
    channels: int
    duration_sec: float
    num_samples: int
    rms_energy: float
    rms_db: float
    peak_amplitude: float
    peak_dbfs: float
    clipping_ratio: float


def load_audio(
    file_path: Union[str, Path],
    target_sr: Optional[int] = 16000,
    mono: bool = True,
    normalize: bool = False,
    target_rms_db: float = -20.0
) -> Tuple[torch.Tensor, int]:
    """Loads an audio file, standardizes channels and sample rate, and returns a PyTorch tensor.

    Args:
        file_path: Path to the input audio file.
        target_sr: Target sample rate in Hz. If None, preserves original sample rate.
        mono: If True, averages multi-channel audio to a single channel.
        normalize: If True, normalizes audio to target_rms_db.
        target_rms_db: Desired RMS level in decibels if normalize is True.

    Returns:
        Tuple of (waveform_tensor, sample_rate) where waveform_tensor has shape [channels, time].
    """
    file_path = str(file_path)
    if not Path(file_path).exists():
        raise FileNotFoundError(f"Audio file not found: {file_path}")

    # Load audio using soundfile for maximum format reliability across OS environments
    data, sr = sf.read(file_path, dtype="float32")

    # Shape handling: ensure tensor is [channels, time]
    if data.ndim == 1:
        waveform = torch.from_numpy(data).unsqueeze(0)  # [1, time]
    else:
        waveform = torch.from_numpy(data.T)  # [channels, time]

    # Convert to mono if requested
    if mono and waveform.shape[0] > 1:
        waveform = torch.mean(waveform, dim=0, keepdim=True)

    # Resample if target_sr is specified and differs from original
    if target_sr is not None and sr != target_sr:
        waveform = resample_audio(waveform, orig_sr=sr, target_sr=target_sr)
        sr = target_sr

    # Optional RMS normalization
    if normalize:
        waveform = normalize_audio(waveform, target_rms_db=target_rms_db)

    return waveform, sr


def save_audio(
    file_path: Union[str, Path],
    waveform: torch.Tensor,
    sample_rate: int,
    subtype: str = "PCM_16"
) -> None:
    """Saves a PyTorch waveform tensor to disk.

    Args:
        file_path: Destination path.
        waveform: PyTorch tensor of shape [channels, time] or [time].
        sample_rate: Sampling frequency in Hz.
        subtype: SoundFile subtype (e.g. 'PCM_16', 'FLOAT').
    """
    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    tensor_cpu = waveform.detach().cpu()
    if tensor_cpu.ndim == 2:
        # soundfile expects [time, channels]
        data = tensor_cpu.numpy().T
    elif tensor_cpu.ndim == 1:
        data = tensor_cpu.numpy()
    else:
        raise ValueError(f"Waveform must have 1 or 2 dimensions, got shape {waveform.shape}")

    sf.write(str(path), data, samplerate=sample_rate, subtype=subtype)


def resample_audio(
    waveform: torch.Tensor,
    orig_sr: int,
    target_sr: int,
    resampling_method: str = "sinc_interp_hann"
) -> torch.Tensor:
    """High-fidelity audio resampling using band-limited sinc interpolation with Kaiser/Hann window.

    Args:
        waveform: Input tensor of shape [channels, time] or [time].
        orig_sr: Original sampling rate in Hz.
        target_sr: Target sampling rate in Hz.
        resampling_method: Torchaudio resampling filter type.

    Returns:
        Resampled waveform tensor.
    """
    if orig_sr == target_sr:
        return waveform

    resampler = T.Resample(
        orig_freq=orig_sr,
        new_freq=target_sr,
        resampling_method=resampling_method
    )
    return resampler(waveform)


def compute_rms(waveform: torch.Tensor, eps: float = 1e-9) -> float:
    """Calculates linear Root Mean Square (RMS) energy: sqrt(mean(x^2))."""
    return float(torch.sqrt(torch.mean(waveform.pow(2)) + eps).item())


def rms_to_db(rms: float, eps: float = 1e-9) -> float:
    """Converts linear RMS amplitude to decibels relative to full scale (dBFS)."""
    return float(20.0 * np.log10(max(rms, eps)))


def compute_peak(waveform: torch.Tensor) -> float:
    """Calculates the absolute peak amplitude of the waveform."""
    return float(torch.max(torch.abs(waveform)).item())


def peak_to_dbfs(peak: float, eps: float = 1e-9) -> float:
    """Converts peak amplitude to dBFS."""
    return float(20.0 * np.log10(max(peak, eps)))


def compute_clipping_ratio(waveform: torch.Tensor, threshold: float = 0.999) -> float:
    """Calculates the fraction of samples saturated at or above the clipping threshold."""
    total_samples = waveform.numel()
    if total_samples == 0:
        return 0.0
    clipped = torch.sum(torch.abs(waveform) >= threshold).item()
    return float(clipped / total_samples)


def normalize_audio(
    waveform: torch.Tensor,
    target_rms_db: float = -20.0,
    peak_limit: float = 0.95,
    eps: float = 1e-9
) -> torch.Tensor:
    """Normalizes waveform to target RMS level with safe peak headroom protection.

    Args:
        waveform: Input tensor [channels, time].
        target_rms_db: Desired RMS in dBFS.
        peak_limit: Maximum allowed peak to prevent digital clipping.
        eps: Epsilon to prevent division by zero.

    Returns:
        Normalized waveform tensor.
    """
    current_rms = compute_rms(waveform, eps=eps)
    target_rms = 10.0 ** (target_rms_db / 20.0)

    gain = target_rms / max(current_rms, eps)
    normalized = waveform * gain

    # Headroom protection: if normalized peak exceeds peak_limit, scale down
    peak = compute_peak(normalized)
    if peak > peak_limit:
        scaling_factor = peak_limit / max(peak, eps)
        normalized = normalized * scaling_factor

    return normalized


def compute_audio_metadata(
    file_path: Union[str, Path],
    clip_id: Optional[str] = None
) -> AudioMetadata:
    """Analyzes an audio file on disk and returns its complete acoustic metadata."""
    path = Path(file_path)
    if clip_id is None:
        clip_id = path.stem

    info = sf.info(str(path))
    data, sr = sf.read(str(path), dtype="float32")
    waveform = torch.from_numpy(data.T if data.ndim > 1 else data).unsqueeze(0) if data.ndim == 1 else torch.from_numpy(data.T)

    rms = compute_rms(waveform)
    rms_db = rms_to_db(rms)
    peak = compute_peak(waveform)
    peak_db = peak_to_dbfs(peak)
    clipping = compute_clipping_ratio(waveform)

    return AudioMetadata(
        clip_id=clip_id,
        file_path=str(path.resolve()),
        sample_rate=info.samplerate,
        channels=info.channels,
        duration_sec=round(info.duration, 4),
        num_samples=info.frames,
        rms_energy=round(rms, 6),
        rms_db=round(rms_db, 2),
        peak_amplitude=round(peak, 6),
        peak_dbfs=round(peak_db, 2),
        clipping_ratio=round(clipping, 6)
    )
