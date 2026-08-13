# Day 25: Context and attention limits

> **Week 4 • Day 4 of 7**  
> **Navigation:** [← Day 24](day_24.md) | [Week 4 Plan](../Week_4_MendSpeech_Daily_Plan.md) | [Master Index](../INDEX.md) | [Day 26 →](day_26.md)

---

### Compute Target
`Modal L4`

---

### 1. Learn
- Full context attention.
- Limited context attention.
- Left and right context.
- Accuracy versus latency intuition.

---

### 2. Build in MendSpeech
- Inspect context settings in the model configuration.
- Create a visual timeline explaining visible past and future context.

---

### 3. Experiment and Measure
- If supported, compare at least two context settings on the same subset.

---

### 4. Required Output Artifacts
- `docs/day25_context_timeline.md`
- `results/day25_context_compare.csv`

---

### 5. Completion Check
> **Definition of Done for Day 25:**  
> You can explain exactly why future context creates algorithmic latency.

---

### 6. Study Method & Protocol
25 minutes focused reading. 65 minutes implementation or controlled experiment. 20 minutes research
notebook. 10 minutes commit and explain the result aloud. When debugging is incomplete, continue the
same task in the next session instead of pretending the day is finished.

---

### 7. References & Resources
- FastConformer primary paper
- NVIDIA NeMo FastConformer model documentation
