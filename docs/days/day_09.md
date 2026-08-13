# Day 09: CTC from first principles

> **Week 2 • Day 2 of 7**  
> **Navigation:** [← Day 08](day_08.md) | [Week 2 Plan](../Week_2_MendSpeech_Daily_Plan.md) | [Master Index](../INDEX.md) | [Day 10 →](day_10.md)

---

### Compute Target
`Local CPU`

---

### 1. Learn
- CTC blank symbol.
- Repeated labels and collapse operation.
- Why many frame paths map to one transcript.
- Conditional independence assumption and its consequence.

---

### 2. Build in MendSpeech
- Implement CTC collapse yourself without a library decoder.
- Create hand written alignment examples and unit tests.

---

### 3. Experiment and Measure
- Enumerate several legal paths for a tiny target word.
- Break your decoder deliberately with repeated letters and fix it.

---

### 4. Required Output Artifacts
- `src/asr/ctc_decode.py`
- `tests/test_ctc_decode.py`
- `docs/ctc_explained.md`

---

### 5. Completion Check
> **Definition of Done for Day 09:**  
> You can explain why a blank is needed and correctly decode repeated characters.

---

### 6. Study Method & Protocol
25 minutes focused reading. 65 minutes implementation or controlled experiment. 20 minutes research
notebook. 10 minutes commit and explain the result aloud. When debugging is incomplete, continue the
same task in the next session instead of pretending the day is finished.

---

### 7. References & Resources
- CTC primary paper or a reliable derivation
- Framework ASR documentation for logits, timestamps, and confidence
