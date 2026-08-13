# Day 14: Week 2 integration and review

> **Week 2 • Day 7 of 7**  
> **Navigation:** [← Day 13](day_13.md) | [Week 2 Plan](../Week_2_MendSpeech_Daily_Plan.md) | [Master Index](../INDEX.md) | [Day 15 →](day_15.md)

---

### Compute Target
`Modal L4 recommended`

---

### 1. Learn
- Review CTC, WER, confidence, timestamp alignment, and repair decisions.

---

### 2. Build in MendSpeech
- Pipeline: damaged audio to transcript to confidence to highlighted repair spans.
- Add clean JSON output for every run.
- Verify the Modal wrapper records model revision, GPU type, software versions, and run id automatically.

---

### 3. Experiment and Measure
- Run at least twenty corrupted utterances and manually inspect policy errors.

---

### 4. Required Output Artifacts
- `app/mendspeech_v0.py`
- `infra/modal_asr.py`
- `results/week2_casebook.md`
- `reports/week2_asr_uncertainty.md`

---

### 5. Completion Check
> **Definition of Done for Day 14:**  
> A user can see what the ASR heard and which exact intervals MendSpeech wants to
preserve or repair.

---

### 6. Study Method & Protocol
25 minutes focused reading. 65 minutes implementation or controlled experiment. 20 minutes research
notebook. 10 minutes commit and explain the result aloud. When debugging is incomplete, continue the
same task in the next session instead of pretending the day is finished.

---

### 7. References & Resources
- CTC primary paper or a reliable derivation
- Framework ASR documentation for logits, timestamps, and confidence   Week 3: Conformer From First Principles Implement the core encoder pieces so model behavior is not a black box.  Day  Focus  Minimum evidence  Compute  Day 15  Attention for speech sequences
- Change sequence length and measure forward time and memory.  Local CPU, L4 optional for scaling  Day 16  Conformer convolution module
- Feed synthetic impulses and inspect how local information spreads.  Local CPU  Day 17  Macaron feed forward and residual scaling
- Compare output statistics with and without residual scaling.  Local CPU  Day 18  Assemble one Conformer block
- Run forward and backward tests on several sequence lengths.
- Intentionally remove one residual path and compare training stability on a toy task.  Local CPU  Day 19  Build a tiny Conformer encoder
- Track tensor shape through every layer on real speech.
- Profile increasing depth.  Local CPU, L4 optional  Day 20  Compare your block with a production
- Choose one difference and reproduce its effect on a small benchmark if feasible.  Local CPU  Day 21  Week 3 architecture review
- Give yourself a ten minute whiteboard explanation from waveform features through one Conformer block.  Local CPU
