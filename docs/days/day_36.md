# Day 36: Training pipeline anatomy

> **Week 6 • Day 1 of 7**  
> **Navigation:** [← Day 35](day_35.md) | [Week 6 Plan](../Week_6_MendSpeech_Daily_Plan.md) | [Master Index](../INDEX.md) | [Day 37 →](day_37.md)

---

### Compute Target
`Modal L4`

---

### 1. Learn
- Manifest format.
- Batching variable duration audio.
- Loss curves.
- Learning rate.
- Validation split.
- Checkpointing.

---

### 2. Build in MendSpeech
- Create a tiny reproducible training configuration.
- Run a short smoke training job and verify loss decreases.

---

### 3. Experiment and Measure
- Deliberately use a bad learning rate and record the failure signature.

---

### 4. Required Output Artifacts
- `configs/train_smoke.yaml`
- `results/day36_training_smoke.csv`
- `docs/training_debug_notes.md`

---

### 5. Completion Check
> **Definition of Done for Day 36:**  
> You can diagnose whether a run is learning, diverging, or overfitting from basic
evidence.

---

### 6. Study Method & Protocol
25 minutes focused reading. 65 minutes implementation or controlled experiment. 20 minutes research
notebook. 10 minutes commit and explain the result aloud. When debugging is incomplete, continue the
same task in the next session instead of pretending the day is finished.

---

### 7. References & Resources
- NVIDIA NeMo ASR training documentation
- RNNT primary references
- Calibration and reliability diagram references
