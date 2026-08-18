# Revised Execution Plan (v1 — October Calendar)

> **Status:** This document re-baselines the calendar to an **October 25 completion** and adds four add-on labs (one post-capstone).
> The 56 day files remain the source of truth for daily content; this file governs **pacing, gates, compression decisions, and add-ons**.
>
> **Speech-ML systems amendment (August 18, 2026):** the 56-day core
> sequence is unchanged. Add-on A is now a mandatory timed VAD build, Add-on B
> includes production streaming/load behavior, and Add-on C becomes an Indic
> and code-mixed evaluation instead of an unrelated VLM lab.

---

## What Changed From the Original 8-Week Plan

1. **Completion target moved from December to October 25** (buffer through October 31). This requires a mandatory **6 sessions per week** cadence and three scope compressions (below).
2. **Weeks 3–4 merged into a 10-session "Encoder Block."** Precise mapping lives in the Week 3 and Week 4 guides (v1 Compression Maps): Days 15, 16, 18, 19, 21 and Days 23, 24, 25, 26, 28 run as sessions; Day 17 becomes learn-only (its macaron build moves into Day 18); Day 20 is dropped as a session; Day 22 merges into Day 23; Day 27 folds into Day 28. Everything downstream uses pretrained NeMo FastConformer. Rationale: the original plan already classified the scratch encoder as a *learning artifact*; the shipped, measured system is the primary research output.
3. **Week 8 compressed to 5 sessions** (mapping in the Week 8 guide): Days 52+53 merge into one combined ablation session, Days 55+56 merge into one report-plus-demo session; the span-sensitivity ablation drops. Keeps the core cascaded-vs-direct comparison, the clean-speech regression check, and the report.
4. **Speech-ML systems depth is strengthened without reordering the core.** Add-on
   A becomes a mandatory from-scratch VAD challenge; Add-on B adds async
   streaming, backpressure, utilization, and tail-latency evidence; Add-on C
   becomes a post-capstone Indic and code-mixed evaluation. The separate
   [Speech-ML Systems Drill Track](SPEECH_ML_SYSTEMS_DRILLS.md) runs in
   short parallel drills and does not consume core build sessions.
5. **The unrelated VLM lab is removed from this three-month plan.** It can be
   reconsidered after the speech-system experiments and documentation are
   complete.
6. **Safety valve:** if two full weeks are missed, the December calendar automatically applies again — no renegotiation, no guilt, just re-date the gates.

Everything else — blueprint, metrics, definition of done, split-session protocol — is unchanged.

---

## Session Protocol (unchanged rules, stricter cadence)

- **Cadence: 6 sessions per week, mandatory.** Five weekday evenings + Saturday. **Sunday is recovery-only:** catch up a missed session or rest. Never bank on Sunday for new material.
- **Split sessions allowed:** a day's `Learn` block and its `Build`/`Experiment` blocks may happen in separate sittings on the same calendar day. Never start a build session without the Learn block read; never end one without a commit.
- **Theory blocks are non-negotiable.** Under compression they are the first thing schedule pressure attacks and the last thing that can be cut — they are what makes the artifacts defensible.
- **Timebox rule (unchanged):** maximum 2 extra sessions per day.
- **Systems drills are parallel, not new days.** Start the
  [Speech-ML Systems Drill Track](SPEECH_ML_SYSTEMS_DRILLS.md) **after
  Gate 2**. Three 30-minute drills per week from then on. Skip a drill
  before skipping a core Learn/Build/Measure session. Week 1 has no
  drill obligation.

---

## Week 1 data contract (do not wait for Day 07)

Gate 1 fails if the labeled set is collected on the freeze day. Split the
work:

| When | What |
| :--- | :--- |
| Days 04–05 | Acquire a public transcripted subset (e.g. LibriSpeech `dev-clean`) into `data/benchmark/`. Relative paths, `transcript`, `speaker_id`. Reach ≥10 labeled clips by Day 05 and ≥30 / ≥5 speakers before Day 07. |
| Day 07 | Freeze only: `data/benchmark_manifest.csv` with a `split` column, SpeechDamageBench v0.1, no new speakers. |
| After Day 07 | The frozen set is immutable. New experiments get new corruption configs, not a new test set. |

Speaker scale: **≥5 speakers is the floor.** Typical lab size is ~5. Week 8's
caveat (“do not generalize from a ~5-speaker set”) is a reporting limit, not
a command to stay at or under 5.

SpeechDamageBench layout: nested package
`speechdamagebench/speechdamagebench/` with its **own** `pyproject.toml`.
Never overwrite the repo-root `mendspeech` `pyproject.toml`.

Gate 1 is a Sunday. Sunday remains recovery-only for *new* material; Day 07
may use 23 Aug as the allowed catch-up session if Days 04–06 landed.

---

## Milestone Gates (October calendar)

