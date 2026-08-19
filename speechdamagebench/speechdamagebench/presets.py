"""Versioned mild / medium / severe recipes for each corruption family.

Units:
    snr_db: signal-to-noise ratio in decibels (higher = quieter noise)
    threshold: hard-clip amplitude in linear full-scale units in [0, 1]
    cutoff_hz: low-pass cutoff in Hertz (content stays at the original sample rate)
    span_ms: dropout length in milliseconds
    n_spans: number of dropout holes
    rt60_s: approximate reverberation time in seconds (60 dB decay)
"""

from typing import Dict

PACKAGE_VERSION = "0.1.0"

# corruption -> severity -> parameter dict
PRESETS: Dict[str, Dict[str, Dict[str, float]]] = {
    "additive_noise": {
        "mild": {"snr_db": 20.0},
        "medium": {"snr_db": 10.0},
        "severe": {"snr_db": 0.0},
    },
    "clipping": {
        "mild": {"threshold": 0.60},
        "medium": {"threshold": 0.35},
        "severe": {"threshold": 0.15},
    },
    "bandwidth": {
        "mild": {"cutoff_hz": 4000.0},
        "medium": {"cutoff_hz": 3400.0},
        "severe": {"cutoff_hz": 2000.0},
    },
    "dropout": {
        "mild": {"span_ms": 50.0, "n_spans": 1.0},
        "medium": {"span_ms": 100.0, "n_spans": 2.0},
        "severe": {"span_ms": 250.0, "n_spans": 3.0},
    },
    "reverberation": {
        "mild": {"rt60_s": 0.15},
        "medium": {"rt60_s": 0.40},
        "severe": {"rt60_s": 0.80},
    },
}

SEVERITIES = ("mild", "medium", "severe")


def resolve_params(
    corruption: str,
    severity: str,
    overrides: Dict[str, float] | None = None,
) -> Dict[str, float]:
    """Return a copy of the preset parameters, optionally overridden.

    Args:
        corruption: One of the keys in ``PRESETS``.
        severity: ``mild``, ``medium``, or ``severe``.
        overrides: Optional parameter replacements. Unknown keys are rejected.

    Returns:
        Parameter dict used for this apply() call.

    Raises:
        KeyError: Unknown corruption or severity.
        ValueError: Override names a parameter the preset does not define.
    """
    if corruption not in PRESETS:
        raise KeyError(
            f"unknown corruption {corruption!r}; choose from {sorted(PRESETS)}"
        )
    if severity not in PRESETS[corruption]:
        raise KeyError(
            f"unknown severity {severity!r}; choose from {list(SEVERITIES)}"
        )
    params = dict(PRESETS[corruption][severity])
    if overrides:
        unknown = set(overrides) - set(params)
        if unknown:
            raise ValueError(
                f"overrides {sorted(unknown)} are not parameters of {corruption}"
            )
        params.update(overrides)
    return params
