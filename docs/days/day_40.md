# Day 40: RNNT and streaming decoding

> **Week 6 • Day 5 of 7**  
> **Navigation:** [← Day 39](day_39.md) | [Week 6 Plan](../Week_6_MendSpeech_Daily_Plan.md) | [Master Index](../INDEX.md) | [Day 41 →](day_41.md)

---

### Compute Target
`Modal L4`

---

### 1. Learn
- Encoder.
- Prediction network.
- Joint network.
- Blank handling.
- Streaming emission behavior.
- Difference from CTC independence.

---

### 2. Build in MendSpeech
- Run or inspect a FastConformer transducer checkpoint.
- Trace one decoding step conceptually and document tensor roles.

---

### 3. Experiment and Measure
- Compare CTC and transducer outputs on selected difficult clips.

---

### 4. Required Output Artifacts
- `docs/rnnt_walkthrough.md`
- `results/day40_ctc_vs_rnnt.csv`

---

### 5. Completion Check
> **Definition of Done for Day 40:**  
> You can explain RNNT without saying only that it is better for streaming.

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
