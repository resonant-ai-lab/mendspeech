# Day 49: Week 7 MendSpeech V1 cascaded repair milestone

> **Week 7 • Day 7 of 7**  
> **Navigation:** [← Day 48](day_48.md) | [Week 7 Plan](../Week_7_MendSpeech_Daily_Plan.md) | [Master Index](../INDEX.md) | [Day 50 →](day_50.md)

---

### Compute Target
`Modal L4`

---

### 1. Learn
- Review TTS, duration, vocoder behavior, speaker conditioning, boundary matching, and information lost through the text bottleneck.
- Treat the cascaded path as a real time baseline, not as the final frontier of speech restoration.

---

### 2. Build in MendSpeech
- Pipeline: damaged audio to streaming ASR to uncertain span to policy decision to speaker conditioned reconstruction to boundary matched waveform.
- Show preserved and reconstructed intervals with distinct visualization.
- Add a V1 label in results so the Week 8 direct audio repair comparison is explicit.

---

### 3. Experiment and Measure
- Run at least ten cases, including deliberate false repair, missed repair, seam artifacts, and one case where the policy abstains.
- Compare naive stitching and boundary matched stitching on the same repaired spans.

---

### 4. Required Output Artifacts
- `app/mendspeech_v4_cascaded.py`
- `demos/week7_before_after/`
- `results/week7_stitching_ablation.csv`
- `reports/week7_cascaded_repair.md`

---

### 5. Completion Check
> **Definition of Done for Day 49:**  
> MendSpeech V1 is a measured cascaded baseline whose strengths and prosody or
seam limitations are documented rather than hidden.

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
- DSP references for energy matching and equal power crossfades   Week 8: Research Capstone: Cascaded Versus Direct Repair Freeze the benchmark, run controlled ablations, compare architectures, and publish a reproducible result.  Day  Focus  Minimum evidence  Compute  Day 50  Freeze research questions and baselines
- Run a tiny dry run to ensure every result field is populated.  Local CPU for planning, Modal L4 for dry run  Day 51  Release SpeechDamageBench v1 and freeze evaluation
- Reinstall the package in a clean environment.
- Regenerate a sample from the manifest and verify its checksum.
- Validate that clean references remain unchanged.  Local CPU  Day 52  Run recognition and context ablations
- Plot WER versus latency and mark Pareto efficient points.  Modal L4, keep hardware fixed  Day 53  Run cascaded repair and seam ablations
- Test whether repairing more audio always helps intelligibility.
- Test whether boundary matching reduces seam artifacts without materially increasing latency.
- Keep recognition outputs fixed for the stitching comparison so only the repair method changes.  Modal L4  Day 54  Compare against direct latent or codec audio inpainting
- Compare raw damaged audio, MendSpeech V1 cascaded repair, full resynthesis, and the direct audio baseline on the same cases.
- Select at least ten worst or most revealing cases and inspect them manually.
- Identify at least one regime where each approach has an advantage, or explicitly report if the data does not support that conclusion.  Modal L4 or the smallest GPU that can run the chosen pretrained baseline, plus local analysis  Day 55  Write the research report and reproducibility guide
- Audit every major claim against a concrete table, figure, or experiment result.
- Remove or soften any conclusion that is not directly supported by frozen evidence.
- Verify that the report distinguishes measured facts from hypotheses and future work.  Local CPU  Day 56  Final product, demo, and clean reproduction
- Record a concise demo and create a final architecture diagram.
- Reproduce one benchmark end to end from the documented command.
- Verify that every public chart can be regenerated from saved result files.  Modal L4 for inference, local CPU for interface and analysis
