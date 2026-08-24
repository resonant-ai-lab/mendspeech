"""Tests for Day 5 objective audio metrics."""

import numpy as np
import pytest
import torch

from src.metrics.audio_metrics import (
    SNR_SENTINEL_DB,
    AudioPairMetrics,
    compute_log_mel_distance,
    compute_pair_metrics,
    compute_snr,
)


class TestComputeSNR:
    """SNR correctness on synthetic signals."""

    def test_identical_signals_return_sentinel(self):
        wave = np.ones(1000, dtype=np.float32) * 0.1
        assert compute_snr(wave, wave.copy()) == SNR_SENTINEL_DB

    def test_pure_tone_with_known_noise_level(self):
        rng = np.random.default_rng(42)
        clean = (0.5 * np.sin(2 * np.pi * 440 * np.arange(16000) / 16000)).astype(
            np.float32
        )
        noise = (rng.standard_normal(16000) * 0.01).astype(np.float32)
        corrupted = clean + noise
        snr = compute_snr(clean, corrupted)
        # Signal power ~ 0.125, noise power ~ 0.0001 -> SNR ~ 10*log10(1250) ~ 31 dB
        assert 25.0 < snr < 40.0, f"Expected SNR in [25, 40], got {snr:.2f}"

    def test_length_mismatch_raises(self):
        with pytest.raises(ValueError, match="Length mismatch"):
            compute_snr(np.ones(100), np.ones(200))


class TestLogMelDistance:
    """Log-Mel distance behaviour on synthetic signals."""

    def test_identical_waveforms_give_zero_distance(self):
        wave = torch.randn(8000)
        dist = compute_log_mel_distance(wave, wave.clone(), 16000)
        assert dist == pytest.approx(0.0, abs=1e-6)

    def test_different_waveforms_give_positive_distance(self):
        rng = np.random.default_rng(7)
        clean = torch.from_numpy(
            (0.5 * np.sin(2 * np.pi * 220 * np.arange(8000) / 8000)).astype(np.float32)
        )
        corrupted = clean + torch.from_numpy(
            (rng.standard_normal(8000) * 0.3).astype(np.float32)
        )
        dist = compute_log_mel_distance(clean, corrupted, 16000)
        assert dist > 0.5, f"Expected distance > 0.5 for heavy noise, got {dist:.4f}"


class TestPairMetrics:
    """Integration of all metrics into the AudioPairMetrics dataclass."""

    def test_returns_all_fields(self):
        rng = np.random.default_rng(99)
        clean = (0.3 * np.sin(2 * np.pi * 300 * np.arange(12000) / 16000)).astype(
            np.float32
        )
        corrupted = clean + (rng.standard_normal(12000) * 0.05).astype(np.float32)
        result = compute_pair_metrics(
            clean=clean,
            corrupted=corrupted,
            sample_rate=16000,
            clip_id="test_001",
            speaker_id="spk_test",
            corruption="additive_noise",
            severity="medium",
            seed=42,
        )
        assert isinstance(result, AudioPairMetrics)
        d = result.to_dict()
        expected_keys = {
            "clip_id",
            "speaker_id",
            "corruption",
            "severity",
            "seed",
            "clean_rms_db",
            "corrupted_rms_db",
            "clean_peak_dbfs",
            "corrupted_peak_dbfs",
            "snr_db",
            "log_mel_distance",
        }
        assert set(d.keys()) == expected_keys
        assert result.snr_db > 0.0
        assert result.log_mel_distance > 0.0
