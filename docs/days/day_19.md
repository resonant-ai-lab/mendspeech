# Day 19: Build a tiny Conformer encoder

> **Week 3 • Day 5 of 7**  
> **Navigation:** [← Day 18](day_18.md) | [Week 3 Plan](../Week_3_MendSpeech_Daily_Plan.md) | [Master Index](../INDEX.md) | [Day 20 →](day_20.md)

---

### Compute Target
`Local CPU, L4 optional`

---

### 1. Learn
- Input projection.
- Stacked blocks.
- Mask propagation.
- Temporal dimensions.

---

### 2. Build in MendSpeech
- Build a small encoder around your blocks.
- Connect log Mel features to the encoder.

---

### 3. Experiment and Measure
- Track tensor shape through every layer on real speech.
- Profile increasing depth.

---

### 4. Required Output Artifacts
- `src/models/tiny_conformer.py`
- `results/day19_shape_trace.md`

---

### 5. Completion Check
> **Definition of Done for Day 19:**  
> A real log Mel tensor can pass through your encoder and produce valid gradients.

---

### 6. Study Method & Protocol
25 minutes focused reading. 65 minutes implementation or controlled experiment. 20 minutes research
notebook. 10 minutes commit and explain the result aloud. When debugging is incomplete, continue the
same task in the next session instead of pretending the day is finished.

---

### 7. References & Resources
- Conformer primary paper
- A mature Conformer implementation such as NVIDIA NeMo
