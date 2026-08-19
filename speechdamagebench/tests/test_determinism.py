"""SpeechDamageBench Day 4 contract: same seed, same waveform."""

from __future__ import annotations

import math

import numpy as np
import pytest

from speechdamagebench import (
    CORRUPTIONS,
    DamageConfig,
    apply_damage,
)
from speechdamagebench.presets import PRESETS, SEVERITIES


def _tone(sr: int = 16000, seconds: float = 0.8, freq_hz: float = 220.0) -> np.ndarray:
    n = int(sr * seconds)
    t = np.arange(n, dtype=np.float32) / float(sr)
    return (0.4 * np.sin(2.0 * math.pi * freq_hz * t)).astype(np.float32)


@pytest.mark.parametrize("corruption", CORRUPTIONS)
def test_same_seed_is_identical(corruption: str) -> None:
    wave = _tone()
    cfg = DamageConfig(corruption, "medium", seed=7, source_id="tone")
    a, rec_a = apply_damage(wave, 16000, cfg)
    b, rec_b = apply_damage(wave, 16000, cfg)
    np.testing.assert_array_equal(a, b)
    assert rec_a.parameters == rec_b.parameters
    assert rec_a.seed == 7
    assert a.shape == wave.shape


@pytest.mark.parametrize(
    "corruption",
    [c for c in CORRUPTIONS if c not in ("clipping", "bandwidth")],
)
def test_seed_change_changes_waveform_not_params(corruption: str) -> None:
    wave = _tone()
    a, rec_a = apply_damage(wave, 16000, DamageConfig(corruption, "medium", 7, "tone"))
    b, rec_b = apply_damage(wave, 16000, DamageConfig(corruption, "medium", 8, "tone"))
    assert rec_a.parameters == rec_b.parameters
    assert not np.array_equal(a, b)


def test_clipping_and_bandwidth_ignore_seed() -> None:
    """These operators are parameter-only; seed is recorded but unused."""
    wave = _tone()
    for corruption in ("clipping", "bandwidth"):
        a, rec_a = apply_damage(wave, 16000, DamageConfig(corruption, "medium", 7, "tone"))
        b, rec_b = apply_damage(wave, 16000, DamageConfig(corruption, "medium", 8, "tone"))
        np.testing.assert_array_equal(a, b)
        assert rec_a.parameters == rec_b.parameters
        assert rec_a.seed != rec_b.seed


def test_severity_changes_additive_noise_power() -> None:
    wave = _tone()
    residual = {}
    for sev in SEVERITIES:
        damaged, rec = apply_damage(
            wave, 16000, DamageConfig("additive_noise", sev, 7, "tone")
        )
        residual[sev] = float(np.mean((damaged - wave) ** 2))
        assert rec.parameters["snr_db"] == PRESETS["additive_noise"][sev]["snr_db"]
    assert residual["severe"] > residual["medium"] > residual["mild"]


def test_record_is_enough_to_regenerate() -> None:
    wave = _tone()
    first, record = apply_damage(
        wave, 16000, DamageConfig("dropout", "medium", 11, "utt_42")
    )
    replay, _ = apply_damage(
        wave,
        record.sample_rate,
        DamageConfig(record.corruption, record.severity, record.seed, record.source_id),
    )
    np.testing.assert_array_equal(first, replay)
    assert record.source_id == "utt_42"
    assert record.package_version
