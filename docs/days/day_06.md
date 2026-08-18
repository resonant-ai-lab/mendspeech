# Day 06: Build the first MendSpeech audio console

> **Week 1 • Day 6 of 7**  
> **Navigation:** [← Day 05](day_05.md) | [Week 1 Plan](../Week_1_MendSpeech_Daily_Plan.md) | [Master Index](../INDEX.md) | [Day 07 →](day_07.md)

---

### Compute Target
`Local CPU`

---

### 1. Learn
- Audio playback in a lightweight interface.
- Waveform and spectrogram synchronization.
- Before and after comparison design.

---

### 2. Build in MendSpeech
- Build a local page or notebook dashboard with clean and damaged playback.
- Add corruption controls and immediately regenerate the damaged clip.
- Display waveform, spectrogram, and basic measurements.

---

### 3. Experiment and Measure
- Test with three speakers and several corruption types.
- Write down usability problems that would block later live debugging.

---

### 4. Required Output Artifacts
- `app/audio_lab.py`
- `results/week1_audio_console.png`

---

### 5. Completion Check
> **Definition of Done for Day 06:**  
> Another person can open the tool, damage an utterance, and understand the visual
change without reading your code.

---

### 6. Study Method & Protocol
25 minutes focused reading. 65 minutes implementation or controlled experiment. 20 minutes research
notebook. 10 minutes commit and explain the result aloud. When debugging is incomplete, continue the
same task in the next session instead of pretending the day is finished.

---

### 7. References & Resources
- PyTorch and TorchAudio audio processing documentation
- A practical digital signal processing reference for STFT and filterbanks
