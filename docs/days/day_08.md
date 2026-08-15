# Day 08: Frame sequence to transcript

> **Week 2 • Day 1 of 7**  
> **Navigation:** [← Day 07](day_07.md) | [Week 2 Plan](../Week_2_MendSpeech_Daily_Plan.md) | [Master Index](../INDEX.md) | [Day 09 →](day_09.md)

---

### Compute Target
`Modal L4 optional, CPU acceptable for
small runs`

---

### 1. Learn
- Why acoustic frames outnumber output tokens.
- Encoder outputs, vocabulary logits, and decoding.
- CTC versus transducer versus attention decoder at a high level.

---

### 2. Build in MendSpeech
- Run a pretrained ASR model on clean and damaged SpeechDamageBench clips.
- Store transcript, token outputs if available, and timing metadata.
- Add a reusable Modal entry point so the same command can run ASR experiments on an L4 without editing deployment code each day.
- Smoke-test the pretrained direct audio inpainting baseline chosen for Week 8: install it, run one masked span, and record install steps plus a fallback in `docs/baseline_install_notes.md`.

---

### 3. Experiment and Measure
- Compare clean and corrupted transcripts on the exact same utterances.

---

### 4. Required Output Artifacts
- `src/asr/baseline.py`
- `infra/modal_asr.py`
- `results/day08_baseline_transcripts.csv`

---

### 5. Completion Check
> **Definition of Done for Day 08:**  
> You can draw the path from features to encoder states to token probabilities to text,
and launch the same baseline locally or on Modal with a documented command.

---

### 6. Study Method & Protocol
25 minutes focused reading. 65 minutes implementation or controlled experiment. 20 minutes research
notebook. 10 minutes commit and explain the result aloud. When debugging is incomplete, continue the
same task in the next session instead of pretending the day is finished.

---

### 7. References & Resources
- CTC primary paper or a reliable derivation
- Framework ASR documentation for logits, timestamps, and confidence
