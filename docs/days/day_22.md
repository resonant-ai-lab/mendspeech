# Day 22: Why FastConformer exists

> **Week 4 • Day 1 of 7**  
> **Navigation:** [← Day 21](day_21.md) | [Week 4 Plan](../Week_4_MendSpeech_Daily_Plan.md) | [Master Index](../INDEX.md) | [Day 23 →](day_23.md)

> **v1 STATUS: LEARN-ONLY — merged into [Day 23](day_23.md).** Paper notes and compute estimates only; no separate session.

---

### Compute Target
`Local CPU`

---

### 1. Learn
- Sequence length as an attention cost driver.
- Subsampling before expensive encoder blocks.
- Depthwise separable convolution.
- Local and limited context attention.

---

### 2. Build in MendSpeech
- Read the FastConformer paper with a comparison checklist.
- Write a diagram showing what changes relative to Conformer.

---

### 3. Experiment and Measure
- Estimate attention matrix size before and after aggressive temporal subsampling.

---

### 4. Required Output Artifacts
- `docs/day22_fastconformer_notes.md`
- `results/day22_compute_estimates.csv`

---

### 5. Completion Check
> **Definition of Done for Day 22:**  
> You can explain FastConformer as a set of concrete efficiency choices, not just a
faster model name.

---

### 6. Study Method & Protocol
25 minutes focused reading. 65 minutes implementation or controlled experiment. 20 minutes research
notebook. 10 minutes commit and explain the result aloud. When debugging is incomplete, continue the
same task in the next session instead of pretending the day is finished.

---

### 7. References & Resources
- FastConformer primary paper
- NVIDIA NeMo FastConformer model documentation
