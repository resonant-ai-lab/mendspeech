# Day 28: Week 4 integration

> **Week 4 • Day 7 of 7**  
> **Navigation:** [← Day 27](day_27.md) | [Week 4 Plan](../Week_4_MendSpeech_Daily_Plan.md) | [Master Index](../INDEX.md) | [Day 29 →](day_29.md)

---

### Compute Target
`Modal L4`

---

### 1. Learn
- Review efficiency choices and baseline results.

---

### 2. Build in MendSpeech
- Replace the generic ASR runner in MendSpeech with the reproducible FastConformer path.
- Expose latency, RTF, WER when reference text exists, and GPU memory in the research console.

---

### 3. Experiment and Measure
- Run the same ten reference clips through the full Week 2 uncertainty policy using FastConformer.

---

### 4. Required Output Artifacts
- `app/mendspeech_v1_fastconformer.py`
- `reports/week4_fastconformer.md`

---

### 5. Completion Check
> **Definition of Done for Day 28:**  
> MendSpeech now has a measured, inspectable FastConformer recognition core.

---

### 6. Study Method & Protocol
25 minutes focused reading. 65 minutes implementation or controlled experiment. 20 minutes research
notebook. 10 minutes commit and explain the result aloud. When debugging is incomplete, continue the
same task in the next session instead of pretending the day is finished.

---

### 7. References & Resources
- FastConformer primary paper
- NVIDIA NeMo FastConformer model documentation   Week 5: Streaming, Cache Aware Inference, and Adaptive Context Turn the recognizer into a real time system and test uncertainty guided context spending.  Day  Focus  Minimum evidence  Compute  Day 29  Offline versus streaming ASR
- Compare offline transcript with naive chunk by chunk transcription.  Modal L4  Day 30  Buffered streaming
- Sweep buffer and stride settings.
- Measure WER and latency tradeoffs.  Modal L4  Day 31  Cache aware streaming internals
- Compare buffered and cache aware inference on the same audio and same hardware.  Modal L4  Day 32  Lookahead ablation
- Plot WER versus latency and identify dominated operating points.  Modal L4  Day 33  Break the cache on purpose
- Measure WER changes around the reset point.
- Inspect whether errors cluster near boundaries or propagate later.  Modal L4  Day 34  Adaptive context controller prototype
- Compare fixed fast, fixed accurate, and adaptive policies on a controlled subset.  Modal L4  Day 35  Week 5 live streaming milestone
- Record a short demo with clean and damaged speech.
- Document remaining technical limitations honestly.  Modal L4
