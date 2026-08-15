# Week 6: Robustness, Fine Tuning, RNNT, and Calibration

> **Days 36 to 42**  
> **Navigation:** [← Week 5](Week_5_MendSpeech_Daily_Plan.md) | [Master Index](INDEX.md) | [Master Roadmap](MendSpeech_8_Week_Master_Roadmap.md) | [Week 7 →](Week_7_MendSpeech_Daily_Plan.md)

---

> [!IMPORTANT]
> **Week Milestone:**  
> Adapt the recognizer to damaged speech while learning training and calibration discipline.

---

## Week Map

| Day | Focus | Minimum Evidence / Artifact | Compute | Daily Link |
| :--- | :--- | :--- | :--- | :--- |
| **Day 36** | Training pipeline anatomy | You can diagnose whether a run is learning, diverging, or overfitting from basic
evidence. | `Modal L4` | [Open Day 36](days/day_36.md) |
| **Day 37** | Build a robust fine tuning dataset | The evaluation set cannot accidentally appear in training through clean or corrupted
duplicates. | `Local CPU` | [Open Day 37](days/day_37.md) |
| **Day 38** | Fine tune for damaged speech robustness | You can state exactly what improved, what did not, and whether clean speech
regressed. | `Modal L4, consider L40S only if
memory blocks the planned experiment` | [Open Day 38](days/day_38.md) |
| **Day 39** | SpecAugment and augmentation ablation | You can separate the effect of augmentation from the effect of extra training time. | `Modal L4` | [Open Day 39](days/day_39.md) |
| **Day 40** | RNN-T concepts and quantization lab | You can explain RNN-T streaming behavior precisely (not only that it is better for streaming), and state the measured accuracy, latency, and memory cost of INT8 quantization on your model. | `Modal L4` | [Open Day 40](days/day_40.md) |
| **Day 41** | Confidence calibration for repair decisions | Repair thresholds are now justified from held out evidence rather than guessed. | `Modal L4 for logits, local CPU for
analysis` | [Open Day 41](days/day_41.md) |
| **Day 42** | Week 6 robustness milestone | MendSpeech can demonstrate measured robustness gains or clearly document a
negative result. | `Modal L4` | [Open Day 42](days/day_42.md) |

---

## Reference Spine
- NVIDIA NeMo ASR training documentation\nRNNT primary references\nCalibration and reliability diagram references

---

## Daily Detailed Operating Plans

### DAY 36: Training pipeline anatomy
- **Compute:** `Modal L4`
- **Dedicated Daily File:** [`docs/days/day_36.md`](days/day_36.md)

#### Learn
- Manifest format.
- Batching variable duration audio.
- Loss curves.
- Learning rate.
- Validation split.
- Checkpointing.

#### Build in MendSpeech
- Create a tiny reproducible training configuration.
- Run a short smoke training job and verify loss decreases.

#### Experiment and Measure
- Deliberately use a bad learning rate and record the failure signature.

#### Required Output
- `configs/train_smoke.yaml`
- `results/day36_training_smoke.csv`
- `docs/training_debug_notes.md`

#### Completion Check
> You can diagnose whether a run is learning, diverging, or overfitting from basic
evidence.

---

### DAY 37: Build a robust fine tuning dataset
- **Compute:** `Local CPU`
- **Dedicated Daily File:** [`docs/days/day_37.md`](days/day_37.md)

#### Learn
- Train, validation, test separation.
- Speaker leakage.
- Synthetic corruption sampling.
- Balanced severity distribution.

#### Build in MendSpeech
- Create manifests that pair clean transcripts with corrupted audio.
- Keep a speaker separated test set frozen.

#### Experiment and Measure
- Audit duplicate and speaker leakage.

#### Required Output
- `data/train_manifest.jsonl`
- `data/val_manifest.jsonl`
- `data/test_manifest.jsonl`
- `reports/data_audit.md`

#### Completion Check
> The evaluation set cannot accidentally appear in training through clean or corrupted
duplicates.

---

