# Day 13: Define selective repair policy v0

> **Week 2 • Day 6 of 7**  
> **Navigation:** [← Day 12](day_12.md) | [Week 2 Plan](../Week_2_MendSpeech_Daily_Plan.md) | [Master Index](../INDEX.md) | [Day 14 →](day_14.md)

---

### Compute Target
`Local CPU after ASR outputs are
cached`

---

### 1. Learn
- Threshold policies.
- Hysteresis to avoid rapid toggling.
- Minimum repair span and padding.
- False repair versus missed repair tradeoff.

---

### 2. Build in MendSpeech
- Implement Preserve, Balanced, and Rescue policies.
- Each policy returns preserve spans and repair spans from confidence plus timing.

---

### 3. Experiment and Measure
- Sweep confidence thresholds on SpeechDamageBench.
- Measure percentage of audio selected for repair and overlap with known damaged spans.

---

### 4. Required Output Artifacts
- `src/controller/policy.py`
- `configs/repair_modes.yaml`
- `results/day13_policy_sweep.csv`

---

### 5. Completion Check
> **Definition of Done for Day 13:**  
> You can explain the cost of repairing too much and repairing too little.

---

### 6. Study Method & Protocol
25 minutes focused reading. 65 minutes implementation or controlled experiment. 20 minutes research
notebook. 10 minutes commit and explain the result aloud. When debugging is incomplete, continue the
same task in the next session instead of pretending the day is finished.

---

### 7. References & Resources
- CTC primary paper or a reliable derivation
- Framework ASR documentation for logits, timestamps, and confidence
