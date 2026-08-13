# Day 34: Adaptive context controller prototype

> **Week 5 • Day 6 of 7**  
> **Navigation:** [← Day 33](day_33.md) | [Week 5 Plan](../Week_5_MendSpeech_Daily_Plan.md) | [Master Index](../INDEX.md) | [Day 35 →](day_35.md)

---

### Compute Target
`Modal L4`

---

### 1. Learn
- Policy driven context selection.
- Confidence smoothing.
- Latency budget.
- Stability versus oscillation.

---

### 2. Build in MendSpeech
- Implement a controller that classifies chunks as easy or uncertain.
- Map states to small or larger supported right context settings, even if the first prototype must simulate switching between runs.

---

### 3. Experiment and Measure
- Compare fixed fast, fixed accurate, and adaptive policies on a controlled subset.

---

### 4. Required Output Artifacts
- `src/controller/adaptive_context.py`
- `results/day34_adaptive_context.csv`

---

### 5. Completion Check
> **Definition of Done for Day 34:**  
> You have a falsifiable first answer to whether uncertainty can guide context spending.

---

### 6. Study Method & Protocol
25 minutes focused reading. 65 minutes implementation or controlled experiment. 20 minutes research
notebook. 10 minutes commit and explain the result aloud. When debugging is incomplete, continue the
same task in the next session instead of pretending the day is finished.

---

### 7. References & Resources
- Stateful or cache aware Conformer primary material
- NVIDIA NeMo streaming ASR documentation and examples
