# Benchmark audio — frozen for Gate 1 (Day 07)

Labeled LibriSpeech `dev-clean` subset frozen for the MendSpeech evaluation.

| Status | Count |
| :--- | :--- |
| Utterances | 30 |
| Speakers | 5 (`spk_1272`, `spk_1462`, `spk_1673`, `spk_1919`, `spk_1988`) |
| Transcripts | yes, relative paths, `transcript` column |
| Splits | speaker-separated: train (1272,1462,1673 → 18 clips), val (1919 → 6), test (1988 → 6) |
| Sample rate | 16 kHz mono |
| Source | `openslr/librispeech dev-clean` via `http://www.openslr.org/resources/12/dev-clean.tar.gz` (extracted 2026-08-31, 16 kHz) |
| Manifests | `data/benchmark_manifest.csv` (canonical, Gate 1 freeze) and `data/benchmark/manifest.csv` (legacy copy, same content) |

Audio files (`*.wav`) are tracked as manifests only for this lab scale (30 clips); full LibriSpeech tarball is not committed. Frozen after Day 07 — do not add speakers or change splits. New experiments vary corruption configs, not the test set.
