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

## Naming rules

- Result and notebook files carry the day prefix (`dayNN_<what>.<ext>`).
- Source and test modules use functional names (`src/audio/stft.py`) — no day counts in permanent code.
- Audio, checkpoints, and run logs are gitignored; only manifests, tables, figures, and notes are tracked.
