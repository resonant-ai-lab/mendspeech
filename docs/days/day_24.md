# Day 24: Pretrained FastConformer baseline

> **Week 4 • Day 3 of 7**  
> **Navigation:** [← Day 23](day_23.md) | [Week 4 Plan](../Week_4_MendSpeech_Daily_Plan.md) | [Master Index](../INDEX.md) | [Day 25 →](day_25.md)

---

### Compute Target
`Modal L4`

---

### 1. Learn
- Model checkpoint loading.
- Tokenizer and decoder configuration.
- Batch versus single utterance inference.

---

### 2. Build in MendSpeech
- Run a current NeMo FastConformer checkpoint on your clean and damaged sets.
- Record model revision and all inference settings.

---

### 3. Experiment and Measure
- Benchmark WER, latency, and GPU memory by damage type.

---

### 4. Required Output Artifacts
- `src/asr/fastconformer_runner.py`
- `results/day24_fastconformer_baseline.csv`
- `configs/model_baseline.yaml`

---

### 5. Completion Check
> **Definition of Done for Day 24:**  
> You have a reproducible baseline with model, data, hardware, and settings fixed.

---

### 6. Study Method & Protocol
25 minutes focused reading. 65 minutes implementation or controlled experiment. 20 minutes research
notebook. 10 minutes commit and explain the result aloud. When debugging is incomplete, continue the
same task in the next session instead of pretending the day is finished.

---

### 7. References & Resources
- FastConformer primary paper
- NVIDIA NeMo FastConformer model documentation
