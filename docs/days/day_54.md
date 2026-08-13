# Day 54: Compare against direct latent or codec audio inpainting

> **Week 8 • Day 5 of 7**  
> **Navigation:** [← Day 53](day_53.md) | [Week 8 Plan](../Week_8_MendSpeech_Daily_Plan.md) | [Master Index](../INDEX.md) | [Day 55 →](day_55.md)

---

### Compute Target
`Modal L4 or the smallest GPU that can
run the chosen pretrained baseline,
plus local analysis`

---

### 1. Learn
- Why text is an information bottleneck for prosody and acoustic continuity.
- Direct audio inpainting in latent or codec token spaces at a conceptual level.
- Fair baseline design when systems have different latency and compute profiles.
- Failure taxonomy across semantic correctness, speaker similarity, prosody, seam quality, and compute.

---

### 2. Build in MendSpeech
- Select one reproducible pretrained direct audio inpainting or restoration baseline.
- Wrap it behind the same benchmark interface used by MendSpeech.
- Feed identical SpeechDamageBench cases and record the same metrics wherever they are meaningful.
- Create a failure casebook covering both architectures.
- Keep abstention active for MendSpeech when the inferred content is not reliable enough to reconstruct safely.

---

### 3. Experiment and Measure
- Compare raw damaged audio, MendSpeech V1 cascaded repair, full resynthesis, and the direct audio baseline on the same cases.
- Select at least ten worst or most revealing cases and inspect them manually.
- Identify at least one regime where each approach has an advantage, or explicitly report if the data does not support that conclusion.

---

### 4. Required Output Artifacts
- `src/baselines/direct_audio_inpaint.py`
- `results/capstone_architecture_compare.csv`
- `results/capstone_failure_casebook.md`
- `results/architecture_tradeoff.png`
- `src/controller/abstain.py`

---

### 5. Completion Check
> **Definition of Done for Day 54:**  
> You can explain when the cascaded path is competitive, where it loses acoustic
information, and whether direct audio repair earns its extra complexity on your benchmark.

---

### 6. Study Method & Protocol
25 minutes focused reading. 65 minutes implementation or controlled experiment. 20 minutes research
notebook. 10 minutes commit and explain the result aloud. When debugging is incomplete, continue the
same task in the next session instead of pretending the day is finished.

---

### 7. References & Resources
- Your frozen protocol and prior results
- A reproducible pretrained direct latent or codec audio inpainting baseline
- Primary papers only when needed to interpret a result
