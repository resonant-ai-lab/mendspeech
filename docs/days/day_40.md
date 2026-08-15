# Day 40: RNN-T concepts and quantization lab

> **Week 6 • Day 5 of 7**  
> **Navigation:** [← Day 39](day_39.md) | [Week 6 Plan](../Week_6_MendSpeech_Daily_Plan.md) | [Master Index](../INDEX.md) | [Day 41 →](day_41.md)

---

### Compute Target
`Modal L4`

---

### 1. Learn
- Encoder.
- Prediction network.
- Joint network.
- Blank handling.
- Streaming emission behavior.
- Difference from CTC independence.
- Post-training quantization: dynamic vs static INT8, and why static needs a calibration set.
- What quantization can and cannot preserve in an ASR model (logit sharpness, confidence behavior).

---

### 2. Build in MendSpeech
- Export the Day 38 fine-tuned ASR checkpoint through a quantization-ready path (NeMo export or ONNX).
- Apply INT8 post-training quantization using a held-out calibration slice of the frozen benchmark.
- Sanity-check transcriptions on a few test clips before measuring anything.

---

### 3. Experiment and Measure
- Measure WER, real-time factor, and peak memory before and after quantization on the frozen benchmark subset.
- Record whether confidence scores shift after quantization (this feeds directly into Day 41 calibration).

---

### 4. Required Output Artifacts
- `docs/rnnt_walkthrough.md` (theory summary from the Learn block)
- `docs/day40_quantization_notes.md`
- `results/day40_quantization_tradeoffs.csv`

---

### 5. Completion Check
> **Definition of Done for Day 40:**  
> You can explain RNN-T streaming behavior precisely (not only that it is better for streaming), and state the measured accuracy, latency, and memory cost of INT8 quantization on your model.

---

### 6. Study Method & Protocol
25 minutes focused reading. 65 minutes implementation or controlled experiment. 20 minutes research
notebook. 10 minutes commit and explain the result aloud. When debugging is incomplete, continue the
same task in the next session instead of pretending the day is finished.

---

### 7. References & Resources
- NVIDIA NeMo ASR training documentation
- RNN-T primary references
- ONNX Runtime quantization documentation or torch.ao quantization overview
