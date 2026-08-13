# Day 42: Week 6 robustness milestone

> **Week 6 • Day 7 of 7**  
> **Navigation:** [← Day 41](day_41.md) | [Week 6 Plan](../Week_6_MendSpeech_Daily_Plan.md) | [Master Index](../INDEX.md) | [Day 43 →](day_43.md)

---

### Compute Target
`Modal L4`

---

### 1. Learn
- Review fine tuning, augmentation, RNNT, and calibration.

---

### 2. Build in MendSpeech
- Switch between base and adapted recognizer in the research console.
- Show clean WER, damaged WER, confidence calibration, and repair percentage.

---

### 3. Experiment and Measure
- Run one fixed benchmark suite and freeze results for Week 8 comparisons.

---

### 4. Required Output Artifacts
- `app/mendspeech_v3_robust.py`
- `results/week6_frozen_baseline.csv`
- `reports/week6_training.md`

---

### 5. Completion Check
> **Definition of Done for Day 42:**  
> MendSpeech can demonstrate measured robustness gains or clearly document a
negative result.

---

### 6. Study Method & Protocol
25 minutes focused reading. 65 minutes implementation or controlled experiment. 20 minutes research
notebook. 10 minutes commit and explain the result aloud. When debugging is incomplete, continue the
same task in the next session instead of pretending the day is finished.

---

### 7. References & Resources
- NVIDIA NeMo ASR training documentation
- RNNT primary references
- Calibration and reliability diagram references   Week 7: TTS, Speaker Preservation, and Boundary Matched Reconstruction Build MendSpeech V1 as a cascaded selective repair baseline with explicit seam diagnostics.  Day  Focus  Minimum evidence  Compute  Day 43  TTS system anatomy
- Compare several sentences with punctuation and pacing changes.  Modal L4  Day 44  FastSpeech style duration and prosody
- Change speaking rate or duration settings and measure generated length.  Modal L4  Day 45  Vocoder realism and acoustic boundary diagnostics
- Measure inference speed and real time factor.
- Create intentionally mismatched generated spans and verify that the boundary diagnostics flag obvious loudness or spectral discontinuities.  Modal L4  Day 46  VITS and end to end synthesis
- Create a listening sheet with randomized sample order.  Modal L4  Day 47  Speaker representation and preservation
- Compare full resynthesis with short span reconstruction for speaker similarity.  Modal L4  Day 48  Selective reconstruction with boundary matched stitching
- Compare full utterance TTS, naive selective repair, and boundary matched selective repair.
- Measure preservation percentage, latency, energy discontinuity, and speaker similarity proxy.
- Run a small blinded seam audibility check with randomized sample order.  Modal L4 plus local CPU for stitching  Day 49  Week 7 MendSpeech V1 cascaded repair milestone
- Run at least ten cases, including deliberate false repair, missed repair, seam artifacts, and one case where the policy abstains.
- Compare naive stitching and boundary matched stitching on the same repaired spans.  Modal L4
