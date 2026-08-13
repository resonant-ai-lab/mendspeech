# Week 4: FastConformer and Efficient Encoder Behavior

> **Days 22 to 28**  
> **Navigation:** [← Week 3](Week_3_MendSpeech_Daily_Plan.md) | [Master Index](INDEX.md) | [Master Roadmap](MendSpeech_8_Week_Master_Roadmap.md) | [Week 5 →](Week_5_MendSpeech_Daily_Plan.md)

---

> [!IMPORTANT]
> **Week Milestone:**  
> Measure why FastConformer is efficient and freeze a reproducible baseline.

---

## Week Map

| Day | Focus | Minimum Evidence / Artifact | Compute | Daily Link |
| :--- | :--- | :--- | :--- | :--- |
| **Day 22** | Why FastConformer exists | You can explain FastConformer as a set of concrete efficiency choices, not just a
faster model name. | `Local CPU` | [Open Day 22](days/day_22.md) |
| **Day 23** | Temporal subsampling experiment | You can quantify how subsampling changes sequence length and downstream
attention cost. | `Modal L4 useful` | [Open Day 23](days/day_23.md) |
| **Day 24** | Pretrained FastConformer baseline | You have a reproducible baseline with model, data, hardware, and settings fixed. | `Modal L4` | [Open Day 24](days/day_24.md) |
| **Day 25** | Context and attention limits | You can explain exactly why future context creates algorithmic latency. | `Modal L4` | [Open Day 25](days/day_25.md) |
| **Day 26** | Efficiency benchmark harness | Repeated runs produce stable enough numbers to support comparisons. | `Modal L4` | [Open Day 26](days/day_26.md) |
| **Day 27** | FastConformer failure casebook | You can name at least three repeatable failure patterns and propose a testable
reason for each. | `Modal L4` | [Open Day 27](days/day_27.md) |
| **Day 28** | Week 4 integration | MendSpeech now has a measured, inspectable FastConformer recognition core. | `Modal L4` | [Open Day 28](days/day_28.md) |

---

## Reference Spine
- Rekesh et al., FastConformer with Linearly Scalable Attention for Efficient Speech Recognition\nNVIDIA NeMo FastConformer documentation and model cards\nPyTorch profiler and benchmark documentation

---

## Daily Detailed Operating Plans

### DAY 22: Why FastConformer exists
- **Compute:** `Local CPU`
- **Dedicated Daily File:** [`docs/days/day_22.md`](days/day_22.md)

#### Learn
- Sequence length as an attention cost driver.
- Subsampling before expensive encoder blocks.
- Depthwise separable convolution.
- Local and limited context attention.

#### Build in MendSpeech
- Read the FastConformer paper with a comparison checklist.
- Write a diagram showing what changes relative to Conformer.

#### Experiment and Measure
- Estimate attention matrix size before and after aggressive temporal subsampling.

#### Required Output
- `docs/day22_fastconformer_notes.md`
- `results/day22_compute_estimates.csv`

#### Completion Check
> You can explain FastConformer as a set of concrete efficiency choices, not just a
faster model name.

---

### DAY 23: Temporal subsampling experiment
- **Compute:** `Modal L4 useful`
- **Dedicated Daily File:** [`docs/days/day_23.md`](days/day_23.md)

#### Learn
- Convolutional subsampling.
- Temporal resolution.
- Information loss versus compute reduction.

#### Build in MendSpeech
- Implement a small subsampling front end or isolate one from a framework.
- Track frames per second before and after each stage.

#### Experiment and Measure
- Compare 2x, 4x, and 8x temporal reduction on tensor length, runtime, and rough output behavior.

#### Required Output
- `src/models/subsampling.py`
- `results/day23_subsampling.csv`

#### Completion Check
> You can quantify how subsampling changes sequence length and downstream
attention cost.

---

### DAY 24: Pretrained FastConformer baseline
- **Compute:** `Modal L4`
- **Dedicated Daily File:** [`docs/days/day_24.md`](days/day_24.md)

#### Learn
- Model checkpoint loading.
- Tokenizer and decoder configuration.
- Batch versus single utterance inference.

#### Build in MendSpeech
- Run a current NeMo FastConformer checkpoint on your clean and damaged sets.
- Record model revision and all inference settings.

#### Experiment and Measure
- Benchmark WER, latency, and GPU memory by damage type.

#### Required Output
- `src/asr/fastconformer_runner.py`
- `results/day24_fastconformer_baseline.csv`
- `configs/model_baseline.yaml`

#### Completion Check
> You have a reproducible baseline with model, data, hardware, and settings fixed.

---

### DAY 25: Context and attention limits
- **Compute:** `Modal L4`
- **Dedicated Daily File:** [`docs/days/day_25.md`](days/day_25.md)

#### Learn
- Full context attention.
- Limited context attention.
- Left and right context.
- Accuracy versus latency intuition.

#### Build in MendSpeech
- Inspect context settings in the model configuration.
- Create a visual timeline explaining visible past and future context.

#### Experiment and Measure
- If supported, compare at least two context settings on the same subset.

#### Required Output
- `docs/day25_context_timeline.md`
- `results/day25_context_compare.csv`

#### Completion Check
> You can explain exactly why future context creates algorithmic latency.

---

### DAY 26: Efficiency benchmark harness
- **Compute:** `Modal L4`
- **Dedicated Daily File:** [`docs/days/day_26.md`](days/day_26.md)

#### Learn
- Warmup runs.
- Synchronized GPU timing.
- Median and percentile latency.
- Real time factor.
- Peak memory.

#### Build in MendSpeech
- Create one benchmark function used by every later experiment.
- Log environment and model metadata automatically.

#### Experiment and Measure
- Run repeated inference and calculate variance.
- Detect and discard obviously invalid cold start comparisons.

#### Required Output
- `src/bench/benchmark_asr.py`
- `src/bench/environment.py`
- `results/day26_repeatability.csv`

#### Completion Check
> Repeated runs produce stable enough numbers to support comparisons.

---

### DAY 27: FastConformer failure casebook
- **Compute:** `Modal L4`
- **Dedicated Daily File:** [`docs/days/day_27.md`](days/day_27.md)

#### Learn
- Error slicing by corruption type and severity.
- Short versus long utterance effects.
- Confidence versus error.

#### Build in MendSpeech
- Build a casebook of at least fifteen interesting failures.
- Link each case to audio, transcript, confidence, and damage metadata.

#### Experiment and Measure
- Look for systematic error patterns rather than isolated anecdotes.

#### Required Output
- `results/fastconformer_failure_casebook.md`

#### Completion Check
> You can name at least three repeatable failure patterns and propose a testable
reason for each.

---

### DAY 28: Week 4 integration
- **Compute:** `Modal L4`
- **Dedicated Daily File:** [`docs/days/day_28.md`](days/day_28.md)

#### Learn
- Review efficiency choices and baseline results.

#### Build in MendSpeech
- Replace the generic ASR runner in MendSpeech with the reproducible FastConformer path.
- Expose latency, RTF, WER when reference text exists, and GPU memory in the research console.

#### Experiment and Measure
- Run the same ten reference clips through the full Week 2 uncertainty policy using FastConformer.

#### Required Output
- `app/mendspeech_v1_fastconformer.py`
- `reports/week4_fastconformer.md`

#### Completion Check
> MendSpeech now has a measured, inspectable FastConformer recognition core.

---
