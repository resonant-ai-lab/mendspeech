"""Tests for log-Mel feature extraction (src/audio/features.py)."""

import pytest
import torch

from src.audio.features import (
    DEFAULT_FLOOR_DB,
    DEFAULT_HOP_16K,
    DEFAULT_N_MELS,
    DEFAULT_N_FFT_16K,
    LogMelMetadata,
    compute_log_mel,
    mel_filterbank_matrix,
)


def _sine(freq_hz: float, duration_s: float, sample_rate: int) -> torch.Tensor:
    t = torch.arange(int(duration_s * sample_rate)) / sample_rate
    return torch.sin(2 * torch.pi * freq_hz * t).double().float()


class TestMelFilterbankMatrix:
    def test_shape_matches_stft_bins(self):
        fb = mel_filterbank_matrix(sample_rate=16000, n_fft=400, n_mels=80)
        assert fb.shape == (201, 80)  # (n_fft // 2 + 1, n_mels)

    def test_bands_are_non_negative_and_have_support(self):
        fb = mel_filterbank_matrix(sample_rate=16000, n_fft=400, n_mels=80)
        assert (fb >= 0).all()
        assert (fb.sum(dim=0) > 0).all()

    def test_peak_bins_march_upward(self):
        # Perceptual warping: band peaks must move up in frequency; the
        # spacing between peaks grows because bands are even in Mel, not Hz.
        fb = mel_filterbank_matrix(sample_rate=16000, n_fft=400, n_mels=80)
        peaks = fb.argmax(dim=0)
        assert (peaks[1:] >= peaks[:-1]).all()

    def test_high_bands_span_more_bins_than_low_bands(self):
        # Low bands pack into ~1 linear bin, high bands into many: this is
        # why 201 linear bins compress to 80 perceptually spaced bands.
        fb = mel_filterbank_matrix(sample_rate=16000, n_fft=400, n_mels=80)
        widths = (fb > 0).sum(dim=0)
        assert widths[-1].item() > widths[0].item()

    def test_explicit_f_max_overrides_nyquist(self):
        fb = mel_filterbank_matrix(
            sample_rate=16000, n_fft=400, n_mels=40, f_max=4000.0
        )
        assert fb.shape == (201, 40)


class TestComputeLogMel:
    def test_shape_n_mels_by_frames(self):
        sr, n_mels = 16000, DEFAULT_N_MELS
        wave = _sine(440.0, 1.0, sr)
        log_mel, meta = compute_log_mel(wave, sr)
        expected_frames = 1 + wave.numel() // DEFAULT_HOP_16K  # center=True
        assert log_mel.shape == (n_mels, expected_frames)
        assert meta.num_frames == expected_frames

    def test_accepts_channels_first_mono(self):
        wave = _sine(440.0, 0.5, 16000).unsqueeze(0)  # (1, num_samples)
        log_mel, _ = compute_log_mel(wave, 16000)
        assert log_mel.shape[0] == DEFAULT_N_MELS

    def test_rejects_non_mono_input(self):
        stereo = torch.randn(2, 16000)
        with pytest.raises(ValueError):
            compute_log_mel(stereo, 16000)

    def test_log_compression_and_peak_normalization(self):
        wave = _sine(440.0, 0.5, 16000)
        log_mel, _ = compute_log_mel(wave, 16000)
        assert log_mel.max().item() == pytest.approx(0.0, abs=1e-4)
        assert (log_mel <= 1e-4).all()
        # a single tone is spectrally sparse: distant bands sit at the floor
        assert (log_mel <= -60).any()

    def test_floor_is_respected(self):
        wave = torch.zeros(8000)  # silence
        log_mel, _ = compute_log_mel(wave, 16000, floor_db=-80.0)
        assert log_mel.min().item() >= -80.0 - 1e-6

    def test_normalization_records_stats(self):
        wave = _sine(440.0, 0.5, 16000)
        log_mel, meta = compute_log_mel(wave, 16000, normalize=True)
        assert log_mel.mean().abs().item() < 1e-5
        assert log_mel.std().item() == pytest.approx(1.0, abs=1e-2)
        assert meta.mean is not None
        assert meta.std is not None

    def test_metadata_reproduces_pipeline_settings(self):
        wave = _sine(440.0, 1.0, 16000)
        _, meta = compute_log_mel(wave, 16000, n_mels=64)
        assert isinstance(meta, LogMelMetadata)
        assert meta.sample_rate == 16000
        assert meta.n_fft == DEFAULT_N_FFT_16K
        assert meta.hop_length == DEFAULT_HOP_16K
        assert meta.n_mels == 64
        assert meta.f_min == 0.0
        assert meta.f_max == 8000.0  # Nyquist default at 16 kHz
        assert meta.log_floor_db == DEFAULT_FLOOR_DB
        assert meta.duration_s == pytest.approx(1.0)

    def test_frames_scale_with_duration_but_mels_stay_fixed(self):
        # Shape contract for batching: only the time axis depends on length.
        short = _sine(440.0, 1.0, 16000)
        long = _sine(440.0, 2.0, 16000)
        short_mel, short_meta = compute_log_mel(short, 16000)
        long_mel, long_meta = compute_log_mel(long, 16000)
        assert short_mel.shape[0] == long_mel.shape[0] == DEFAULT_N_MELS
        assert long_mel.shape[1] == 2 * short_mel.shape[1] - 1
        assert long_meta.num_frames == 1 + long.numel() // DEFAULT_HOP_16K
        assert long_meta.duration_s == pytest.approx(2.0)