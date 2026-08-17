# Week 7: TTS, Speaker Preservation, and Boundary Matched Reconstruction

> **Days 43 to 49**  
> **Navigation:** [← Week 6](Week_6_MendSpeech_Daily_Plan.md) | [Master Index](INDEX.md) | [Master Roadmap](MendSpeech_8_Week_Master_Roadmap.md) | [Week 8 →](Week_8_MendSpeech_Daily_Plan.md)

---

> [!IMPORTANT]
> **Week Milestone:**  
> Build MendSpeech V1 as a cascaded selective repair baseline with explicit seam diagnostics.
>
> **v1 October calendar:** Gate 6 target **Oct 18**. Days 43–49 run as written, then **Add-on D** (voice-agent demo) on the Gate 6 weekend.

---

## Week Map

| Day | Focus | Minimum Evidence / Artifact | Compute | Daily Link |
| :--- | :--- | :--- | :--- | :--- |
| **Day 43** | TTS system anatomy | You can explain how text becomes waveform and where speaker identity can enter. | `Modal L4` | [Open Day 43](days/day_43.md) |
| **Day 44** | FastSpeech style duration and prosody | You understand why duration matters when replacing only a short span. | `Modal L4` | [Open Day 44](days/day_44.md) |
| **Day 45** | Vocoder realism and acoustic boundary diagnostics | You can separate acoustic model errors from vocoder artifacts and quantify at least
two causes of an audible seam. | `Modal L4` | [Open Day 45](days/day_45.md) |
| **Day 46** | VITS and end to end synthesis | You can explain why different TTS architectures behave differently for selective repair. | `Modal L4` | [Open Day 46](days/day_46.md) |
| **Day 47** | Speaker representation and preservation | You can discuss speaker similarity measurements and their limitations without
claiming identity preservation from listening alone. | `Modal L4` | [Open Day 47](days/day_47.md) |
| **Day 48** | Selective reconstruction with boundary matched stitching | The final audio keeps most original samples, replaces only a targeted interval, and
shows measurably smoother boundaries than naive stitching. | `Modal L4 plus local CPU for stitching` | [Open Day 48](days/day_48.md) |
| **Day 49** | Week 7 MendSpeech V1 cascaded repair milestone | MendSpeech V1 is a measured cascaded baseline whose strengths and prosody or
seam limitations are documented rather than hidden. | `Modal L4` | [Open Day 49](days/day_49.md) |

---

## Reference Spine
- FastSpeech 2 paper\nHiFi GAN paper\nVITS paper\nDSP references for energy matching and equal power crossfades

---

## Daily Detailed Operating Plans

### DAY 43: TTS system anatomy
- **Compute:** `Modal L4`
- **Dedicated Daily File:** [`docs/days/day_43.md`](days/day_43.md)

#### Learn
- Text or phoneme representation.
- Acoustic model.
- Mel spectrogram or latent representation.
- Vocoder.
- Speaker conditioning.
- Prosody.
- Content, speaker, and style representations; why useful factorization is not
  proof of perfect disentanglement.

#### Build in MendSpeech
- Run a pretrained TTS system on controlled text.
- Save generated waveform and intermediate representations if exposed.
- Record where the selected system injects linguistic content, speaker
  identity, and style or prosody conditioning.

#### Experiment and Measure
- Compare several sentences with punctuation and pacing changes.

#### Required Output
- `src/tts/baseline.py`
- `results/day43_tts_samples/`
- `docs/tts_pipeline.md`

#### Completion Check
> You can explain how text becomes waveform and where speaker identity can enter.

---

### DAY 44: FastSpeech style duration and prosody
- **Compute:** `Modal L4`
- **Dedicated Daily File:** [`docs/days/day_44.md`](days/day_44.md)

#### Learn
- Duration prediction.
- Pitch and energy predictors.
- Parallel generation intuition.

#### Build in MendSpeech
- Study FastSpeech 2 architecture and inspect an implementation.
- Extract or visualize duration, pitch, or energy controls if available.

#### Experiment and Measure
- Change speaking rate or duration settings and measure generated length.

#### Required Output
- `docs/day44_fastspeech2.md`
- `results/day44_prosody_samples/`

#### Completion Check
> You understand why duration matters when replacing only a short span.

---

### DAY 45: Vocoder realism and acoustic boundary diagnostics
- **Compute:** `Modal L4`
- **Dedicated Daily File:** [`docs/days/day_45.md`](days/day_45.md)

#### Learn
- Mel to waveform generation.
- HiFi GAN style generator and discriminator intuition.
- Phase, bandwidth, and vocoder artifacts.
- Short time energy, local loudness, spectral balance, and room tone as boundary signals.

#### Build in MendSpeech
- Run a neural vocoder or inspect the one used by the selected TTS stack.
- Add boundary diagnostics that measure short time energy and simple spectral statistics before and after a candidate repair span.
- Save a local room tone estimate where possible.

