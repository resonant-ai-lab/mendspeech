# Day 31: Cache aware streaming internals

> **Week 5 • Day 3 of 7**  
> **Navigation:** [← Day 30](day_30.md) | [Week 5 Plan](../Week_5_MendSpeech_Daily_Plan.md) | [Master Index](../INDEX.md) | [Day 32 →](day_32.md)

---

### Compute Target
`Modal L4`

---

### 1. Learn
- Cached activations.
- Past context state.
- Streaming masks.
- Right context and lookahead.

---

### 2. Build in MendSpeech
- Use NeMo cache aware streaming inference on a supported FastConformer checkpoint.
- Log cache related configuration and chunk boundaries.
- If cache-aware inference is unsupported for the chosen checkpoint, document the limitation and fall back to buffered streaming; the buffered vs cache comparison still runs.

---

### 3. Experiment and Measure
- Compare buffered and cache aware inference on the same audio and same hardware.

---

### 4. Required Output Artifacts
- `src/streaming/cache_aware_runner.py`
- `results/day31_buffered_vs_cache.csv`

---

### 5. Completion Check
> **Definition of Done for Day 31:**  
> You can explain what is cached, what is recomputed, and why cache aware inference
can be more efficient.

---

### 6. Study Method & Protocol
25 minutes focused reading. 65 minutes implementation or controlled experiment. 20 minutes research
notebook. 10 minutes commit and explain the result aloud. When debugging is incomplete, continue the
same task in the next session instead of pretending the day is finished.

---

### 7. References & Resources
- Stateful or cache aware Conformer primary material
- NVIDIA NeMo streaming ASR documentation and examples
