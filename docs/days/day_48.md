# Day 48: Selective reconstruction with boundary matched stitching

> **Week 7 • Day 6 of 7**  
> **Navigation:** [← Day 47](day_47.md) | [Week 7 Plan](../Week_7_MendSpeech_Daily_Plan.md) | [Master Index](../INDEX.md) | [Day 49 →](day_49.md)

---

### Compute Target
`Modal L4 plus local CPU for stitching`

---

### 1. Learn
- Repair span text selection.
- Timing constraints and duration control.
- Boundary padding and silence handling.
- Short time energy matching and local loudness matching.
- Linear versus equal power crossfades.
- Spectral and room tone mismatch.
- Why ASR to text to TTS can lose pitch, emotion, breathing, and coarticulation.

---

### 2. Build in MendSpeech
- Take a known damaged interval and synthesize only its transcript span.
- Match generated duration to the target interval without changing untouched speech.
- Match local energy before stitching and implement both linear and equal power crossfades.
- Add optional room tone under the regenerated span when the original context supports it.
- Log preserved samples, reconstructed samples, boundary length, and all matching parameters.

---

### 3. Experiment and Measure
- Compare full utterance TTS, naive selective repair, and boundary matched selective repair.
- Measure preservation percentage, latency, energy discontinuity, and speaker similarity proxy.
- Run a small blinded seam audibility check with randomized sample order.

---

### 4. Required Output Artifacts
- `src/repair/reconstruct.py`
- `src/repair/stitch.py`
- `src/repair/boundary_metrics.py`
- `results/day48_selective_samples/`
- `results/day48_seam_ablation.csv`

---

### 5. Completion Check
> **Definition of Done for Day 48:**  
> The final audio keeps most original samples, replaces only a targeted interval, and
shows measurably smoother boundaries than naive stitching.

---

### 6. Study Method & Protocol
25 minutes focused reading. 65 minutes implementation or controlled experiment. 20 minutes research
notebook. 10 minutes commit and explain the result aloud. When debugging is incomplete, continue the
same task in the next session instead of pretending the day is finished.

---

### 7. References & Resources
- FastSpeech 2 paper
- HiFi GAN paper
- VITS paper
- DSP references for energy matching and equal power crossfades