### DAY 38: Fine tune for damaged speech robustness
- **Compute:** `Modal L4, consider L40S only if
memory blocks the planned experiment`
- **Dedicated Daily File:** [`docs/days/day_38.md`](days/day_38.md)

#### Learn
- Transfer learning.
- Frozen versus trainable layers.
- Mixed precision.
- Gradient accumulation.

#### Build in MendSpeech
- Fine tune a manageable FastConformer or compatible ASR checkpoint on the robustness dataset.
- Save model, config, and training logs.

#### Experiment and Measure
- Compare base and adapted model on the frozen test set.

#### Required Output
- `training/finetune.py`
- `checkpoints/week6_best/`
- `results/day38_base_vs_adapted.csv`

#### Completion Check
> You can state exactly what improved, what did not, and whether clean speech
regressed.

---

### DAY 39: SpecAugment and augmentation ablation
- **Compute:** `Modal L4`
- **Dedicated Daily File:** [`docs/days/day_39.md`](days/day_39.md)

#### Learn
- Time masking.
- Frequency masking.
- Data augmentation as invariance training.

#### Build in MendSpeech
- Add one augmentation intervention to a controlled short run.

#### Experiment and Measure
- Compare no augmentation versus selected augmentation with the same seed and training budget.

#### Required Output
- `experiments/specaugment_ablation.py`
- `results/day39_augmentation.csv`

#### Completion Check
> You can separate the effect of augmentation from the effect of extra training time.

---

### DAY 40: RNN-T concepts and quantization lab
- **Compute:** `Modal L4`
- **Dedicated Daily File:** [`docs/days/day_40.md`](days/day_40.md)

#### Learn
- Encoder.
- Prediction network.
- Joint network.
- Blank handling.
- Streaming emission behavior.
- Difference from CTC independence.
- Post-training quantization: dynamic vs static INT8, and why static needs a calibration set.
- What quantization can and cannot preserve in an ASR model (logit sharpness, confidence behavior).

#### Build in MendSpeech
- Export the Day 38 fine-tuned ASR checkpoint through a quantization-ready path (NeMo export or ONNX).
- Apply INT8 post-training quantization using a held-out calibration slice of the frozen benchmark.

#### Experiment and Measure
- Measure WER, real-time factor, and peak memory before and after quantization on the frozen benchmark subset.

#### Required Output
- `docs/rnnt_walkthrough.md`
- `docs/day40_quantization_notes.md`
- `results/day40_quantization_tradeoffs.csv`

#### Completion Check
> You can explain RNN-T streaming behavior precisely (not only that it is better for streaming), and state the measured accuracy, latency, and memory cost of INT8 quantization on your model.

---

### DAY 41: Confidence calibration for repair decisions
- **Compute:** `Modal L4 for logits, local CPU for
analysis`
- **Dedicated Daily File:** [`docs/days/day_41.md`](days/day_41.md)

#### Learn
- Reliability diagrams.
- Expected calibration error intuition.
- Threshold selection from validation data.

#### Build in MendSpeech
- Build a simple calibration analysis for confidence versus correctness.
- Choose policy thresholds on validation, not test.

#### Experiment and Measure
- Compare raw and calibrated confidence if a simple method is feasible.

#### Required Output
- `src/asr/calibration.py`
- `results/day41_reliability.png`
- `configs/repair_modes_calibrated.yaml`

#### Completion Check
> Repair thresholds are now justified from held out evidence rather than guessed.

---

### DAY 42: Week 6 robustness milestone
- **Compute:** `Modal L4`
- **Dedicated Daily File:** [`docs/days/day_42.md`](days/day_42.md)

#### Learn
- Review fine tuning, augmentation, RNNT, and calibration.

#### Build in MendSpeech
- Switch between base and adapted recognizer in the research console.
- Show clean WER, damaged WER, confidence calibration, and repair percentage.

#### Experiment and Measure
- Run one fixed benchmark suite and freeze results for Week 8 comparisons.

#### Required Output
- `app/mendspeech_v3_robust.py`
- `results/week6_frozen_baseline.csv`
- `reports/week6_training.md`

#### Completion Check
> MendSpeech can demonstrate measured robustness gains or clearly document a
negative result.

---
