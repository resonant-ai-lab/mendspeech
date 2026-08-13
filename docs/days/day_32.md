# Day 32: Lookahead ablation

> **Week 5 • Day 4 of 7**  
> **Navigation:** [← Day 31](day_31.md) | [Week 5 Plan](../Week_5_MendSpeech_Daily_Plan.md) | [Master Index](../INDEX.md) | [Day 33 →](day_33.md)

---

### Compute Target
`Modal L4`

---

### 1. Learn
- Right context.
- Lookahead.
- Commit delay.
- WER and latency as competing objectives.

---

### 2. Build in MendSpeech
- Run several supported lookahead settings with everything else fixed.
- Store per utterance and aggregate metrics.

---

### 3. Experiment and Measure
- Plot WER versus latency and identify dominated operating points.

---

### 4. Required Output Artifacts
- `experiments/lookahead_ablation.py`
- `results/day32_lookahead.csv`
- `results/day32_pareto.png`

---

### 5. Completion Check
> **Definition of Done for Day 32:**  
> You can defend a Balanced operating point using data rather than preference.

---

### 6. Study Method & Protocol
25 minutes focused reading. 65 minutes implementation or controlled experiment. 20 minutes research
notebook. 10 minutes commit and explain the result aloud. When debugging is incomplete, continue the
same task in the next session instead of pretending the day is finished.

---

### 7. References & Resources
- Stateful or cache aware Conformer primary material
- NVIDIA NeMo streaming ASR documentation and examples
