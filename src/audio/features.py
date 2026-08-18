"""Mel-scale and log-Mel feature extraction for MendSpeech.

Day 3 module: warps the linear-frequency STFT from src/audio/stft.py onto
the perceptual Mel scale using an overlapping triangular filterbank, applies
log compression with a dB-scaled noise floor, and returns the feature tensor
together with a metadata record (:class:`LogMelMetadata`) so every feature
matrix carries the parameters needed to reproduce it exactly.
"""

from dataclasses import dataclass
from typing import Optional, Tuple

import torch
import torchaudio

from src.audio.stft import DEFAULT_HOP_16K, DEFAULT_N_FFT_16K

# Modern ASR standard: 80 Mel bands (Conformer / FastConformer front-end).
DEFAULT_N_MELS = 80
DEFAULT_F_MIN_HZ = 0.0
DEFAULT_F_MAX_HZ = 8000.0  # Nyquist frequency at the 16 kHz working rate
DEFAULT_FLOOR_DB = -100.0


@dataclass
class LogMelMetadata:
    """Reproducibility metadata for one log-Mel feature tensor.

    Attributes:
        sample_rate: Waveform sample rate in Hz.
        n_fft: FFT size in samples (analysis window = n_fft / sample_rate s).
        hop_length: Hop between frames in samples (frame period = hop / sr s).
        n_mels: Number of Mel filterbank bands.
        f_min: Lowest filterbank edge in Hz.
        f_max: Highest filterbank edge in Hz.
        log_floor_db: Lower clamp in dB relative to the tensor maximum,
            applied after log compression.
        num_frames: Number of time frames (columns) in the feature tensor.
        duration_s: Analyzed audio duration in seconds.
        mean: Mean removed by optional normalization, or None if not applied.
        std: Standard deviation applied by optional normalization, or None.
    """

    sample_rate: int
    n_fft: int
    hop_length: int
    n_mels: int
    f_min: float
    f_max: float
    log_floor_db: float
    num_frames: int
    duration_s: float
    mean: Optional[float] = None
    std: Optional[float] = None


def mel_filterbank_matrix(
    sample_rate: int,
    n_fft: int,
    n_mels: int = DEFAULT_N_MELS,
    f_min: float = DEFAULT_F_MIN_HZ,
    f_max: Optional[float] = None,
) -> torch.Tensor:
    """Returns the triangular Mel filterbank for a given STFT resolution.

    Args:
        sample_rate: Sample rate in Hz.
        n_fft: FFT size in samples; the filterbank spans the
            n_fft // 2 + 1 linear-frequency bins of the STFT.
        n_mels: Number of Mel bands.
        f_min: Lower filterbank edge in Hz.
        f_max: Upper filterbank edge in Hz; defaults to the Nyquist
            frequency (sample_rate / 2).

    Returns:
        Filterbank matrix of shape (n_fft // 2 + 1, n_mels). Column i holds
        the triangular weighting applied to each linear-frequency bin for
        Mel band i; triangles are narrow at low frequencies and wide at high
        frequencies because they are spaced evenly in Mel, not in Hz.
    """
    if f_max is None:
        f_max = sample_rate / 2.0
    return torchaudio.functional.melscale_fbanks(
        n_freqs=n_fft // 2 + 1,
        f_min=f_min,
        f_max=f_max,
        n_mels=n_mels,
        sample_rate=sample_rate,
    )


def compute_log_mel(
    waveform: torch.Tensor,
    sample_rate: int,
    n_mels: int = DEFAULT_N_MELS,
    n_fft: int = DEFAULT_N_FFT_16K,
    hop_length: int = DEFAULT_HOP_16K,
    f_min: float = DEFAULT_F_MIN_HZ,
    f_max: Optional[float] = None,
    floor_db: float = DEFAULT_FLOOR_DB,
    normalize: bool = False,
) -> Tuple[torch.Tensor, LogMelMetadata]:
    """Computes a log-Mel spectrogram with reproducibility metadata.

    Pipeline: waveform -> power STFT (n_fft / hop, center=True) -> Mel
    filterbank (n_mels triangular bands over [f_min, f_max]) ->
    10 * log10 with a 1e-10 floor -> peak renormalized to 0 dB -> clamped
    at floor_db. Optionally applies per-utterance mean/std normalization.

    Args:
        waveform: 1-D mono waveform tensor, shape (num_samples,). A
            channels-first mono tensor (1, num_samples) is accepted.
        sample_rate: Sample rate in Hz.
        n_mels: Number of Mel bands.
        n_fft: FFT size in samples.
        hop_length: Hop in samples.
        f_min: Lowest Mel edge in Hz.
        f_max: Highest Mel edge in Hz; defaults to Nyquist (sample_rate / 2).
        floor_db: Lower clamp in dB relative to the tensor maximum.
        normalize: If True, standardize the output to zero mean and unit
            variance per utterance, recording the statistics in metadata.

    Returns:
        Tuple of (log_mel, metadata): log_mel has shape (n_mels,
        num_frames); metadata records every parameter needed to reproduce
        the tensor. num_frames = 1 + num_samples // hop_length with
        center=True framing.
    """
    if f_max is None:
        f_max = sample_rate / 2.0
    if waveform.dim() == 2 and waveform.shape[0] == 1:
        waveform = waveform[0]
    if waveform.dim() != 1:
        raise ValueError(
            f"Expected 1-D mono waveform, got shape {tuple(waveform.shape)}"
        )

    mel_spec = torchaudio.transforms.MelSpectrogram(
        sample_rate=sample_rate,
        n_fft=n_fft,
        hop_length=hop_length,
        n_mels=n_mels,
        f_min=f_min,
        f_max=f_max,
        power=2.0,
        center=True,
    )
    mel = mel_spec(waveform)  # (n_mels, num_frames)
    amin = 1e-10
    log_mel = 10.0 * torch.log10(torch.clamp(mel, min=amin))
    log_mel = log_mel - log_mel.max()  # normalize to 0 dB peak
    log_mel = torch.clamp(log_mel, min=floor_db)

    metadata = LogMelMetadata(
        sample_rate=sample_rate,
        n_fft=n_fft,
        hop_length=hop_length,
        n_mels=n_mels,
        f_min=f_min,
        f_max=f_max,
        log_floor_db=floor_db,
        num_frames=log_mel.shape[1],
        duration_s=waveform.numel() / sample_rate,
    )

    if normalize:
        mean = log_mel.mean()
        std = log_mel.std()
        log_mel = (log_mel - mean) / std
        metadata.mean = float(mean.item())
        metadata.std = float(std.item())

    return log_mel, metadata