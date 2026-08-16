"""Tests for STFT computation and resolution bookkeeping (src/audio/stft.py)."""

import pytest
import torch

from src.audio.stft import (
    DEFAULT_HOP_16K,
    DEFAULT_N_FFT_16K,
    compute_stft,
    dominant_frequency,
    spectrogram_db,
    stft_resolutions,
)


def _sine(freq_hz: float, duration_s: float, sample_rate: int) -> torch.Tensor:
    t = torch.arange(int(duration_s * sample_rate)) / sample_rate
    return torch.sin(2 * torch.pi * freq_hz * t).double().float()


class TestComputeStft:
    def test_output_shape_matches_hop_and_fft(self):
        sr, n_fft, hop = 16000, 400, 160
        wave = _sine(440.0, 1.0, sr)
        spec = compute_stft(wave, n_fft=n_fft, hop_length=hop)
        expected_frames = 1 + wave.numel() // hop  # center=True
        assert spec.shape == (n_fft // 2 + 1, expected_frames)

    def test_accepts_channels_first_mono(self):
        sr, n_fft, hop = 16000, 400, 160
        wave = _sine(440.0, 0.5, sr).unsqueeze(0)  # (1, num_samples)
        spec = compute_stft(wave, n_fft=n_fft, hop_length=hop)
        assert spec.shape == (n_fft // 2 + 1, 1 + wave.numel() // hop)

    def test_rejects_non_mono_input(self):
        stereo = torch.randn(2, 16000)
        with pytest.raises(ValueError):
            compute_stft(stereo, n_fft=400, hop_length=160)

    def test_power_spectrogram_is_non_negative(self):
        wave = _sine(440.0, 0.5, 16000)
        spec = compute_stft(wave, n_fft=512, hop_length=128)
        assert (spec >= 0).all()


class TestSpectrogramDb:
    def test_peak_normalized_to_zero_db(self):
        wave = _sine(440.0, 0.5, 16000)
        spec_db = spectrogram_db(wave, n_fft=512, hop_length=128)
        assert spec_db.max().item() == pytest.approx(0.0, abs=1e-4)

    def test_floor_is_respected(self):
        wave = torch.zeros(8000)  # silence
        spec_db = spectrogram_db(wave, n_fft=512, hop_length=128, floor_db=-80.0)
        assert spec_db.min().item() >= -80.0 - 1e-6


class TestStftResolutions:
    def test_speech_defaults_at_16k(self):
        res = stft_resolutions(DEFAULT_N_FFT_16K, DEFAULT_HOP_16K, 16000)
        assert res["window_ms"] == pytest.approx(25.0)
        assert res["hop_ms"] == pytest.approx(10.0)
        assert res["delta_f_hz"] == pytest.approx(40.0)
        assert res["num_freq_bins"] == 201

    def test_resolution_tradeoff_directions(self):
        # Doubling n_fft halves frequency spacing (finer frequency detail).
        small = stft_resolutions(256, 64, 16000)
        large = stft_resolutions(512, 128, 16000)
        assert large["delta_f_hz"] == pytest.approx(small["delta_f_hz"] / 2)
        assert large["delta_t_ms"] == pytest.approx(small["delta_t_ms"] * 2)


class TestDominantFrequency:
    def test_recovers_tone_frequency(self):
        sr = 16000
        wave = _sine(1000.0, 1.0, sr)
        freq, _ = dominant_frequency(wave, sr, n_fft=4096)
        assert freq == pytest.approx(1000.0, abs=sr / 4096)
