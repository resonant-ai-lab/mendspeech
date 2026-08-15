# Week 8: Research Capstone: Cascaded Versus Direct Repair

> **Days 50 to 56**  
> **Navigation:** [← Week 7](Week_7_MendSpeech_Daily_Plan.md) | [Master Index](INDEX.md) | [Master Roadmap](MendSpeech_8_Week_Master_Roadmap.md) | [Index →](INDEX.md)

---

> [!IMPORTANT]
> **Week Milestone:**  
> Freeze the benchmark, run controlled ablations, compare architectures, and publish a reproducible result.

---

## Week Map

| Day | Focus | Minimum Evidence / Artifact | Compute | Daily Link |
| :--- | :--- | :--- | :--- | :--- |
| **Day 50** | Freeze research questions and baselines | Another engineer could reproduce the protocol and understand exactly which claims
compare cascaded repair with direct audio repair. | `Local CPU for planning, Modal L4 for
dry run` | [Open Day 50](days/day_50.md) |
| **Day 51** | Release SpeechDamageBench v1 and freeze evaluation | SpeechDamageBench is independently installable, deterministic, versioned, and
usable without MendSpeech. | `Local CPU` | [Open Day 51](days/day_51.md) |
| **Day 52** | Run recognition and context ablations | You can say whether adaptive context helped, hurt, or made no meaningful
difference. | `Modal L4, keep hardware fixed` | [Open Day 52](days/day_52.md) |
| **Day 53** | Run cascaded repair and seam ablations | You have a defensible result for the cascaded selective repair path and can separate
recognition, reconstruction, and stitching effects. | `Modal L4` | [Open Day 53](days/day_53.md) |
| **Day 54** | Compare against direct latent or codec audio inpainting | You can explain when the cascaded path is competitive, where it loses acoustic
information, and whether direct audio repair earns its extra complexity on your benchmark. | `Modal L4 or the smallest GPU that can
run the chosen pretrained baseline,
plus local analysis` | [Open Day 54](days/day_54.md) |
| **Day 55** | Write the research report and reproducibility guide | A technical reader can understand the contribution, the architectural tradeoff, and the
limitations without opening the source code first. | `Local CPU` | [Open Day 55](days/day_55.md) |
| **Day 56** | Final product, demo, and clean reproduction | A new user can understand, run, and evaluate MendSpeech, SpeechDamageBench,
the cascaded baseline, and the direct audio comparison, and you can defend every major design decision. | `Modal L4 for inference, local CPU for
interface and analysis` | [Open Day 56](days/day_56.md) |

---

## Reference Spine
- Your frozen protocol and prior results\nA reproducible pretrained direct latent or codec audio inpainting baseline\nPrimary papers only when needed to interpret a result

---

## Daily Detailed Operating Plans

### DAY 50: Freeze research questions and baselines
- **Compute:** `Local CPU for planning, Modal L4 for
dry run`
- **Dedicated Daily File:** [`docs/days/day_50.md`](days/day_50.md)

#### Learn
- Primary question: can selective semantic repair improve intelligibility while preserving more original speech than full resynthesis?
- Secondary question: can uncertainty guided context allocation improve the latency versus accuracy operating point?
- Architecture question: when does cascaded ASR plus TTS repair beat or lose to a pretrained direct latent or codec audio inpainting baseline?
- Scope every claim to the frozen benchmark scale (≥30 utterances, ≤5 speakers) and state the statistical caveat explicitly.
- Define null outcomes, failure criteria, and claims you will not make.

#### Build in MendSpeech
- Freeze code revision, model revisions, datasets, hardware, corruption configs, and metrics.
- Define baselines: raw damaged audio, full resynthesis, MendSpeech V1 cascaded repair, fixed context, adaptive context, and one pretrained direct audio inpainting baseline if reproducible.
- Do not train the direct inpainting model from scratch. The purpose is architectural comparison, not a second major training project.

