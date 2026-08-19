# Benchmark audio (in progress)

Labeled LibriSpeech utterances used to start the frozen evaluation set.
Audio files (`*.wav`) are gitignored; this folder's `manifest.csv` is tracked.

| Status | Count |
| :--- | :--- |
| Utterances | 8 |
| Speakers | 1 (`spk_1272`) |
| Transcripts | yes, relative paths |

Source: `hf-internal-testing/librispeech_asr_dummy` (LibriSpeech `dev-clean` speaker 1272).

**Not frozen.** Day 05 must grow this to ≥10 labeled clips and add speakers
so Day 07 can freeze ≥30 utterances / ≥5 speakers. Do not invent transcripts.
