# Day 29: Offline versus streaming ASR

> **Week 5 • Day 1 of 7**  
> **Navigation:** [← Day 28](day_28.md) | [Week 5 Plan](../Week_5_MendSpeech_Daily_Plan.md) | [Master Index](../INDEX.md) | [Day 30 →](day_30.md)

---

### Compute Target
`Modal L4`

---

### 1. Learn
- Audio chunks.
- Algorithmic latency.
- Partial hypotheses.
- Endpointing and finalization.

---

### 2. Build in MendSpeech
- Create a chunk simulator that feeds audio incrementally.
- Log when each chunk becomes available and when text changes.

---

### 3. Experiment and Measure
- Compare offline transcript with naive chunk by chunk transcription.

---

### 4. Required Output Artifacts
- `src/streaming/chunker.py`
- `results/day29_offline_vs_naive.csv`

---

### 5. Completion Check
> **Definition of Done for Day 29:**  
> You can explain why naive chunking creates boundary errors and redundant compute.

---

### 6. Study Method & Protocol
25 minutes focused reading. 65 minutes implementation or controlled experiment. 20 minutes research
notebook. 10 minutes commit and explain the result aloud. When debugging is incomplete, continue the
same task in the next session instead of pretending the day is finished.

---

### 7. References & Resources
- Stateful or cache aware Conformer primary material
- NVIDIA NeMo streaming ASR documentation and examples
