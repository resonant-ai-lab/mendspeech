# Day 18: Assemble one Conformer block

> **Week 3 • Day 4 of 7**  
> **Navigation:** [← Day 17](day_17.md) | [Week 3 Plan](../Week_3_MendSpeech_Daily_Plan.md) | [Master Index](../INDEX.md) | [Day 19 →](day_19.md)

---

### Compute Target
`Local CPU`

---

### 1. Learn
- Macaron structure.
- Layer normalization placement.
- Attention plus convolution interaction.

---

### 2. Build in MendSpeech
- Assemble feed forward, attention, convolution, second feed forward, and final normalization.
- Match expected input and output shapes.

---

### 3. Experiment and Measure
- Run forward and backward tests on several sequence lengths.
- Intentionally remove one residual path and compare training stability on a toy task.

---

### 4. Required Output Artifacts
- `src/models/conformer_block.py`
- `tests/test_conformer_block.py`
- `docs/conformer_block_walkthrough.md`

---

### 5. Completion Check
> **Definition of Done for Day 18:**  
> You can point to every operation and say why it exists.

---

### 6. Study Method & Protocol
25 minutes focused reading. 65 minutes implementation or controlled experiment. 20 minutes research
notebook. 10 minutes commit and explain the result aloud. When debugging is incomplete, continue the
same task in the next session instead of pretending the day is finished.

---

### 7. References & Resources
- Conformer primary paper
- A mature Conformer implementation such as NVIDIA NeMo
