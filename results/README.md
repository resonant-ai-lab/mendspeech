# Results Index

Measured artifacts produced by the daily sessions. Day numbers refer to the
plans in [`docs/days/`](../docs/days/) — the experiment registry for this
project. Result files follow the `dayNN_<what>.<ext>` naming convention.

| Day | Artifact | Finding |
| :--- | :--- | :--- |
| 01 | `day01_resampling_comparison_table.csv` | Downsampling to 8/16/24/48 kHz preserves RMS level (−18.5 dB across all rates) but halves bandwidth each step — everything above the Nyquist frequency is gone for good. |
| 01 | `day01_sampling_rate_spectrum_comparison.png` | Visual proof of the table: spectra at each sample rate truncate at their Nyquist frequency; speech formant energy survives at 16 kHz, so 16 kHz is the project's working rate. |
| 02 | `day02_stft_parameter_grid.png` | STFT tradeoff measured on one utterance: 16 ms windows resolve plosive timing but blur harmonics; 128 ms windows resolve harmonics but smear onsets. Hop changes sampling density only, not resolution. Speech standard: 25 ms window / 10 ms hop at 16 kHz (n_fft=400, hop=160). |
| 03 | `day03_mel_bins_comparison.png` | Mel bin count sweep on one 6 s utterance: 40/80/128 bands → 93.9/187.8/300.5 KB per feature matrix, visual detail grows but 128 bands at n_fft=400 leave top filters with zero linear-bin coverage (torchaudio warning) — 80 bands is the supported ASR standard. Log-Mel shape contract: n_mels fixed, frames scale with duration (601 frames @ 6.00 s vs 651 @ 6.50 s). |
| 04 | `day04_determinism.csv` | Same seed (7) reproduces an identical medium-noise waveform; seed 8 changes the realization while SNR stays 10 dB. Clipping and bandwidth ignore the seed (they are parameter-only) and still record it. |
| 04 | `day04_severity_grid.png` | One labeled LibriSpeech sentence, seed 7: mild / medium / severe for noise, clipping, bandwidth, dropout, and reverberation. Length and 16 kHz rate stay fixed. |
| 05 | `week1_damage_metrics.csv` | 150 rows: 10 clips × 5 corruptions × 3 severities. Additive noise SNR matches presets exactly (20/10/0 dB). Reverberation produces negative SNR (-8 to -3 dB) despite sounding natural at mild severity — SNR is misleading for correlated distortions. Clipping mild can be a no-op when peak < threshold. Bandwidth loss yields low SNR even at mild severity while speech remains intelligible. See docs/metric_limitations.md. |
| 06 | `week1_audio_console.png` | Gradio console for side-by-side clean/damaged playback with waveform, spectrogram, and seed-aware measurements. Desktop comparison columns remain paired, while the layout collapses to one column on narrow screens. |

| 07 | `day07_recreation.png` | Blank-notebook recreation: log-Mel (80 bins, 400/160) scales with duration (1496 frames @ 14.95 s) and additive_noise medium seed 7 reproduces SNR 10.00 dB deterministically — validates clean→corruption→feature path is teachable. |

## Naming rules

- Result and notebook files carry the day prefix (`dayNN_<what>.<ext>`).
- Source and test modules use functional names (`src/audio/stft.py`) — no day counts in permanent code.
- Audio, checkpoints, and run logs are gitignored; only manifests, tables, figures, and notes are tracked.
