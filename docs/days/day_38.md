# Day 38: Fine tune for damaged speech robustness

> **Week 6 • Day 3 of 7**  
> **Navigation:** [← Day 37](day_37.md) | [Week 6 Plan](../Week_6_MendSpeech_Daily_Plan.md) | [Master Index](../INDEX.md) | [Day 39 →](day_39.md)

---

### Compute Target
`Modal L4, consider L40S only if
memory blocks the planned experiment — never
for latency, RTF, or memory comparisons`

---

### 1. Learn
- Transfer learning.
- Frozen versus trainable layers.
- Mixed precision.
- Gradient accumulation.

---

### 2. Build in MendSpeech
- Fine tune a manageable FastConformer or compatible ASR checkpoint on the robustness dataset.
- Save model, config, and training logs.

---

### 3. Experiment and Measure
- Compare base and adapted model on the frozen test set.

---

### 4. Required Output Artifacts
- `training/finetune.py`
- `checkpoints/week6_best/`
- `results/day38_base_vs_adapted.csv`

---

### 5. Completion Check
> **Definition of Done for Day 38:**  
> You can state exactly what improved, what did not, and whether clean speech
regressed.

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
