"""SpeechDamageBench: deterministic, seed-controlled speech damage.

Another project can `pip install` this package and regenerate the same
damaged waveform from a manifest row (corruption, severity, seed, source).
"""

from speechdamagebench.audio_damage import (
    CORRUPTIONS,
    DamageConfig,
    DamageRecord,
    apply_damage,
    load_mono,
    save_mono,
)
from speechdamagebench.presets import PACKAGE_VERSION, resolve_params

__all__ = [
    "CORRUPTIONS",
    "DamageConfig",
    "DamageRecord",
    "PACKAGE_VERSION",
    "apply_damage",
    "load_mono",
    "resolve_params",
    "save_mono",
]
