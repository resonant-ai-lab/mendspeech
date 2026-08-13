# Day 10: WER, CER, and error taxonomy

> **Week 2 • Day 3 of 7**  
> **Navigation:** [← Day 09](day_09.md) | [Week 2 Plan](../Week_2_MendSpeech_Daily_Plan.md) | [Master Index](../INDEX.md) | [Day 11 →](day_11.md)

---

### Compute Target
`Local CPU`

---

### 1. Learn
- Word error rate: substitutions, deletions, insertions.
- Character error rate and when it helps.
- Why WER alone hides error severity.

---

### 2. Build in MendSpeech
- Implement or verify WER and CER calculations.
- Add an error analyzer that labels substitution, deletion, and insertion spans.

---

### 3. Experiment and Measure
- Score clean versus every SpeechDamageBench severity.
- Find which corruption type causes deletion errors fastest.

---

### 4. Required Output Artifacts
- `src/metrics/wer.py`
- `results/day10_wer_by_damage.csv`
- `results/day10_error_types.csv`

---

### 5. Completion Check
> **Definition of Done for Day 10:**  
> You can calculate WER by hand for a short example and explain each error.

---

### 6. Study Method & Protocol
25 minutes focused reading. 65 minutes implementation or controlled experiment. 20 minutes research
notebook. 10 minutes commit and explain the result aloud. When debugging is incomplete, continue the
same task in the next session instead of pretending the day is finished.

---

### 7. References & Resources
- CTC primary paper or a reliable derivation
- Framework ASR documentation for logits, timestamps, and confidence
