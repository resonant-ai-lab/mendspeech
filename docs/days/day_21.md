# Day 21: Week 3 architecture review

> **Week 3 • Day 7 of 7**  
> **Navigation:** [← Day 20](day_20.md) | [Week 3 Plan](../Week_3_MendSpeech_Daily_Plan.md) | [Master Index](../INDEX.md) | [Day 22 →](day_22.md)

---

### Compute Target
`Local CPU`

---

### 1. Learn
- Review attention, convolution, feed forward, normalization, residual paths, and sequence cost.

---

### 2. Build in MendSpeech
- Add an architecture inspector page to MendSpeech showing encoder stage shapes and context assumptions.

---

### 3. Experiment and Measure
- Give yourself a ten minute whiteboard explanation from waveform features through one Conformer block.

---

### 4. Required Output Artifacts
- `app/encoder_inspector.py`
- `reports/week3_conformer.md`

---

### 5. Completion Check
> **Definition of Done for Day 21:**  
> You can explain which parts are local, which are global, and which become
problematic for streaming.

---

### 6. Study Method & Protocol
25 minutes focused reading. 65 minutes implementation or controlled experiment. 20 minutes research
notebook. 10 minutes commit and explain the result aloud. When debugging is incomplete, continue the
same task in the next session instead of pretending the day is finished.

---

### 7. References & Resources
- Conformer primary paper
- A mature Conformer implementation such as NVIDIA NeMo   Week 4: FastConformer and Efficient Encoder Behavior Measure why FastConformer is efficient and freeze a reproducible baseline.  Day  Focus  Minimum evidence  Compute  Day 22  Why FastConformer exists
- Estimate attention matrix size before and after aggressive temporal subsampling.  Local CPU  Day 23  Temporal subsampling experiment
- Compare 2x, 4x, and 8x temporal reduction on tensor length, runtime, and rough output behavior.  Modal L4 useful  Day 24  Pretrained FastConformer baseline
- Benchmark WER, latency, and GPU memory by damage type.  Modal L4  Day 25  Context and attention limits
- If supported, compare at least two context settings on the same subset.  Modal L4  Day 26  Efficiency benchmark harness
- Run repeated inference and calculate variance.
- Detect and discard obviously invalid cold start comparisons.  Modal L4  Day 27  FastConformer failure casebook
- Look for systematic error patterns rather than isolated anecdotes.  Modal L4  Day 28  Week 4 integration
- Run the same ten reference clips through the full Week 2 uncertainty policy using FastConformer.  Modal L4
