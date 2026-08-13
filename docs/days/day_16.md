# Day 16: Conformer convolution module

> **Week 3 • Day 2 of 7**  
> **Navigation:** [← Day 15](day_15.md) | [Week 3 Plan](../Week_3_MendSpeech_Daily_Plan.md) | [Master Index](../INDEX.md) | [Day 17 →](day_17.md)

---

### Compute Target
`Local CPU`

---

### 1. Learn
- Pointwise convolution.
- GLU gating.
- Depthwise convolution.
- Batch normalization and activation.
- Why local patterns matter in speech.

---

### 2. Build in MendSpeech
- Implement a Conformer style convolution module.
- Test causality assumptions and receptive field.

---

### 3. Experiment and Measure
- Feed synthetic impulses and inspect how local information spreads.

---

### 4. Required Output Artifacts
- `src/models/conformer_conv.py`
- `tests/test_conformer_conv.py`
- `notebooks/day16_receptive_field.ipynb`

---

### 5. Completion Check
> **Definition of Done for Day 16:**  
> You can explain why depthwise convolution is computationally attractive and what
local context it captures.

---

### 6. Study Method & Protocol
25 minutes focused reading. 65 minutes implementation or controlled experiment. 20 minutes research
notebook. 10 minutes commit and explain the result aloud. When debugging is incomplete, continue the
same task in the next session instead of pretending the day is finished.

---

### 7. References & Resources
- Conformer primary paper
- A mature Conformer implementation such as NVIDIA NeMo
