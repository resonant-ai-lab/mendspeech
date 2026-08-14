"""Audio processing, feature extraction, and ingestion module for MendSpeech."""

from .loader import (
    AudioMetadata,
    load_audio,
    save_audio,
    resample_audio,
    compute_rms,
    rms_to_db,
    compute_peak,
    peak_to_dbfs,
    compute_clipping_ratio,
    normalize_audio,
    compute_audio_metadata,
)

__all__ = [
    "AudioMetadata",
    "load_audio",
    "save_audio",
    "resample_audio",
    "compute_rms",
    "rms_to_db",
    "compute_peak",
    "peak_to_dbfs",
    "compute_clipping_ratio",
    "normalize_audio",
    "compute_audio_metadata",
]
