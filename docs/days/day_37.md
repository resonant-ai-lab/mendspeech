# Day 37: Build a robust fine tuning dataset

> **Week 6 • Day 2 of 7**  
> **Navigation:** [← Day 36](day_36.md) | [Week 6 Plan](../Week_6_MendSpeech_Daily_Plan.md) | [Master Index](../INDEX.md) | [Day 38 →](day_38.md)

---

### Compute Target
`Local CPU`

---

### 1. Learn
- Train, validation, test separation.
- Speaker leakage.
- Synthetic corruption sampling.
- Balanced severity distribution.

---

### 2. Build in MendSpeech
- Create manifests that pair clean transcripts with corrupted audio.
- Keep a speaker separated test set frozen.

---

### 3. Experiment and Measure
- Audit duplicate and speaker leakage.

---

### 4. Required Output Artifacts
- `data/train_manifest.jsonl`
- `data/val_manifest.jsonl`
- `data/test_manifest.jsonl`
- `reports/data_audit.md`

---

### 5. Completion Check
> **Definition of Done for Day 37:**  
> The evaluation set cannot accidentally appear in training through clean or corrupted
duplicates.

---

### 6. Study Method & Protocol
25 minutes focused reading. 65 minutes implementation or controlled experiment. 20 minutes research
notebook. 10 minutes commit and explain the result aloud. When debugging is incomplete, continue the
same task in the next session instead of pretending the day is finished.

---

### 7. References & Resources
- NVIDIA NeMo ASR training documentation
- RNNT primary references
- Calibration and reliability diagram references
