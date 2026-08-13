# Day 03: Mel scale and log Mel features

> **Week 1 • Day 3 of 7**  
> **Navigation:** [← Day 02](day_02.md) | [Week 1 Plan](../Week_1_MendSpeech_Daily_Plan.md) | [Master Index](../INDEX.md) | [Day 04 →](day_04.md)

---

### Compute Target
`Local CPU`

---

### 1. Learn
- Human frequency perception and the Mel scale.
- Mel filterbanks and log compression.
- Number of Mel bins and dynamic range.
- Normalization of acoustic features.

---

### 2. Build in MendSpeech
- Implement or inspect a log Mel feature pipeline.
- Build a function that returns features plus metadata needed for reproducibility.

---

### 3. Experiment and Measure
- Change Mel bin count and compare visual structure and compute size.
- Verify consistent feature shapes for different utterance lengths.

---

### 4. Required Output Artifacts
- `src/audio/features.py`
- `notebooks/day03_logmel.ipynb`
- `tests/test_features.py`

---

### 5. Completion Check
> **Definition of Done for Day 03:**  
> You can trace waveform to STFT to Mel filterbank to log Mel tensor.

---

### 6. Study Method & Protocol
25 minutes focused reading. 65 minutes implementation or controlled experiment. 20 minutes research
notebook. 10 minutes commit and explain the result aloud. When debugging is incomplete, continue the
same task in the next session instead of pretending the day is finished.

---

### 7. References & Resources
- PyTorch and TorchAudio audio processing documentation
- A practical digital signal processing reference for STFT and filterbanks
