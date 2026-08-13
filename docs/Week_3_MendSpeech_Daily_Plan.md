# Week 3: Conformer From First Principles

> **Days 15 to 21**  
> **Navigation:** [← Week 2](Week_2_MendSpeech_Daily_Plan.md) | [Master Index](INDEX.md) | [Master Roadmap](MendSpeech_8_Week_Master_Roadmap.md) | [Week 4 →](Week_4_MendSpeech_Daily_Plan.md)

---

> [!IMPORTANT]
> **Week Milestone:**  
> Implement the core encoder pieces so model behavior is not a black box.

---

## Week Map

| Day | Focus | Minimum Evidence / Artifact | Compute | Daily Link |
| :--- | :--- | :--- | :--- | :--- |
| **Day 15** | Attention for speech sequences | You can derive every major tensor shape and explain quadratic sequence cost. | `Local CPU, L4 optional for scaling` | [Open Day 15](days/day_15.md) |
| **Day 16** | Conformer convolution module | You can explain why depthwise convolution is computationally attractive and what
local context it captures. | `Local CPU` | [Open Day 16](days/day_16.md) |
| **Day 17** | Macaron feed forward and residual scaling | You can explain the ordering of the Conformer block without memorizing a diagram. | `Local CPU` | [Open Day 17](days/day_17.md) |
| **Day 18** | Assemble one Conformer block | You can point to every operation and say why it exists. | `Local CPU` | [Open Day 18](days/day_18.md) |
| **Day 19** | Build a tiny Conformer encoder | A real log Mel tensor can pass through your encoder and produce valid gradients. | `Local CPU, L4 optional` | [Open Day 19](days/day_19.md) |
| **Day 20** | Compare your block with a production | You can read production Conformer code and orient yourself without treating it as
magic. | `Local CPU` | [Open Day 20](days/day_20.md) |
| **Day 21** | Week 3 architecture review | You can explain which parts are local, which are global, and which become
problematic for streaming. | `Local CPU` | [Open Day 21](days/day_21.md) |

---

## Reference Spine
- Gulati et al., Conformer: Convolution
- augmented Transformer for Speech Recognition\nAnnotated Transformer and Attention Is All You Need\nA mature open
- source Conformer implementation

---

## Daily Detailed Operating Plans

### DAY 15: Attention for speech sequences
- **Compute:** `Local CPU, L4 optional for scaling`
- **Dedicated Daily File:** [`docs/days/day_15.md`](days/day_15.md)

#### Learn
- Query, key, value projections.
- Scaled dot product attention.
- Attention masks.
- Sequence length cost.

#### Build in MendSpeech
- Implement single head attention and then multi head attention in PyTorch.
- Add shape assertions and gradient tests.

#### Experiment and Measure
- Change sequence length and measure forward time and memory.

#### Required Output
- `src/models/attention.py`
- `tests/test_attention.py`
- `results/day15_attention_scaling.csv`

#### Completion Check
> You can derive every major tensor shape and explain quadratic sequence cost.

---

### DAY 16: Conformer convolution module
- **Compute:** `Local CPU`
- **Dedicated Daily File:** [`docs/days/day_16.md`](days/day_16.md)

#### Learn
- Pointwise convolution.
- GLU gating.
- Depthwise convolution.
- Batch normalization and activation.
- Why local patterns matter in speech.

#### Build in MendSpeech
- Implement a Conformer style convolution module.
- Test causality assumptions and receptive field.

#### Experiment and Measure
- Feed synthetic impulses and inspect how local information spreads.

#### Required Output
- `src/models/conformer_conv.py`
- `tests/test_conformer_conv.py`
- `notebooks/day16_receptive_field.ipynb`

#### Completion Check
> You can explain why depthwise convolution is computationally attractive and what
local context it captures.

---

### DAY 17: Macaron feed forward and residual scaling
- **Compute:** `Local CPU`
- **Dedicated Daily File:** [`docs/days/day_17.md`](days/day_17.md)

#### Learn
- Feed forward expansion.
- Swish or SiLU activation.
- Dropout.
- Half step residual weighting in Conformer.

#### Build in MendSpeech
- Implement the feed forward module and residual wrapper.
- Add numerical tests for shape and gradient flow.

#### Experiment and Measure
- Compare output statistics with and without residual scaling.

#### Required Output
- `src/models/conformer_ffn.py`
- `tests/test_conformer_ffn.py`

#### Completion Check
> You can explain the ordering of the Conformer block without memorizing a diagram.

---

### DAY 18: Assemble one Conformer block
- **Compute:** `Local CPU`
- **Dedicated Daily File:** [`docs/days/day_18.md`](days/day_18.md)

#### Learn
- Macaron structure.
- Layer normalization placement.
- Attention plus convolution interaction.

#### Build in MendSpeech
- Assemble feed forward, attention, convolution, second feed forward, and final normalization.
- Match expected input and output shapes.

#### Experiment and Measure
- Run forward and backward tests on several sequence lengths.
- Intentionally remove one residual path and compare training stability on a toy task.

#### Required Output
- `src/models/conformer_block.py`
- `tests/test_conformer_block.py`
- `docs/conformer_block_walkthrough.md`

#### Completion Check
> You can point to every operation and say why it exists.

---

### DAY 19: Build a tiny Conformer encoder
- **Compute:** `Local CPU, L4 optional`
- **Dedicated Daily File:** [`docs/days/day_19.md`](days/day_19.md)

#### Learn
- Input projection.
- Stacked blocks.
- Mask propagation.
- Temporal dimensions.

#### Build in MendSpeech
- Build a small encoder around your blocks.
- Connect log Mel features to the encoder.

#### Experiment and Measure
- Track tensor shape through every layer on real speech.
- Profile increasing depth.

#### Required Output
- `src/models/tiny_conformer.py`
- `results/day19_shape_trace.md`

#### Completion Check
> A real log Mel tensor can pass through your encoder and produce valid gradients.

---

### DAY 20: Compare your block with a production
- **Compute:** `Local CPU`
- **Dedicated Daily File:** [`docs/days/day_20.md`](days/day_20.md)

#### Learn
- Read the original Conformer paper sections relevant to block design.
- Inspect a mature implementation such as NeMo.
- Identify differences caused by engineering and efficiency.

#### Build in MendSpeech
- Create an annotated comparison table: your component, paper definition, production implementation.

#### Experiment and Measure
- Choose one difference and reproduce its effect on a small benchmark if feasible.

#### Required Output
- `docs/day20_implementation_comparison.md`

#### Completion Check
> You can read production Conformer code and orient yourself without treating it as
magic.

---

### DAY 21: Week 3 architecture review
- **Compute:** `Local CPU`
- **Dedicated Daily File:** [`docs/days/day_21.md`](days/day_21.md)

#### Learn
- Review attention, convolution, feed forward, normalization, residual paths, and sequence cost.

#### Build in MendSpeech
- Add an architecture inspector page to MendSpeech showing encoder stage shapes and context assumptions.

#### Experiment and Measure
- Give yourself a ten minute whiteboard explanation from waveform features through one Conformer block.

#### Required Output
- `app/encoder_inspector.py`
- `reports/week3_conformer.md`

#### Completion Check
> You can explain which parts are local, which are global, and which become
problematic for streaming.

---
