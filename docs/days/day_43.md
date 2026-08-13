# Day 43: TTS system anatomy

> **Week 7 • Day 1 of 7**  
> **Navigation:** [← Day 42](day_42.md) | [Week 7 Plan](../Week_7_MendSpeech_Daily_Plan.md) | [Master Index](../INDEX.md) | [Day 44 →](day_44.md)

---

### Compute Target
`Modal L4`

---

### 1. Learn
- Text or phoneme representation.
- Acoustic model.
- Mel spectrogram or latent representation.
- Vocoder.
- Speaker conditioning.
- Prosody.

---

### 2. Build in MendSpeech
- Run a pretrained TTS system on controlled text.
- Save generated waveform and intermediate representations if exposed.

---

### 3. Experiment and Measure
- Compare several sentences with punctuation and pacing changes.

---

### 4. Required Output Artifacts
- `src/tts/baseline.py`
- `results/day43_tts_samples/`
- `docs/tts_pipeline.md`

---

### 5. Completion Check
> **Definition of Done for Day 43:**  
> You can explain how text becomes waveform and where speaker identity can enter.

---

### 6. Study Method & Protocol
25 minutes focused reading. 65 minutes implementation or controlled experiment. 20 minutes research
notebook. 10 minutes commit and explain the result aloud. When debugging is incomplete, continue the
same task in the next session instead of pretending the day is finished.

---

### 7. References & Resources
- FastSpeech 2 paper
- HiFi GAN paper
- VITS paper
- DSP references for energy matching and equal power crossfades
