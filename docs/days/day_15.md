# Day 15: Attention for speech sequences

> **Week 3 • Day 1 of 7**  
> **Navigation:** [← Day 14](day_14.md) | [Week 3 Plan](../Week_3_MendSpeech_Daily_Plan.md) | [Master Index](../INDEX.md) | [Day 16 →](day_16.md)

---

### Compute Target
`Local CPU, L4 optional for scaling`

---

### 1. Learn
- Query, key, value projections.
- Scaled dot product attention.
- Attention masks.
- Sequence length cost.

---

### 2. Build in MendSpeech
- Implement single head attention and then multi head attention in PyTorch.
- Add shape assertions and gradient tests.

---

### 3. Experiment and Measure
- Change sequence length and measure forward time and memory.

---

### 4. Required Output Artifacts
- `src/models/attention.py`
- `tests/test_attention.py`
- `results/day15_attention_scaling.csv`

---

### 5. Completion Check
> **Definition of Done for Day 15:**  
> You can derive every major tensor shape and explain quadratic sequence cost.

---

### 6. Study Method & Protocol
25 minutes focused reading. 65 minutes implementation or controlled experiment. 20 minutes research
notebook. 10 minutes commit and explain the result aloud. When debugging is incomplete, continue the
same task in the next session instead of pretending the day is finished.

---

### 7. References & Resources
- Conformer primary paper
- A mature Conformer implementation such as NVIDIA NeMo
