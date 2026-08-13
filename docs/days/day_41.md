# Day 41: Confidence calibration for repair decisions

> **Week 6 • Day 6 of 7**  
> **Navigation:** [← Day 40](day_40.md) | [Week 6 Plan](../Week_6_MendSpeech_Daily_Plan.md) | [Master Index](../INDEX.md) | [Day 42 →](day_42.md)

---

### Compute Target
`Modal L4 for logits, local CPU for
analysis`

---

### 1. Learn
- Reliability diagrams.
- Expected calibration error intuition.
- Threshold selection from validation data.

---

### 2. Build in MendSpeech
- Build a simple calibration analysis for confidence versus correctness.
- Choose policy thresholds on validation, not test.

---

### 3. Experiment and Measure
- Compare raw and calibrated confidence if a simple method is feasible.

---

### 4. Required Output Artifacts
- `src/asr/calibration.py`
- `results/day41_reliability.png`
- `configs/repair_modes_calibrated.yaml`

---

### 5. Completion Check
> **Definition of Done for Day 41:**  
> Repair thresholds are now justified from held out evidence rather than guessed.

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