#### Experiment and Measure
- Run a tiny dry run to ensure every result field is populated.

#### Required Output
- `experiments/capstone_protocol.md`
- `configs/capstone_frozen.yaml`
- `docs/baseline_definitions.md`

#### Completion Check
> Another engineer could reproduce the protocol and understand exactly which claims
compare cascaded repair with direct audio repair.

---

### DAY 51: Release SpeechDamageBench v1 and freeze evaluation
- **Compute:** `Local CPU`
- **Dedicated Daily File:** [`docs/days/day_51.md`](days/day_51.md)

#### Learn
- Severity grids.
- Speaker separated evaluation.
- Seed control and deterministic manifests.
- Package versioning and reproducibility.
- Clean regression cases that must remain untouched.

#### Build in MendSpeech
- Finalize the independent SpeechDamageBench package with noise, clipping, bandwidth, dropout, and reverberation presets.
- Generate the frozen test matrix and lock manifest checksums.
- Add an installation command and a one command example that reproduces one benchmark item.

#### Experiment and Measure
- Reinstall the package in a clean environment.
- Regenerate a sample from the manifest and verify its checksum.
- Validate that clean references remain unchanged.

#### Required Output
- `speechdamagebench/`
- `speechdamagebench/README.md`
- `speechdamagebench/CHANGELOG.md`
- `benchmarks/speechdamagebench_manifest.csv`
- `benchmarks/README.md`

#### Completion Check
> SpeechDamageBench is independently installable, deterministic, versioned, and
usable without MendSpeech.

---

### DAY 52: Run recognition and context ablations
- **Compute:** `Modal L4, keep hardware fixed`
- **Dedicated Daily File:** [`docs/days/day_52.md`](days/day_52.md)

#### Learn
- Fixed lookahead comparison.
- Adaptive context policy.
- WER, latency, RTF, memory, confidence behavior.

#### Build in MendSpeech
- Run every streaming condition on the exact same benchmark subset.
- Repeat timing runs enough to estimate variance.
- Record GPU type and environment automatically through the Modal runner.

#### Experiment and Measure
- Plot WER versus latency and mark Pareto efficient points.

#### Required Output
- `results/capstone_streaming.csv`
- `results/streaming_pareto.png`

#### Completion Check
> You can say whether adaptive context helped, hurt, or made no meaningful
difference.

---

### DAY 53: Run cascaded repair and seam ablations
- **Compute:** `Modal L4`
- **Dedicated Daily File:** [`docs/days/day_53.md`](days/day_53.md)

#### Learn
- Repair threshold.
- Repair span padding.
- Preserve percentage.
- Full resynthesis baseline.
- Boundary energy matching, crossfade choice, and seam artifact rate.

#### Build in MendSpeech
- Run Preserve, Balanced, Rescue, full resynthesis, naive selective stitching, and boundary matched selective stitching.
- Record original waveform retained, repair percentage, end to end latency, speaker similarity proxy, and seam metrics.

#### Experiment and Measure
- Test whether repairing more audio always helps intelligibility.
- Test whether boundary matching reduces seam artifacts without materially increasing latency.
- Keep recognition outputs fixed for the stitching comparison so only the repair method changes.

#### Required Output
- `results/capstone_cascaded_repair.csv`
- `results/repair_tradeoff.png`
- `results/seam_ablation.png`

#### Completion Check
> You have a defensible result for the cascaded selective repair path and can separate
recognition, reconstruction, and stitching effects.

---

### DAY 54: Compare against direct latent or codec audio inpainting
- **Compute:** `Modal L4 or the smallest GPU that can
run the chosen pretrained baseline,
plus local analysis`
- **Dedicated Daily File:** [`docs/days/day_54.md`](days/day_54.md)

#### Learn
- Why text is an information bottleneck for prosody and acoustic continuity.
- Direct audio inpainting in latent or codec token spaces at a conceptual level.
- Fair baseline design when systems have different latency and compute profiles.
- Failure taxonomy across semantic correctness, speaker similarity, prosody, seam quality, and compute.

