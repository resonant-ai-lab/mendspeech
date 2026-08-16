# Day 02: Fourier intuition and STFT

> **Week 1 • Day 2 of 7**  
> **Navigation:** [← Day 01](day_01.md) | [Week 1 Plan](../Week_1_MendSpeech_Daily_Plan.md) | [Master Index](../INDEX.md) | [Day 03 →](day_03.md)

---

### Compute Target
`Local CPU`

---

### 1. Learn
- Frequency, phase, harmonics, and spectral energy.
- Fourier transform intuition without memorizing derivations.
- STFT frames, window length, hop length, overlap.
- Tradeoff between time resolution and frequency resolution.

---

### 2. Build in MendSpeech
- Implement STFT visualization with PyTorch or TorchAudio.
- Plot the same utterance with several window and hop settings.

---

### 3. Experiment and Measure
- Hold audio constant and change one STFT setting at a time.
- Write what phonetic or transient detail becomes easier or harder to see.

---

### 4. Required Output Artifacts
- `notebooks/day02_stft.ipynb`
- `results/day02_stft_parameter_grid.png`

---

### 5. Completion Check
> **Definition of Done for Day 02:**  
> You can choose a reasonable frame and hop configuration and explain why.

---

### 6. Study Method & Protocol
25 minutes focused reading. 65 minutes implementation or controlled experiment. 20 minutes research
notebook. 10 minutes commit and explain the result aloud. When debugging is incomplete, continue the
same task in the next session instead of pretending the day is finished.

---

### 7. References & Resources
- PyTorch and TorchAudio audio processing documentation
- A practical digital signal processing reference for STFT and filterbanks
