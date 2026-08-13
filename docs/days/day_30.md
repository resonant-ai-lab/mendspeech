# Day 30: Buffered streaming

> **Week 5 • Day 2 of 7**  
> **Navigation:** [← Day 29](day_29.md) | [Week 5 Plan](../Week_5_MendSpeech_Daily_Plan.md) | [Master Index](../INDEX.md) | [Day 31 →](day_31.md)

---

### Compute Target
`Modal L4`

---

### 1. Learn
- Overlapping windows.
- Buffer size.
- Stride.
- Repeated computation.

---

### 2. Build in MendSpeech
- Implement or run buffered streaming with configurable overlap.
- Measure how much audio is recomputed.

---

### 3. Experiment and Measure
- Sweep buffer and stride settings.
- Measure WER and latency tradeoffs.

---

### 4. Required Output Artifacts
- `src/streaming/buffered.py`
- `results/day30_buffered_sweep.csv`

---

### 5. Completion Check
> **Definition of Done for Day 30:**  
> You can quantify the compute waste caused by overlapping history.

---

### 6. Study Method & Protocol
25 minutes focused reading. 65 minutes implementation or controlled experiment. 20 minutes research
notebook. 10 minutes commit and explain the result aloud. When debugging is incomplete, continue the
same task in the next session instead of pretending the day is finished.

---

### 7. References & Resources
- Stateful or cache aware Conformer primary material
- NVIDIA NeMo streaming ASR documentation and examples
