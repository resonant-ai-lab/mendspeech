# Day 11: Token confidence and uncertainty

> **Week 2 • Day 4 of 7**  
> **Navigation:** [← Day 10](day_10.md) | [Week 2 Plan](../Week_2_MendSpeech_Daily_Plan.md) | [Master Index](../INDEX.md) | [Day 12 →](day_12.md)

---

### Compute Target
`Modal L4 recommended`

---

### 1. Learn
- Softmax confidence and why it can be miscalibrated.
- Frame confidence versus token confidence versus word confidence.
- Entropy as an uncertainty signal.
- Confidence calibration intuition.

---

### 2. Build in MendSpeech
- Extract confidence or approximate it from model outputs.
- Create a word level confidence timeline aligned to the transcript.

---

### 3. Experiment and Measure
- Compare confidence on clean, noisy, clipped, and dropout audio.
- Find confident but wrong examples and document them.

---

### 4. Required Output Artifacts
- `src/asr/confidence.py`
- `results/day11_confidence_cases.csv`
- `docs/confidence_failure_modes.md`

---

### 5. Completion Check
> **Definition of Done for Day 11:**  
> You understand why low confidence can be useful but cannot be treated as truth.

---

### 6. Study Method & Protocol
25 minutes focused reading. 65 minutes implementation or controlled experiment. 20 minutes research
notebook. 10 minutes commit and explain the result aloud. When debugging is incomplete, continue the
same task in the next session instead of pretending the day is finished.

---

### 7. References & Resources
- CTC primary paper or a reliable derivation
- Framework ASR documentation for logits, timestamps, and confidence
