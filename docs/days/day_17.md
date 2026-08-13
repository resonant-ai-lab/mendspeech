# Day 17: Macaron feed forward and residual scaling

> **Week 3 • Day 3 of 7**  
> **Navigation:** [← Day 16](day_16.md) | [Week 3 Plan](../Week_3_MendSpeech_Daily_Plan.md) | [Master Index](../INDEX.md) | [Day 18 →](day_18.md)

---

### Compute Target
`Local CPU`

---

### 1. Learn
- Feed forward expansion.
- Swish or SiLU activation.
- Dropout.
- Half step residual weighting in Conformer.

---

### 2. Build in MendSpeech
- Implement the feed forward module and residual wrapper.
- Add numerical tests for shape and gradient flow.

---

### 3. Experiment and Measure
- Compare output statistics with and without residual scaling.

---

### 4. Required Output Artifacts
- `src/models/conformer_ffn.py`
- `tests/test_conformer_ffn.py`

---

### 5. Completion Check
> **Definition of Done for Day 17:**  
> You can explain the ordering of the Conformer block without memorizing a diagram.

---

### 6. Study Method & Protocol
25 minutes focused reading. 65 minutes implementation or controlled experiment. 20 minutes research
notebook. 10 minutes commit and explain the result aloud. When debugging is incomplete, continue the
same task in the next session instead of pretending the day is finished.

---

### 7. References & Resources
- Conformer primary paper
- A mature Conformer implementation such as NVIDIA NeMo
