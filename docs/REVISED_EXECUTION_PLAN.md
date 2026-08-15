# Revised Execution Plan (v1 — October Calendar)

> **Status:** This document re-baselines the calendar to an **October 25 completion** and adds four add-on labs (one deferred to November).
> The 56 day files remain the source of truth for daily content; this file governs **pacing, gates, compression decisions, and add-ons**.

---

## What Changed From the Original 8-Week Plan

1. **Completion target moved from December to October 25** (buffer through October 31). This requires a mandatory **6 sessions per week** cadence and three scope compressions (below).
2. **Weeks 3–4 merged into a 10-session "Encoder Block."** Precise mapping lives in the Week 3 and Week 4 guides (v1 Compression Maps): Days 15, 16, 18, 19, 21 and Days 23, 24, 25, 26, 28 run as sessions; Day 17 becomes learn-only (its macaron build moves into Day 18); Day 20 is dropped as a session; Day 22 merges into Day 23; Day 27 folds into Day 28. Everything downstream uses pretrained NeMo FastConformer. Rationale: the original plan already classified the scratch encoder as a *learning artifact*; jobs hire the shipped, measured system.
3. **Week 8 compressed to 5 sessions** (mapping in the Week 8 guide): Days 52+53 merge into one combined ablation session, Days 55+56 merge into one report-plus-demo session; the span-sensitivity ablation drops. Keeps the core cascaded-vs-direct comparison, the clean-speech regression check, and the report.
4. **Add-on C (VLM lab) deferred to November**, post-completion. It serves a different door and must not compete with the October finish.
5. **Safety valve:** if two full weeks are missed, the December calendar automatically applies again — no renegotiation, no guilt, just re-date the gates.

Everything else — blueprint, metrics, definition of done, split-session protocol — is unchanged.

---

## Session Protocol (unchanged rules, stricter cadence)

- **Cadence: 6 sessions per week, mandatory.** Five weekday evenings + Saturday. **Sunday is recovery-only:** catch up a missed session or rest. Never bank on Sunday for new material.
- **Split sessions allowed:** a day's `Learn` block and its `Build`/`Experiment` blocks may happen in separate sittings on the same calendar day. Never start a build session without the Learn block read; never end one without a commit.
- **Theory blocks are non-negotiable.** Under compression they are the first thing schedule pressure attacks and the last thing that can be cut — they are what makes the artifacts defensible.
- **Timebox rule (unchanged):** maximum 2 extra sessions per day.

---

## Milestone Gates (October calendar)

| Gate | Days | Exit Evidence | Target |
| :--- | :--- | :--- | :--- |
| **Gate 1** | 02–07 | Audio lab + `SpeechDamageBench` v0; frozen benchmark (≥30 transcripted utterances, ≥5 speakers, speaker-separated splits) | **Aug 23** |
| **Gate 2** | 08–14 | ASR baseline + confidence + Modal pipeline; inpainting baseline smoke-tested. **Then Add-on A** (weekend) | **Sep 1** |
| **Gate 3** | 15–28 (compressed to 10 sessions) | **Encoder Block:** scratch attention, convolution, and macaron modules with shape/gradient tests; pretrained FastConformer baseline reproducing reference WER; subsampling profiling; top-3 failure casebook | **Sep 13** |
| **Gate 4** | 29–35 | Cache-aware streaming ASR with adaptive-context results. **Then Add-on B** (weekend) | **Sep 27** |
| **Gate 5** | 36–42 | Robust fine-tuning + Day 40 quantization + calibration; frozen Week 6 benchmark | **Oct 3** |
| **Gate 6** | 43–49 | MendSpeech V1 complete: selective TTS repair, boundary matching, seam diagnostics. **Then Add-on D** (weekend) | **Oct 18** |
| **Gate 7** | 50–56 (compressed to 5 sessions) | Capstone: cascaded vs direct repair, core Pareto ablation, clean-speech regression check, final report | **Oct 25** |

Buffer: October 26–31 for slippage, report polish, and demo recording.

---

## Add-On Labs

### Add-on A — Diarization & VAD Lab *(Gate 2 weekend, ~2 sessions)*
- **Build:** pyannote (or equivalent) diarization + VAD over the frozen SpeechDamageBench set, clean and damaged variants.
- **Measure:** diarization error rate clean vs damaged; VAD boundary shift under dropouts.
- **Artifacts:** `results/addon_a_diarization_der.csv`, `docs/addon_a_notes.md`.

### Add-on B — Serving Deployment *(Gate 4 weekend, ~2 sessions)*
- **Build:** FastAPI service around the streaming ASR, Dockerized, deployed on Modal.
- **Measure:** RTF p50/p95 under ~8 concurrent streams, cold-start time, peak GPU memory.
- **Artifacts:** `infra/serve/`, `results/addon_b_serving.csv`.

### Add-on D — Voice-Agent Loop Demo *(Gate 6 weekend, ~2 sessions)*
- **Build:** streaming ASR → LLM → TTS loop (Week 7 model or API), one recorded demo clip.
- **Measure:** per-stage latency budget and end-to-end response time.
- **Artifacts:** `app/voice_agent_demo.py`, `results/addon_d_latency_budget.csv`, demo clip.

### Add-on C — VLM Fine-Tune Lab *(DEFERRED to November, post-completion)*
- LoRA fine-tune a small open VLM (Qwen2-VL-2B or SmolVLM) on form/document field extraction with a strict eval. Runs after Gate 7; it must not compete with the October finish.

---

## What the Compression Costs (read this once, accept it)

- **Scratch-encoder depth.** You will not hand-implement the full Conformer (macaron FFNs, full integration, scratch-vs-pretrained benchmark). You implement the two core modules and study the rest through the pretrained model's behavior. The theory blocks still cover the full architecture.
- **Capstone breadth.** Week 8 keeps the decision-relevant comparisons and drops nice-to-have ablations.
- **No slack.** At 6 sessions/week the plan has roughly one spare session per 10 days. A wasted week is not recoverable inside October — which is exactly what the safety valve is for.

If this trade stops feeling right mid-flight, the December calendar remains one decision away.