| Gate | Days | Exit Evidence | Target |
| :--- | :--- | :--- | :--- |
| **Gate 1** | 02–07 | Audio lab + `SpeechDamageBench` v0; frozen benchmark (≥30 transcripted utterances, ≥5 speakers, speaker-separated splits) | **Aug 23** |
| **Gate 2** | 08–14 | ASR baseline + confidence + Modal pipeline; inpainting baseline smoke-tested. **Then mandatory Add-on A** (timed VAD weekend) | **Sep 1** |
| **Gate 3** | 15–28 (compressed to 10 sessions) | **Encoder Block:** scratch attention, convolution, and macaron modules with shape/gradient tests; pretrained FastConformer baseline reproducing reference WER; subsampling profiling; top-3 failure casebook | **Sep 13** |
| **Gate 4** | 29–35 | Cache-aware streaming ASR with VAD/endpointing and adaptive-context results. **Then Add-on B** (async serving/load weekend) | **Sep 27** |
| **Gate 5** | 36–42 | Robust fine-tuning + Day 40 quantization + calibration; frozen Week 6 benchmark | **Oct 3** |
| **Gate 6** | 43–49 | MendSpeech V1 complete: selective TTS repair, boundary matching, seam diagnostics. **Then Add-on D** (weekend) | **Oct 18** |
| **Gate 7** | 50–56 (compressed to 5 sessions) | Capstone: cascaded vs direct repair, core Pareto ablation, clean-speech regression check, final report. **Then Add-on C** (post-capstone) | **Oct 25** |

Buffer: October 26–31 for slippage, report polish, and demo recording.

---

## Add-On Labs

### Add-on A — Timed VAD Challenge *(mandatory after Gate 2, ~2 sessions)*
- **Session 1 — constrained build:** freeze a 30–50-file subset, start a
  2.5-hour timer, and implement a deterministic frame-level VAD without an
  external API or pretrained VAD. Begin with energy, spectral, or log-Mel
  features plus an explainable threshold or small classical classifier. Add
  tests for framing, timestamps, silence, and seed-controlled evaluation.
- **Session 2 — production comparison:** compare the scratch baseline with
  WebRTC VAD or another local production baseline. Denoising and diarization
  are optional second-stage comparisons; they must not replace the scratch
  implementation.
- **Measure:** speech precision/recall/F1, false-alarm rate, missed-speech rate,
  onset/offset boundary error in milliseconds, and CPU RTF on clean and damaged
  clips. Record the improvements that did not fit inside the timer.
- **Artifacts:** `src/vad/baseline.py`, `tests/test_vad.py`,
  `results/addon_a_vad_benchmark.csv`,
  `results/addon_a_diarization_der.csv` when diarization is run, and
  `docs/addon_a_notes.md`.
- **Completion check:** rebuild the scratch baseline under the constraint,
  defend the architecture and error trade-offs, and name the next three
  improvements without hiding incomplete work.

### Add-on B — Serving Deployment *(Gate 4 weekend, ~2 sessions)*
- **Build:** an async FastAPI/WebSocket service around the streaming ASR,
  Dockerized and deployed on Modal. Reuse Add-on A VAD for endpointing; make
  queue limits, backpressure, timeout, disconnect, retry, and fallback behavior
  explicit.
- **Measure:** concurrency at 1, 4, and 8 streams on fixed hardware; time to
  first partial transcript; endpoint/finalization delay; end-to-end p50/p95/p99;
  RTF; cold-start time; CPU/GPU utilization; peak GPU memory; queue depth; and
  dropped or delayed chunks.
- **Artifacts:** `infra/serve/`, `results/addon_b_serving.csv`, and
  `reports/addon_b_serving.md`.
- **Completion check:** identify the measured bottleneck, explain how
  backpressure prevents unbounded latency, and reproduce one controlled
  failure/recovery case.

### Add-on D — Voice-Agent Loop Demo *(Gate 6 weekend, ~2 sessions)*
- **Build:** streaming ASR → LLM → TTS loop (Week 7 model or API), one recorded demo clip.
- **Measure:** per-stage latency budget and end-to-end response time.
- **Artifacts:** `app/voice_agent_demo.py`, `results/addon_d_latency_budget.csv`, demo clip.

### Add-on C — Indic & Code-Mixed Speech Evaluation *(post-Gate 7, ~2 sessions)*
- **Build:** create a separate, consented or public evaluation manifest for one
  Indian language the researcher can verify, Indian English, and a code-mixed
  slice. Include multiple speakers plus names, numerals, transliterations, and
  clean/noisy/dropout conditions. Do not mutate the frozen capstone benchmark.
- **Compare:** run the open MendSpeech path first. Optional commercial or
  hosted ASR/TTS backends may be adapters, but the core result must remain
  reproducible without private credentials.
- **Measure:** WER/CER by language slice, entity error rate, VAD/endpointing
  errors, time to first partial transcript, p50/p95 latency, and explicitly
  documented code-mixing failures.
- **Artifacts:** `data/indic_codemix_manifest.csv`,
  `results/addon_c_indic_codemix.csv`, and
  `reports/addon_c_speech_readiness.md`.
- **Completion check:** explain at least three multilingual failure modes
  without making population-level claims from the small extension set.

---

## Parallel Speech-ML Systems Drill Track

Use the [Speech-ML Systems Drill Track](SPEECH_ML_SYSTEMS_DRILLS.md)
for three 30-minute drills per week. It covers implementation under time
pressure, gradient descent, transformer linear algebra and tensor shapes,
Whisper-style chunk processing, CTC versus RNN-T, profiling, and content versus
speaker/style representations. It reinforces first-principles understanding
without adding a second project or weakening the 56-day build.

---

## What the Compression Costs (read this once, accept it)

- **Scratch-encoder depth.** You will not hand-implement the full Conformer (macaron FFNs, full integration, scratch-vs-pretrained benchmark). You implement the two core modules and study the rest through the pretrained model's behavior. The theory blocks still cover the full architecture.
- **Capstone breadth.** Week 8 keeps the decision-relevant comparisons and drops nice-to-have ablations.
- **No slack.** At 6 sessions/week the plan has roughly one spare session per 10 days. A wasted week is not recoverable inside October — which is exactly what the safety valve is for.

If this trade stops feeling right mid-flight, the December calendar remains one decision away.
