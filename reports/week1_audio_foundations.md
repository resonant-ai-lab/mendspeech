# Week 1 Audio Foundations — Clean Waveform to Controlled Corruption and Feature Tensor

> **MendSpeech Day 07 freeze** — Gate 1 review. Teaches the complete path from raw audio → resampling → STFT → log-Mel → deterministic damage → objective measurement → interactive inspection.

---

## 1. From waveform to 16 kHz mono

**What is lost when sample rate is reduced?** Each downsample halves bandwidth at the Nyquist frequency (`sr/2`). RMS energy is preserved (−18.5 dB across 8/16/24/48 kHz) but content above Nyquist is gone forever. Speech is intelligible at 16 kHz; above that we keep only extra sibilance and sensor noise.

**Contract used everywhere:** `src/audio/loader.py` loads any file, converts to mono, resamples to **16,000 Hz** with `torchaudio`, preserves duration and peak/RMS metadata. Every downstream module assumes 16 kHz, mono, float32. Artifact `data/clean_manifest.csv` records `sample_rate, channels, duration_sec, rms_db, peak_dbfs`.

Measured in `results/day01_resampling_comparison_table.csv` and `results/day01_sampling_rate_spectrum_comparison.png`: spectra truncate cleanly at `sr/2`; 16 kHz is the working rate.

---

## 2. STFT — time versus frequency resolution

**Core tradeoff:** window length sets frequency resolution; hop length sets time sampling density. Measured on one 6 s utterance:

- 16 ms window → resolves plosive timing, blurs harmonics
- 128 ms window → resolves harmonic lines, smears onsets
- Hop changes only sampling density, not resolution

Speech standard adopted: **`n_fft=400 (25 ms), hop=160 (10 ms), window=hann` at 16 kHz** — balances transient sharpness and harmonic clarity. Implementation in `src/audio/stft.py`, visualization in `notebooks/day02_stft.ipynb`. Artifact `results/day02_stft_parameter_grid.png`.

**Shape contract:** for `T` samples, frames ≈ `1 + (T − n_fft)/hop`. Verify with gradient test (STFT is differentiable via torch).

---

## 3. Log-Mel — perceptually scaled features

**Path:** waveform → STFT magnitude → Mel filterbank (Slaney, `f_min=0, f_max=8000`) → natural log (+ `log(1e-5)` floor) → tensor `[n_mels, frames]`.

**Measurement:** sweep 40/80/128 Mel bins on one 6 s clip (n_fft=400):

| bins | matrix size | note |
|------|-------------|------|
| 40 | 93.9 KB | coarse, loses detail |
| 80 | 187.8 KB | **supported ASR standard** |
| 128 | 300.5 KB | top filters have zero linear-bin coverage → torchaudio warning |

`n_mels` is fixed; frames scale with duration (601 frames @ 6.00 s vs 651 @ 6.50 s). Metadata in `LogMelMetadata` (`n_fft, hop_length, sample_rate, n_mels, f_min, f_max, log_offset`). Artifact `results/day03_mel_bins_comparison.png`. Code: `src/audio/logmel.py` (`compute_log_mel` returns `Tensor, LogMelMetadata`).

---

## 4. SpeechDamageBench — deterministic damage

**Why standalone?** Another project can `pip install -e ./speechdamagebench` and regenerate the same damaged clip from `(corruption, severity, seed, source_id)` — no MendSpeech import needed.

**Operators (length and sample rate preserved; bandwidth limits content, not file rate):**

| corruption | parameter preset (mild / medium / severe) | seed used? |
|------------|-------------------------------------------|------------|
| `additive_noise` | SNR 20 / 10 / 0 dB | yes |
| `clipping` | threshold 0.85 / 0.60 / 0.35 | no (deterministic gain) |
| `bandwidth` | low-pass cutoff 6000 / 3500 / 2000 Hz | no |
| `dropout` | zero spans 20 ms×2 / 50 ms×4 / 100 ms×6 | yes |
| `reverberation` | RT60 0.3 / 0.6 / 0.9 s | yes (comb seed) |

Severity presets in `speechdamagebench/presets.py`, package version in `speechdamagebench/pyproject.toml` (`0.1.0`, mirrored in `speechdamagebench/VERSION`). Every `DamageRecord` and CLI JSON prints `corruption, severity, seed, source_id, params, package_version`.

**Determinism verified:** `results/day04_determinism.csv` — seed 7 reproduces identical medium-noise waveform; seed 8 changes realization while SNR stays 10 dB. Clipping/bandwidth ignore seed but still record it.

**Artifact:** `speechdamagebench/` nested package with its own `pyproject.toml`, `speechdamagebench/README.md`, and `speechdamagebench/VERSION`. Usage:

```bash
pip install -e ./speechdamagebench
speechdamagebench damage --in clean.wav --out damaged.wav --corruption additive_noise --severity medium --seed 7 --source-id clean_01
```

Corruption grid measured on one labeled sentence at seed 7: `results/day04_severity_grid.png` (mild/medium/severe for all 5 corruptions; length and 16 kHz rate fixed).

