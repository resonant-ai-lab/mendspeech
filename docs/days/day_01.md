# Day 01: Waveforms, sampling, and the MendSpeech baseline

> **Week 1 • Day 1 of 7**  
> **Navigation:** [← Index](../INDEX.md) | [Week 1 Plan](../Week_1_MendSpeech_Daily_Plan.md) | [Master Index](../INDEX.md) | [Day 02 →](day_02.md)

---

### Compute Target
`Local CPU`

> **Still open after Day 01:** `data/benchmark/` and the `transcript` column
> were required here and were not finished. Do not re-run Day 01. Carry that
> labeled-corpus work into [Day 04](day_04.md). Use relative paths only.

---

### 1. Learn
- Waveform amplitude and time axes.
- Sampling rate, Nyquist intuition, bit depth, mono versus stereo.
- Why speech systems often standardize to 16 kHz.
- Duration, peak amplitude, RMS energy, and clipping.

---

### 2. Build in MendSpeech
- Create the repository and a minimal audio loader.
- Record or collect five clean speech clips with consent.
- Acquire a reference-transcripted subset (e.g., a LibriSpeech dev-clean slice) into `data/benchmark/`; the frozen benchmark will run on labeled clips, not only waveforms.
- Normalize all clips to a consistent sample rate and mono format.

---

### 3. Experiment and Measure
- Compare 8 kHz, 16 kHz, 24 kHz, and 48 kHz versions by listening and plotting.
- Measure duration, RMS energy, and file size for each version.

---

### 4. Required Output Artifacts
- `notebooks/day01_waveform.ipynb`
- `data/clean_manifest.csv` (now includes a `transcript` column)
- `data/benchmark/` (reference-transcripted corpus slice)
- `docs/audio_baseline_notes.md`

---

### 5. Completion Check
> **Definition of Done for Day 01:**  
> You can explain what is lost when sample rate is reduced and can reproduce the
same preprocessing from code.

---

### 6. Study Method & Protocol
25 minutes focused reading. 65 minutes implementation or controlled experiment. 20 minutes research
notebook. 10 minutes commit and explain the result aloud. When debugging is incomplete, continue the
same task in the next session instead of pretending the day is finished.

---

### 7. References & Resources
- PyTorch and TorchAudio audio processing documentation
- A practical digital signal processing reference for STFT and filterbanks
