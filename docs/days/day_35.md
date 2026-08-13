# Day 35: Week 5 live streaming milestone

> **Week 5 • Day 7 of 7**  
> **Navigation:** [← Day 34](day_34.md) | [Week 5 Plan](../Week_5_MendSpeech_Daily_Plan.md) | [Master Index](../INDEX.md) | [Day 36 →](day_36.md)

---

### Compute Target
`Modal L4`

---

### 1. Learn
- Review buffered streaming, cache aware inference, lookahead, cache failures, and adaptive context.

---

### 2. Build in MendSpeech
- Connect microphone or simulated live audio to the streaming recognizer.
- Show partial text, confidence timeline, current context mode, and latency.

---

### 3. Experiment and Measure
- Record a short demo with clean and damaged speech.
- Document remaining technical limitations honestly.

---

### 4. Required Output Artifacts
- `app/mendspeech_v2_streaming.py`
- `demos/week5_streaming_demo.mp4`
- `reports/week5_streaming.md`

---

### 5. Completion Check
> **Definition of Done for Day 35:**  
> A person can speak and watch MendSpeech transcribe incrementally while exposing
the state that drives repair decisions.

---

### 6. Study Method & Protocol
25 minutes focused reading. 65 minutes implementation or controlled experiment. 20 minutes research
notebook. 10 minutes commit and explain the result aloud. When debugging is incomplete, continue the
same task in the next session instead of pretending the day is finished.

---

### 7. References & Resources
- Stateful or cache aware Conformer primary material
- NVIDIA NeMo streaming ASR documentation and examples   Week 6: Robustness, Fine Tuning, RNNT, and Calibration Adapt the recognizer to damaged speech while learning training and calibration discipline.  Day  Focus  Minimum evidence  Compute  Day 36  Training pipeline anatomy
- Deliberately use a bad learning rate and record the failure signature.  Modal L4  Day 37  Build a robust fine tuning dataset
- Audit duplicate and speaker leakage.  Local CPU  Day 38  Fine tune for damaged speech robustness
- Compare base and adapted model on the frozen test set.  Modal L4, consider L40S only if memory blocks the planned experiment  Day 39  SpecAugment and augmentation ablation
- Compare no augmentation versus selected augmentation with the same seed and training budget.  Modal L4  Day 40  RNNT and streaming decoding
- Compare CTC and transducer outputs on selected difficult clips.  Modal L4  Day 41  Confidence calibration for repair decisions
- Compare raw and calibrated confidence if a simple method is feasible.  Modal L4 for logits, local CPU for analysis  Day 42  Week 6 robustness milestone
- Run one fixed benchmark suite and freeze results for Week 8 comparisons.  Modal L4
