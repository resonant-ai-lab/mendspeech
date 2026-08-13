# Week 2: ASR, CTC, Confidence, and Repair Localization

> **Days 08 to 14**  
> **Navigation:** [← Week 1](Week_1_MendSpeech_Daily_Plan.md) | [Master Index](INDEX.md) | [Master Roadmap](MendSpeech_8_Week_Master_Roadmap.md) | [Week 3 →](Week_3_MendSpeech_Daily_Plan.md)

---

> [!IMPORTANT]
> **Week Milestone:**  
> Build the recognition and uncertainty layer, plus a reusable Modal execution path.

---

## Week Map

| Day | Focus | Minimum Evidence / Artifact | Compute | Daily Link |
| :--- | :--- | :--- | :--- | :--- |
| **Day 08** | Frame sequence to transcript | You can draw the path from features to encoder states to token probabilities to text,
and launch the same baseline locally or on Modal with a documented command. | `Modal L4 optional, CPU acceptable for
small runs` | [Open Day 08](days/day_08.md) |
| **Day 09** | CTC from first principles | You can explain why a blank is needed and correctly decode repeated characters. | `Local CPU` | [Open Day 09](days/day_09.md) |
| **Day 10** | WER, CER, and error taxonomy | You can calculate WER by hand for a short example and explain each error. | `Local CPU` | [Open Day 10](days/day_10.md) |
| **Day 11** | Token confidence and uncertainty | You understand why low confidence can be useful but cannot be treated as truth. | `Modal L4 recommended` | [Open Day 11](days/day_11.md) |
| **Day 12** | Time alignment and uncertain spans | The UI can highlight an uncertain audio interval and show the associated word or
token. | `Modal L4 recommended` | [Open Day 12](days/day_12.md) |
| **Day 13** | Define selective repair policy v0 | You can explain the cost of repairing too much and repairing too little. | `Local CPU after ASR outputs are
cached` | [Open Day 13](days/day_13.md) |
| **Day 14** | Week 2 integration and review | A user can see what the ASR heard and which exact intervals MendSpeech wants to
preserve or repair. | `Modal L4 recommended` | [Open Day 14](days/day_14.md) |

---

## Reference Spine
- Graves et al., Connectionist Temporal Classification\nPyTorch CTC loss and TorchAudio ASR documentation\nModal documentation for environment definitions and GPU runs

---

## Daily Detailed Operating Plans

### DAY 08: Frame sequence to transcript
- **Compute:** `Modal L4 optional, CPU acceptable for
small runs`
- **Dedicated Daily File:** [`docs/days/day_08.md`](days/day_08.md)

#### Learn
- Why acoustic frames outnumber output tokens.
- Encoder outputs, vocabulary logits, and decoding.
- CTC versus transducer versus attention decoder at a high level.

#### Build in MendSpeech
- Run a pretrained ASR model on clean and damaged SpeechDamageBench clips.
- Store transcript, token outputs if available, and timing metadata.
- Add a reusable Modal entry point so the same command can run ASR experiments on an L4 without editing deployment code each day.

#### Experiment and Measure
- Compare clean and corrupted transcripts on the exact same utterances.

#### Required Output
- `src/asr/baseline.py`
- `infra/modal_asr.py`
- `results/day08_baseline_transcripts.csv`

#### Completion Check
> You can draw the path from features to encoder states to token probabilities to text,
and launch the same baseline locally or on Modal with a documented command.

---

### DAY 09: CTC from first principles
- **Compute:** `Local CPU`
- **Dedicated Daily File:** [`docs/days/day_09.md`](days/day_09.md)

#### Learn
- CTC blank symbol.
- Repeated labels and collapse operation.
- Why many frame paths map to one transcript.
- Conditional independence assumption and its consequence.

#### Build in MendSpeech
- Implement CTC collapse yourself without a library decoder.
- Create hand written alignment examples and unit tests.

#### Experiment and Measure
- Enumerate several legal paths for a tiny target word.
- Break your decoder deliberately with repeated letters and fix it.

#### Required Output
- `src/asr/ctc_decode.py`
- `tests/test_ctc_decode.py`
- `docs/ctc_explained.md`

#### Completion Check
> You can explain why a blank is needed and correctly decode repeated characters.

---

