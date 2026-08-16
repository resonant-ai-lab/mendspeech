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
from .stft import (
    DEFAULT_HOP_16K,
    DEFAULT_N_FFT_16K,
    compute_stft,
    dominant_frequency,
    spectrogram_db,
    stft_resolutions,
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
    "DEFAULT_HOP_16K",
    "DEFAULT_N_FFT_16K",
    "compute_stft",
    "dominant_frequency",
    "spectrogram_db",
    "stft_resolutions",
]