#### Build in MendSpeech
- Use the pretrained direct audio inpainting baseline already selected and smoke-tested in Week 2 (see `docs/baseline_install_notes.md`); do not start model hunting here.
- Wrap it behind the same benchmark interface used by MendSpeech.
- Feed identical SpeechDamageBench cases and record the same metrics wherever they are meaningful.
- Create a failure casebook covering both architectures.
- Keep abstention active for MendSpeech when the inferred content is not reliable enough to reconstruct safely.

#### Experiment and Measure
- Compare raw damaged audio, MendSpeech V1 cascaded repair, full resynthesis, and the direct audio baseline on the same cases.
- Select at least ten worst or most revealing cases and inspect them manually.
- Identify at least one regime where each approach has an advantage, or explicitly report if the data does not support that conclusion.

#### Required Output
- `src/baselines/direct_audio_inpaint.py`
- `results/capstone_architecture_compare.csv`
- `results/capstone_failure_casebook.md`
- `results/architecture_tradeoff.png`
- `src/controller/abstain.py`

#### Completion Check
> You can explain when the cascaded path is competitive, where it loses acoustic
information, and whether direct audio repair earns its extra complexity on your benchmark.

---

### DAY 55: Write the research report and reproducibility guide
- **Compute:** `Local CPU`
- **Dedicated Daily File:** [`docs/days/day_55.md`](days/day_55.md)

#### Learn
- Abstract, motivation, hypotheses, method, baselines, metrics, results, limitations, ethics, and future work.
- Difference between observation and causal claim.
- How to report a negative or mixed architectural comparison honestly.
- Benchmark scale and its statistical limits: never claim population-level generalization from ≤5 speakers.

#### Build in MendSpeech
- Write the complete report.
- Add exact reproduction commands and environment capture.
- Include the cascaded versus direct repair comparison as a dedicated section.
- Document seam limitations, prosody loss, and any conditions where the direct baseline is clearly stronger.
- Include plots with captions that state what changed and what stayed fixed.

#### Experiment and Measure
- Audit every major claim against a concrete table, figure, or experiment result.
- Remove or soften any conclusion that is not directly supported by frozen evidence.
- Verify that the report distinguishes measured facts from hypotheses and future work.

#### Required Output
- `REPORT.md`
- `REPRODUCE.md`
- `results/final_figures/`
- `docs/limitations_and_claims.md`

#### Completion Check
> A technical reader can understand the contribution, the architectural tradeoff, and the
limitations without opening the source code first.

---

### DAY 56: Final product, demo, and clean reproduction
- **Compute:** `Modal L4 for inference, local CPU for
interface and analysis`
- **Dedicated Daily File:** [`docs/days/day_56.md`](days/day_56.md)

#### Learn
- Review the complete path from waveform and controlled corruption to streaming encoder, uncertainty, repair policy, cascaded reconstruction, direct audio baseline, and evaluation.

#### Build in MendSpeech
- Build the final demo with upload or microphone input, controlled damage, live transcript, uncertainty heatmap, preserved versus repaired timeline, before and after playback, metrics, and architecture selection for benchmark playback.
- Show which milliseconds were preserved, reconstructed by the cascaded path, or repaired by the direct baseline.
- Reproduce one frozen benchmark from a fresh environment and tag a stable release.

#### Experiment and Measure
- Record a concise demo and create a final architecture diagram.
- Reproduce one benchmark end to end from the documented command.
- Verify that every public chart can be regenerated from saved result files.

#### Required Output
- `app/mendspeech_final.py`
- `README.md`
- `demos/final_demo.mp4`
- `docs/architecture.png`
- `release_notes.md`
- `results/reproduction_check.txt`

#### Completion Check
> A new user can understand, run, and evaluate MendSpeech, SpeechDamageBench,
the cascaded baseline, and the direct audio comparison, and you can defend every major design decision.

---
