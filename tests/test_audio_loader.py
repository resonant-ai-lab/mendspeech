"""Unit tests for src/audio/loader.py."""

import math
import tempfile
from pathlib import Path

import pytest
import soundfile as sf
import torch

from src.audio.loader import (
    compute_audio_metadata,
    compute_clipping_ratio,
    compute_peak,
    compute_rms,
    load_audio,
    normalize_audio,
    peak_to_dbfs,
    resample_audio,
    rms_to_db,
    save_audio,
)


def test_rms_and_peak_calculations():
    # Synthetic sine wave: amplitude = 1.0 -> theoretical RMS = 1 / sqrt(2) approx 0.7071
    t = torch.linspace(0, 1, 16000)
    waveform = torch.sin(2 * math.pi * 440 * t).unsqueeze(0)

    rms = compute_rms(waveform)
    assert abs(rms - (1.0 / math.sqrt(2))) < 1e-2

    peak = compute_peak(waveform)
    assert abs(peak - 1.0) < 1e-3

    peak_db = peak_to_dbfs(peak)
    assert abs(peak_db - 0.0) < 1e-2


def test_clipping_ratio():
    # 50% clipped signal
    waveform = torch.tensor([[1.0, 1.0, 0.5, 0.2]])
    clip_ratio = compute_clipping_ratio(waveform, threshold=0.99)
    assert clip_ratio == 0.5


def test_normalization():
    # Low amplitude waveform
    t = torch.linspace(0, 1, 16000)
    waveform = (0.1 * torch.sin(2 * math.pi * 440 * t)).unsqueeze(0)

    # Normalize to -20 dBFS
    target_db = -20.0
    normalized = normalize_audio(waveform, target_rms_db=target_db)

    norm_rms = compute_rms(normalized)
    norm_db = rms_to_db(norm_rms)
    assert abs(norm_db - target_db) < 0.2


def test_save_and_load_roundtrip():
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir) / "test_tone.wav"
        t = torch.linspace(0, 1, 16000)
        orig_waveform = (0.5 * torch.sin(2 * math.pi * 440 * t)).unsqueeze(0)

        # Save
        save_audio(tmp_path, orig_waveform, sample_rate=16000)
        assert tmp_path.exists()

        # Load
        loaded_wav, loaded_sr = load_audio(tmp_path, target_sr=16000, mono=True)
        assert loaded_sr == 16000
        assert loaded_wav.shape == (1, 16000)

        # Metadata
        meta = compute_audio_metadata(tmp_path, clip_id="tone_440")
        assert meta.sample_rate == 16000
        assert meta.channels == 1
        assert meta.duration_sec == 1.0
        assert meta.clipping_ratio == 0.0


def test_resampling():
    t = torch.linspace(0, 1, 48000)
    orig_wav = (0.5 * torch.sin(2 * math.pi * 440 * t)).unsqueeze(0)

    # Resample 48 kHz to 16 kHz
    resampled = resample_audio(orig_wav, orig_sr=48000, target_sr=16000)
    assert resampled.shape == (1, 16000)