### DAY 10: WER, CER, and error taxonomy
- **Compute:** `Local CPU`
- **Dedicated Daily File:** [`docs/days/day_10.md`](days/day_10.md)

#### Learn
- Word error rate: substitutions, deletions, insertions.
- Character error rate and when it helps.
- Why WER alone hides error severity.

#### Build in MendSpeech
- Implement or verify WER and CER calculations.
- Add an error analyzer that labels substitution, deletion, and insertion spans.

#### Experiment and Measure
- Score clean versus every SpeechDamageBench severity.
- Find which corruption type causes deletion errors fastest.

#### Required Output
- `src/metrics/wer.py`
- `results/day10_wer_by_damage.csv`
- `results/day10_error_types.csv`

#### Completion Check
> You can calculate WER by hand for a short example and explain each error.

---

### DAY 11: Token confidence and uncertainty
- **Compute:** `Modal L4 recommended`
- **Dedicated Daily File:** [`docs/days/day_11.md`](days/day_11.md)

#### Learn
- Softmax confidence and why it can be miscalibrated.
- Frame confidence versus token confidence versus word confidence.
- Entropy as an uncertainty signal.
- Confidence calibration intuition.

#### Build in MendSpeech
- Extract confidence or approximate it from model outputs.
- Create a word level confidence timeline aligned to the transcript.

#### Experiment and Measure
- Compare confidence on clean, noisy, clipped, and dropout audio.
- Find confident but wrong examples and document them.

#### Required Output
- `src/asr/confidence.py`
- `results/day11_confidence_cases.csv`
- `docs/confidence_failure_modes.md`

#### Completion Check
> You understand why low confidence can be useful but cannot be treated as truth.

---

### DAY 12: Time alignment and uncertain spans
- **Compute:** `Modal L4 recommended`
- **Dedicated Daily File:** [`docs/days/day_12.md`](days/day_12.md)

#### Learn
- Frame time conversion.
- Token timestamps and word timestamps.
- Alignment boundaries around corrupted regions.

#### Build in MendSpeech
- Map low confidence tokens back to audio time spans.
- Overlay uncertain intervals on waveform and spectrogram.

#### Experiment and Measure
- Inject known 100 ms and 250 ms dropouts and test whether uncertainty overlaps them.

#### Required Output
- `src/asr/alignment.py`
- `app/uncertainty_overlay.py`
- `results/day12_overlap_metrics.csv`

#### Completion Check
> The UI can highlight an uncertain audio interval and show the associated word or
token.

---

### DAY 13: Define selective repair policy v0
- **Compute:** `Local CPU after ASR outputs are
cached`
- **Dedicated Daily File:** [`docs/days/day_13.md`](days/day_13.md)

#### Learn
- Threshold policies.
- Hysteresis to avoid rapid toggling.
- Minimum repair span and padding.
- False repair versus missed repair tradeoff.

#### Build in MendSpeech
- Implement Preserve, Balanced, and Rescue policies.
- Each policy returns preserve spans and repair spans from confidence plus timing.

#### Experiment and Measure
- Sweep confidence thresholds on SpeechDamageBench.
- Measure percentage of audio selected for repair and overlap with known damaged spans.

#### Required Output
- `src/controller/policy.py`
- `configs/repair_modes.yaml`
- `results/day13_policy_sweep.csv`

#### Completion Check
> You can explain the cost of repairing too much and repairing too little.

---

### DAY 14: Week 2 integration and review
- **Compute:** `Modal L4 recommended`
- **Dedicated Daily File:** [`docs/days/day_14.md`](days/day_14.md)

#### Learn
- Review CTC, WER, confidence, timestamp alignment, and repair decisions.

#### Build in MendSpeech
- Pipeline: damaged audio to transcript to confidence to highlighted repair spans.
- Add clean JSON output for every run.
- Verify the Modal wrapper records model revision, GPU type, software versions, and run id automatically.

#### Experiment and Measure
- Run at least twenty corrupted utterances and manually inspect policy errors.

#### Required Output
- `app/mendspeech_v0.py`
- `infra/modal_asr.py`
- `results/week2_casebook.md`
- `reports/week2_asr_uncertainty.md`

#### Completion Check
> A user can see what the ASR heard and which exact intervals MendSpeech wants to
preserve or repair.

---
