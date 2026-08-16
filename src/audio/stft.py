"""STFT computation and spectrogram visualization utilities for MendSpeech.

Day 2 module: wraps short-time Fourier transform computation with explicit
frame/hop control and resolution bookkeeping so every spectrogram carries
its own time/frequency resolution numbers (delta_t = hop / sample_rate,
delta_f = sample_rate / n_fft).
"""

from typing import Dict, Tuple

import torch
import torchaudio

# Standard speech configuration at 16 kHz: 25 ms analysis window with a 10 ms
# hop. Rationale: 25 ms is long enough to resolve formants (spaced ~1 kHz,
# needing ~4 Hz-per-bin order accuracy at speech fundamental frequencies) yet
# short enough that plosive onsets stay visible; 10 ms hop matches typical
# phoneme transition rates.
DEFAULT_N_FFT_16K = 400  # 25 ms at 16000 Hz
DEFAULT_HOP_16K = 160    # 10 ms at 16000 Hz


def compute_stft(
    waveform: torch.Tensor,
    n_fft: int,
    hop_length: int,
) -> torch.Tensor:
    """Computes the power spectrogram of a mono waveform.

    Args:
        waveform: 1-D waveform tensor, shape (num_samples,).
        n_fft: FFT size in samples. Sets frequency resolution.
        hop_length: Hop between successive frames in samples. Sets time
            resolution.

    Returns:
        Power spectrogram tensor of shape (num_freq_bins, num_frames), where
        num_freq_bins = n_fft // 2 + 1.
    """
    if waveform.dim() == 2 and waveform.shape[0] == 1:
        waveform = waveform[0]
    if waveform.dim() != 1:
        raise ValueError(f"Expected 1-D mono waveform, got shape {tuple(waveform.shape)}")
    spectrogram = torchaudio.transforms.Spectrogram(
        n_fft=n_fft, hop_length=hop_length, power=2.0, center=True
    )
    return spectrogram(waveform)


def spectrogram_db(
    waveform: torch.Tensor,
    n_fft: int,
    hop_length: int,
    floor_db: float = -100.0,
) -> torch.Tensor:
    """Computes a dB-scaled power spectrogram with a fixed noise floor.

    Args:
        waveform: 1-D mono waveform tensor.
        n_fft: FFT size in samples.
        hop_length: Hop length in samples.
        floor_db: Lower clamp in dB relative to the spectrogram maximum,
            applied after scaling.

    Returns:
        dB spectrogram of shape (num_freq_bins, num_frames).
    """
    power = compute_stft(waveform, n_fft=n_fft, hop_length=hop_length)
    amin = 1e-10
    spec_db = 10.0 * torch.log10(torch.clamp(power, min=amin))
    spec_db = spec_db - spec_db.max()  # normalize to 0 dB peak
    return torch.clamp(spec_db, min=floor_db)


def stft_resolutions(
    n_fft: int,
    hop_length: int,
    sample_rate: int,
) -> Dict[str, float]:
    """Returns the time and frequency resolution implied by STFT settings.

    Args:
        n_fft: FFT size in samples.
        hop_length: Hop length in samples.
        sample_rate: Waveform sample rate in Hz.

    Returns:
        Dict with 'window_ms', 'hop_ms', 'delta_t_ms', 'delta_f_hz', and
        'num_freq_bins'. delta_t_ms = hop / sr * 1000; delta_f_hz = sr / n_fft.
    """
    return {
        "window_ms": n_fft / sample_rate * 1000.0,
        "hop_ms": hop_length / sample_rate * 1000.0,
        "delta_t_ms": hop_length / sample_rate * 1000.0,
        "delta_f_hz": sample_rate / n_fft,
        "num_freq_bins": n_fft // 2 + 1,
    }


def dominant_frequency(
    waveform: torch.Tensor,
    sample_rate: int,
    n_fft: int = 4096,
) -> Tuple[float, torch.Tensor]:
    """Finds the dominant frequency of a stationary tone via STFT.

    Args:
        waveform: 1-D mono waveform (ideally a stationary tone).
        sample_rate: Sample rate in Hz.
        n_fft: FFT size; larger improves the frequency estimate.

    Returns:
        Tuple of (dominant frequency in Hz, mean power spectrogram of shape
        (num_freq_bins, num_frames)).
    """
    power = compute_stft(waveform, n_fft=n_fft, hop_length=n_fft // 4)
    mean_power = power.mean(dim=1)
    bin_hz = sample_rate / n_fft
    peak_bin = int(torch.argmax(mean_power).item())
    return peak_bin * bin_hz, mean_power