#### Experiment and Measure
- Measure inference speed and real time factor.
- Create intentionally mismatched generated spans and verify that the boundary diagnostics flag obvious loudness or spectral discontinuities.

#### Required Output
- `results/day45_vocoder_benchmark.csv`
- `src/repair/boundary_metrics.py`
- `docs/vocoder_and_boundary_notes.md`

#### Completion Check
> You can separate acoustic model errors from vocoder artifacts and quantify at least
two causes of an audible seam.

---

### DAY 46: VITS and end to end synthesis
- **Compute:** `Modal L4`
- **Dedicated Daily File:** [`docs/days/day_46.md`](days/day_46.md)

#### Learn
- Latent variable modeling.
- Normalizing flow intuition.
- Adversarial training.
- End to end waveform generation.

#### Build in MendSpeech
- Run a VITS style pretrained model or study its code path.
- Compare latency and perceived naturalness with your Week 7 baseline.

#### Experiment and Measure
- Create a listening sheet with randomized sample order.

#### Required Output
- `results/day46_tts_comparison.csv`
- `results/day46_listening_sheet.md`

#### Completion Check
> You can explain why different TTS architectures behave differently for selective repair.

---

### DAY 47: Speaker representation and preservation
- **Compute:** `Modal L4`
- **Dedicated Daily File:** [`docs/days/day_47.md`](days/day_47.md)

#### Learn
- Speaker embeddings.
- Reference conditioned synthesis.
- Speaker similarity as a measurable but imperfect proxy.
- Consent and voice identity boundaries.

#### Build in MendSpeech
- Choose a speaker conditioned or reference conditioned path that is legally and ethically appropriate for your own or consented samples.
- Compute speaker embeddings before and after synthesis if tooling is available.

#### Experiment and Measure
- Compare full resynthesis with short span reconstruction for speaker similarity.

#### Required Output
- `src/tts/speaker_conditioning.py`
- `results/day47_speaker_similarity.csv`
- `docs/voice_use_policy.md`

#### Completion Check
> You can discuss speaker similarity measurements and their limitations without
claiming identity preservation from listening alone.

---

### DAY 48: Selective reconstruction with boundary matched stitching
- **Compute:** `Modal L4 plus local CPU for stitching`
- **Dedicated Daily File:** [`docs/days/day_48.md`](days/day_48.md)

#### Learn
- Repair span text selection.
- Timing constraints and duration control.
- Boundary padding and silence handling.
- Short time energy matching and local loudness matching.
- Linear versus equal power crossfades.
- Spectral and room tone mismatch.
- Why ASR to text to TTS can lose pitch, emotion, breathing, and coarticulation.

#### Build in MendSpeech
- Take a known damaged interval and synthesize only its transcript span.
- Match generated duration to the target interval without changing untouched speech.
- Match local energy before stitching and implement both linear and equal power crossfades.
- Add optional room tone under the regenerated span when the original context supports it.
- Log preserved samples, reconstructed samples, boundary length, and all matching parameters.

#### Experiment and Measure
- Compare full utterance TTS, naive selective repair, and boundary matched selective repair.
- Measure preservation percentage, latency, energy discontinuity, and speaker similarity proxy.
- Run a small blinded seam audibility check with randomized sample order.

#### Required Output
- `src/repair/reconstruct.py`
- `src/repair/stitch.py`
- `src/repair/boundary_metrics.py`
- `results/day48_selective_samples/`
- `results/day48_seam_ablation.csv`

#### Completion Check
> The final audio keeps most original samples, replaces only a targeted interval, and
shows measurably smoother boundaries than naive stitching.

---

### DAY 49: Week 7 MendSpeech V1 cascaded repair milestone
- **Compute:** `Modal L4`
- **Dedicated Daily File:** [`docs/days/day_49.md`](days/day_49.md)

#### Learn
- Review TTS, duration, vocoder behavior, speaker conditioning, boundary matching, and information lost through the text bottleneck.
- Treat the cascaded path as a real time baseline, not as the final frontier of speech restoration.

#### Build in MendSpeech
- Pipeline: damaged audio to streaming ASR to uncertain span to policy decision to speaker conditioned reconstruction to boundary matched waveform.
- Show preserved and reconstructed intervals with distinct visualization.
- Add a V1 label in results so the Week 8 direct audio repair comparison is explicit.

#### Experiment and Measure
- Run at least ten cases, including deliberate false repair, missed repair, seam artifacts, and one case where the policy abstains.
- Compare naive stitching and boundary matched stitching on the same repaired spans.

#### Required Output
- `app/mendspeech_v4_cascaded.py`
- `demos/week7_before_after/`
- `results/week7_stitching_ablation.csv`
- `reports/week7_cascaded_repair.md`

#### Completion Check
> MendSpeech V1 is a measured cascaded baseline whose strengths and prosody or
seam limitations are documented rather than hidden.

---
