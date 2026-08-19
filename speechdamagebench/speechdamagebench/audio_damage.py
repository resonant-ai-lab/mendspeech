"""Seed-controlled speech damage operators.

Every operator takes an explicit integer seed. The same
(config, seed, waveform) triple must produce a bit-identical float32
result. Changing only the seed changes the realization; configured
parameters (SNR, threshold, cutoff, span length) stay fixed.

Waveforms are mono float32 numpy arrays. Length and sample rate are
preserved (bandwidth limits the *content*, not the file rate).
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Callable, Dict, Optional, Tuple, Union

import numpy as np
import soundfile as sf
from scipy import signal
from numpy.typing import NDArray

from speechdamagebench.presets import PACKAGE_VERSION, resolve_params

Array = NDArray[np.float32]

CORRUPTIONS = (
    "additive_noise",
    "clipping",
    "bandwidth",
    "dropout",
    "reverberation",
)


@dataclass
class DamageConfig:
    """How to damage one utterance.

    Attributes:
        corruption: Operator name (see ``CORRUPTIONS``).
        severity: ``mild``, ``medium``, or ``severe``.
        seed: Integer seed for this realization. Required; never omitted.
        source_id: Clean-source identifier written into the output record.
        param_overrides: Optional replacements for preset values.
    """

    corruption: str
    severity: str
    seed: int
    source_id: str
    param_overrides: Optional[Dict[str, float]] = None


@dataclass
class DamageRecord:
    """Manifest row for one damaged clip. Enough to regenerate it.

    Attributes:
        corruption: Operator name.
        severity: Preset name.
        seed: Integer seed used.
        source_id: Clean source identifier.
        parameters: Numeric parameters actually applied (after overrides).
        package_version: SpeechDamageBench version string.
        sample_rate: Sample rate in Hz.
        num_samples: Output length in samples.
    """

    corruption: str
    severity: str
    seed: int
    source_id: str
    parameters: Dict[str, float]
    package_version: str
    sample_rate: int
    num_samples: int

    def to_dict(self) -> Dict[str, Union[str, int, float, Dict[str, float]]]:
        """JSON-serializable copy of the record."""
        return asdict(self)


def load_mono(path: Union[str, Path], target_sr: Optional[int] = 16000) -> Tuple[Array, int]:
    """Load a wav as mono float32, optionally resampling with polyphase.

    Args:
        path: Audio file path.
        target_sr: Target sample rate in Hz. ``None`` keeps the file rate.

    Returns:
        ``(waveform, sample_rate)``. Waveform shape is ``(num_samples,)``.
    """
    data, sr = sf.read(str(path), dtype="float32", always_2d=True)
    mono = data.mean(axis=1).astype(np.float32)
    if target_sr is not None and sr != target_sr:
        gcd = np.gcd(sr, target_sr)
        mono = signal.resample_poly(mono, target_sr // gcd, sr // gcd).astype(np.float32)
        sr = target_sr
    return mono, int(sr)


def save_mono(path: Union[str, Path], waveform: Array, sample_rate: int) -> None:
    """Write a mono float32 waveform as 16-bit PCM WAV.

    Args:
        path: Destination path. Parent directories are created.
        waveform: Mono samples.
        sample_rate: Sample rate in Hz.
    """
    dest = Path(path)
    dest.parent.mkdir(parents=True, exist_ok=True)
    sf.write(str(dest), np.asarray(waveform, dtype=np.float32), sample_rate, subtype="PCM_16")


def _rng(seed: int) -> np.random.Generator:
    return np.random.default_rng(int(seed))


def _as_mono(wave: np.ndarray) -> Array:
    arr = np.asarray(wave, dtype=np.float32)
    if arr.ndim == 2:
        arr = arr.mean(axis=0 if arr.shape[0] < arr.shape[1] else 1)
    if arr.ndim != 1:
        raise ValueError(f"expected mono waveform, got shape {arr.shape}")
    return np.ascontiguousarray(arr, dtype=np.float32)


def additive_noise(wave: Array, sample_rate: int, rng: np.random.Generator, snr_db: float) -> Array:
    """Add white Gaussian noise at a target SNR.

    Args:
        wave: Clean mono samples.
        sample_rate: Unused; accepted so every operator has the same signature.
        rng: Seeded generator (chooses the noise *samples*).
        snr_db: Target SNR in decibels.

    Returns:
        Damaged waveform, same length.
    """
    del sample_rate
    signal_power = float(np.mean(wave.astype(np.float64) ** 2))
    if signal_power <= 1e-12:
        return wave.copy()
    noise = rng.standard_normal(wave.shape[0]).astype(np.float64)
    noise_power = float(np.mean(noise ** 2))
    scale = np.sqrt(signal_power / (noise_power * 10.0 ** (snr_db / 10.0)))
    out = wave.astype(np.float64) + scale * noise
    return np.clip(out, -1.0, 1.0).astype(np.float32)


def clipping(wave: Array, sample_rate: int, rng: np.random.Generator, threshold: float) -> Array:
    """Hard-clip at ±threshold (linear full scale).

    Clipping is deterministic given the threshold; ``rng`` is unused but
    accepted so the operator table stays uniform.

    Args:
        wave: Clean mono samples.
        sample_rate: Unused.
        rng: Unused.
        threshold: Clip level in (0, 1].

    Returns:
        Clipped waveform, same length.
    """
    del sample_rate, rng
    thr = float(threshold)
    if thr <= 0.0:
        raise ValueError("clipping threshold must be > 0")
    return np.clip(wave, -thr, thr).astype(np.float32)


def bandwidth(wave: Array, sample_rate: int, rng: np.random.Generator, cutoff_hz: float) -> Array:
    """Zero-phase Butterworth low-pass. File rate stays ``sample_rate``.

    Args:
        wave: Clean mono samples.
        sample_rate: Sample rate in Hz.
        rng: Unused (filter is deterministic).
        cutoff_hz: Cutoff in Hertz. Must be below Nyquist.

    Returns:
        Band-limited waveform at the original sample rate and length.
    """
    del rng
    nyquist = sample_rate / 2.0
    if not 0.0 < cutoff_hz < nyquist:
        raise ValueError(f"cutoff_hz={cutoff_hz} must be in (0, {nyquist})")
    sos = signal.butter(8, cutoff_hz / nyquist, btype="low", output="sos")
    filtered = signal.sosfiltfilt(sos, wave.astype(np.float64))
    return np.asarray(filtered, dtype=np.float32)


def dropout(
    wave: Array,
    sample_rate: int,
    rng: np.random.Generator,
    span_ms: float,
    n_spans: float,
) -> Array:
    """Zero one or more holes of length ``span_ms``.

    The seed chooses *where* the holes start. Span length and count come
    from the preset and do not change when only the seed changes.

    Args:
        wave: Clean mono samples.
        sample_rate: Sample rate in Hz.
        rng: Seeded generator (start indices).
        span_ms: Hole length in milliseconds.
        n_spans: Number of holes (stored as float in presets; cast to int).

    Returns:
        Waveform with zeros in the chosen spans, same length.
    """
    out = wave.copy()
    n = int(n_spans)
    span = max(1, int(round(span_ms * 1e-3 * sample_rate)))
    if span >= wave.shape[0] or n <= 0:
        return out
    max_start = wave.shape[0] - span
    # Sample without replacement when possible so holes do not stack.
    starts = rng.choice(max_start + 1, size=min(n, max_start + 1), replace=False)
    for start in starts:
        out[int(start) : int(start) + span] = 0.0
    return out


def reverberation(wave: Array, sample_rate: int, rng: np.random.Generator, rt60_s: float) -> Array:
    """Convolve with a seeded exponentially decaying noise impulse response.

    The output is trimmed to the original length so stitching later does
    not have to guess a tail.

    Args:
        wave: Clean mono samples.
        sample_rate: Sample rate in Hz.
        rng: Seeded generator (IR samples).
        rt60_s: Time in seconds for the IR envelope to fall 60 dB.

    Returns:
        Reverberated waveform, same length as ``wave``.
    """
    if rt60_s <= 0.0:
        raise ValueError("rt60_s must be > 0")
    ir_len = max(8, int(round(rt60_s * sample_rate)))
    # 60 dB decay over rt60_s: envelope = 10**(-3 * t / rt60)
    t = np.arange(ir_len, dtype=np.float64) / float(sample_rate)
    envelope = np.power(10.0, -3.0 * t / rt60_s)
    ir = rng.standard_normal(ir_len).astype(np.float64) * envelope
    ir[0] = 1.0  # keep a dry peak so energy does not vanish
    wet = signal.fftconvolve(wave.astype(np.float64), ir, mode="full")[: wave.shape[0]]
    peak = np.max(np.abs(wet))
    if peak > 1.0:
        wet = wet / peak
    return wet.astype(np.float32)


_OPERATORS: Dict[str, Callable[..., Array]] = {
    "additive_noise": additive_noise,
    "clipping": clipping,
    "bandwidth": bandwidth,
    "dropout": dropout,
    "reverberation": reverberation,
}


def apply_damage(
    waveform: np.ndarray,
    sample_rate: int,
    config: DamageConfig,
) -> Tuple[Array, DamageRecord]:
    """Apply one corruption and return the waveform plus a regenerable record.

    Args:
        waveform: Mono samples (any float dtype; converted to float32).
        sample_rate: Sample rate in Hz.
        config: Corruption, severity, seed, and source id.

    Returns:
        ``(damaged_waveform, record)``. Length equals the input length.
    """
    if config.corruption not in _OPERATORS:
        raise KeyError(
            f"unknown corruption {config.corruption!r}; choose from {list(_OPERATORS)}"
        )
    wave = _as_mono(waveform)
    params = resolve_params(config.corruption, config.severity, config.param_overrides)
    rng = _rng(config.seed)
    damaged = _OPERATORS[config.corruption](wave, sample_rate, rng, **params)
    if damaged.shape != wave.shape:
        raise RuntimeError(
            f"{config.corruption} changed shape {wave.shape} -> {damaged.shape}"
        )
    record = DamageRecord(
        corruption=config.corruption,
        severity=config.severity,
        seed=int(config.seed),
        source_id=config.source_id,
        parameters=params,
        package_version=PACKAGE_VERSION,
        sample_rate=int(sample_rate),
        num_samples=int(damaged.shape[0]),
    )
    return damaged, record
