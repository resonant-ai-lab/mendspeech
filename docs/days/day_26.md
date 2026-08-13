# Day 26: Efficiency benchmark harness

> **Week 4 • Day 5 of 7**  
> **Navigation:** [← Day 25](day_25.md) | [Week 4 Plan](../Week_4_MendSpeech_Daily_Plan.md) | [Master Index](../INDEX.md) | [Day 27 →](day_27.md)

---

### Compute Target
`Modal L4`

---

### 1. Learn
- Warmup runs.
- Synchronized GPU timing.
- Median and percentile latency.
- Real time factor.
- Peak memory.

---

### 2. Build in MendSpeech
- Create one benchmark function used by every later experiment.
- Log environment and model metadata automatically.

---

### 3. Experiment and Measure
- Run repeated inference and calculate variance.
- Detect and discard obviously invalid cold start comparisons.

---

### 4. Required Output Artifacts
- `src/bench/benchmark_asr.py`
- `src/bench/environment.py`
- `results/day26_repeatability.csv`

---

### 5. Completion Check
> **Definition of Done for Day 26:**  
> Repeated runs produce stable enough numbers to support comparisons.

---

### 6. Study Method & Protocol
25 minutes focused reading. 65 minutes implementation or controlled experiment. 20 minutes research
notebook. 10 minutes commit and explain the result aloud. When debugging is incomplete, continue the
same task in the next session instead of pretending the day is finished.

---

### 7. References & Resources
- FastConformer primary paper
- NVIDIA NeMo FastConformer model documentation
