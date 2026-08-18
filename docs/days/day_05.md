# Day 05: Objective audio measurements

> **Week 1 • Day 5 of 7**  
> **Navigation:** [← Day 04](day_04.md) | [Week 1 Plan](../Week_1_MendSpeech_Daily_Plan.md) | [Master Index](../INDEX.md) | [Day 06 →](day_06.md)

---

### Compute Target
`Local CPU`

---

### 1. Learn
- RMS and peak level.
- Simple SNR calculation when the clean reference is known.
- Spectral distance intuition.
- Why perceptual speech quality is not fully captured by one scalar metric.

---

### 2. Build in MendSpeech
- Add baseline metrics for clean versus corrupted pairs.
- Store results in a tidy CSV schema with clip id, corruption, severity, seed, and measurements.

---

### 3. Experiment and Measure
- Run all corruption levels on at least ten **labeled** clips from
  `data/benchmark/` (or `data/benchmark/` plus `data/clean_manifest.csv` if
  those rows have transcripts). If fewer than ten labeled clips exist, finish
  the corpus first — do not invent metrics on five unlabeled files.
- Look for cases where a metric disagrees with your listening judgment.

---

### 4. Required Output Artifacts
- `src/metrics/audio_metrics.py`
- `results/week1_damage_metrics.csv`
- `docs/metric_limitations.md`

---

### 5. Completion Check
> **Definition of Done for Day 05:**  
> You can explain what each metric says and what it fails to say.

---

### 6. Study Method & Protocol
25 minutes focused reading. 65 minutes implementation or controlled experiment. 20 minutes research
notebook. 10 minutes commit and explain the result aloud. When debugging is incomplete, continue the
same task in the next session instead of pretending the day is finished.

---

### 7. References & Resources
- PyTorch and TorchAudio audio processing documentation
- A practical digital signal processing reference for STFT and filterbanks