---

## 5. Objective measurements — what scalars say and hide

**Pair metrics** (`src/metrics/audio_metrics.py:compute_pair_metrics`) when clean reference is known:

- `clean_rms_db / corrupted_rms_db` and `peak_dbfs` — level preservation
- `snr_db` — `10·log10(P_signal / P_noise)` where `P_noise = P(corrupted−clean)` — trustworthy only for **additive, uncorrelated** distortions
- `log_mel_distance` — L2 on 80-bin log-Mel (`n_fft=400, hop=160`) — captures spectral distortion predictively for ASR

**Measured at scale:** `scripts/run_week1_metrics.py` ran all 5×3 corruptions on **10 labeled benchmark clips** → 150 rows in `results/week1_damage_metrics.csv`.

| finding | detail |
|---------|--------|
| Additive noise SNR matches presets exactly | 20/10/0 dB dialed, 20/10/0 dB measured |
| Reverberation SNR is misleading | −8 to −3 dB despite natural mild reverb — SNR penalizes correlated late energy |
| Clipping mild can be no-op | peak < 0.85 → no samples exceed threshold, SNR → inf, Mel distance ≈ 0 |
| Bandwidth loss yields low SNR even when intelligible | low-pass removes high-frequency energy → large `P_noise` though speech remains understandable |
| All rows carry `clip_id, speaker_id, corruption, severity, seed` | no unseeded randomness |

Limitation note `docs/metric_limitations.md`: single scalars do not capture perceptual quality; Mel distance correlates better with ASR degradation but still misses temporal artifacts.

---

## 6. Audio console — before/after inspection

**Tool:** `app/audio_lab.py` (Gradio, `Local CPU`). Left/right comparison columns stay paired on desktop, collapse to one column on narrow screens. Controls: clip select, corruption, severity, seed → immediately regenerates damaged clip via `SpeechDamageBench.apply_damage`.

**Displays per clip:** clean and damaged playback (`<audio>` 100% width), waveform (matplotlib, synchronized time axes), log-Mel spectrogram (80 bins, 10 ms hop), and `compute_pair_metrics` table (RMS, peak, SNR, Mel distance, seed-aware).

**Why it matters:** live debugging for later ASR/TTS — hear and see what the model will see. Tested with three speakers and several corruptions; usability notes logged during Day 06 (seed stability, column pairing, lazy loading).

Artifact `results/week1_audio_console.png` screenshots the console.

---

## 7. Freeze for Gate 1

**Frozen benchmark:** `data/benchmark_manifest.csv` — **≥30 utterances across ≥5 speakers** with `clip_id, speaker_id, file_path (relative), transcript, sample_rate, source, split`. Speaker-separated splits: no speaker in two splits (e.g., 3 speakers train ≈60%, 1 val ≈20%, 1 test ≈20%). File creation via deterministic download from LibriSpeech `dev-clean` (OpenSLR 12) at 16 kHz; `file_path` is `data/benchmark/<id>.wav`. Once frozen, immutable — new experiments get new corruption configs, not a new test set.

**This freeze** expands the earlier 10-clip single-speaker dummy (`hf-internal-testing/librispeech_asr_dummy`, `spk_1272`) to 30 clips / 5 speakers from real `dev-clean` (downloaded from `http://www.openslr.org/resources/12/dev-clean.tar.gz`, resampled to 16 kHz mono). Previous `data/benchmark/manifest.csv` is superseded by `data/benchmark_manifest.csv` (canonical). `data/benchmark/README.md` updated.

**Package freeze:** `speechdamagebench` v0.1 — severity presets immutable, `VERSION=0.1.0`, independent install verified (`pip install -e ./speechdamagebench` → CLI prints reproducible JSON).

**Blank-notebook recreation (Day 07 Experiment):** from a blank notebook, without copying cells:

1. Load one frozen clip with `src/audio/loader.load_audio(..., target_sr=16000)`, compute log-Mel with `src/audio/logmel.compute_log_mel` (80 bins, 400/160), plot with `matplotlib` — shape `[80, frames]` scales with duration.
2. Apply `additive_noise, medium, seed=7` via `speechdamagebench.audio_damage.apply_damage`, verify SNR ≈ 10 dB with `src/metrics/audio_metrics.compute_pair_metrics`, and A/B playback.

Both succeed deterministically — validates the full path is teachable.

---

## 8. Limitations and next

- Benchmark is still **lab scale (~5 speakers, 30 clips)** — Gate 1 floor, not a claim to generalize. Week 8 caveat applies: do not over-claim from this size.
- Metrics are **reference-based** (need clean) — later ASR uncertainty must work without clean reference.
- Console runs **locally** — later add-on will serve streaming ASR on Modal L4 for tail-latency and backpressure evidence.

**Next is Day 08:** run pretrained ASR on clean vs damaged clips, store transcripts and timing, add Modal L4 entry point, smoke-test direct inpainting baseline.

---

*Generated for Day 07 freeze — deterministic, seed-controlled, Local CPU.*
