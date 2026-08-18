# Day 07: Review, explain, and freeze Week 1

> **Week 1 • Day 7 of 7**  
> **Navigation:** [← Day 06](day_06.md) | [Week 1 Plan](../Week_1_MendSpeech_Daily_Plan.md) | [Master Index](../INDEX.md) | [Day 08 →](day_08.md)

---

### Compute Target
`Local CPU`

---

### 1. Learn
- Review waveform, STFT, Mel features, SNR, clipping, dropouts, and reverberation.

---

### 2. Build in MendSpeech
- Clean repository structure.
- **Freeze only.** Do not start collecting a new corpus on this day. The
  labeled set must already exist from Days 04–05. Freeze SpeechDamageBench
  v0.1 severity presets and a benchmark set of **≥30 utterances across ≥5
  speakers with reference transcripts** (lab scale is typically ~5 speakers;
  ≥5 is the floor, not a race to dozens), written as speaker-separated
  train/val/test splits in one manifest.
- Tag the benchmark package schema and add a minimal usage example independent of MendSpeech.

---

### 3. Experiment and Measure
- From a blank notebook, recreate one corruption and one log Mel plot without copying previous cells.

---

### 4. Required Output Artifacts
- `reports/week1_audio_foundations.md`
- `data/benchmark_manifest.csv` (relative paths, `transcript`, `speaker_id`, and a `split` column: train/val/test)
- `speechdamagebench/README.md`
- `speechdamagebench/VERSION`

---

### 5. Completion Check
> **Definition of Done for Day 07:**  
> You can teach the complete path from clean waveform to controlled corruption and
feature tensor.

---

### 6. Study Method & Protocol
25 minutes focused reading. 65 minutes implementation or controlled experiment. 20 minutes research
notebook. 10 minutes commit and explain the result aloud. When debugging is incomplete, continue the
same task in the next session instead of pretending the day is finished.

---

### 7. References & Resources
- PyTorch and TorchAudio audio processing documentation
- A practical digital signal processing reference for STFT and filterbanks
