# Revised Execution Plan (v2)

> **Status:** This document re-baselines the calendar and adds four portfolio add-on labs.
> The 56 day files remain the source of truth for daily content; this file governs **pacing, gates, and add-ons**.

---

## What Changed From v1

1. **Calendar re-baseline:** the 8-week calendar becomes milestone gates over roughly 18–20 weeks at a sustainable 5–6 evening sessions per week (realistic completion: mid-December for the core spine, add-ons landing by year-end).
2. **Day 40 redefined:** RNN-T stays as theory; the hands-on block is now an INT8 quantization lab on the Day 38 fine-tuned model (accuracy/latency/memory trade-offs). See [`days/day_40.md`](days/day_40.md).
3. **Four add-on labs added** (A–D below): diarization/VAD, serving deployment, a VLM fine-tune lab, and a voice-agent loop demo. Each is small (1–3 sessions) and slots in after a specific gate.
4. **Fallback rule made explicit** (see below) to protect the schedule without gutting learning.

Everything else — blueprint, metrics, ablations, definition of done — is unchanged.

---

## Session Protocol (v2)

- **Split sessions allowed:** a day's `Learn` block and its `Build`/`Experiment` blocks may happen in separate sittings on the same calendar day. Never start a build session without the Learn block read; never end one without a commit.
- **Cadence:** 5–6 build sessions per week plus one longer weekend buffer session for anything that slipped.
- **Timebox rule (unchanged):** maximum 2 extra sessions per day beyond the standard protocol.
- **Gates, not dates:** if a gate target date slips, re-date the remaining gates. Do not compress experiment quality to hit a date.

---

## Milestone Gates

| Gate | Days | Exit Evidence | Planned Target |
| :--- | :--- | :--- | :--- |
| **Gate 1** | 01–07 | Audio lab + `SpeechDamageBench` v0; frozen benchmark (≥30 transcripted utterances, ≥5 speakers, speaker-separated splits) | **Sep 6** |
| **Gate 2** | 08–14 | ASR baseline + confidence + Modal pipeline; direct inpainting baseline selected and smoke-tested. **Then Add-on A** | **Sep 27** |
| **Gate 3** | 15–21 | Scratch Conformer completed as a **learning artifact** (Day 20 benchmark optional) | **Oct 11** |
| **Gate 4** | 22–28 | Reproducible FastConformer baseline + subsampling/efficiency profiling. **Fallback decision point** | **Oct 25** |
| **Gate 5** | 29–35 | Cache-aware streaming ASR with adaptive-context results. **Then Add-on B** | **Nov 15** |
| **Gate 6** | 36–42 | Robust fine-tuning + Day 40 quantization + calibration; frozen Week 6 benchmark. **Then Add-on C** | **Dec 6** |
| **Gate 7** | 43–49 | MendSpeech V1 complete: selective TTS repair with boundary matching and seam diagnostics. **Then Add-on D** | **Dec 27** |
| **Gate 8** | 50–56 | Capstone: cascaded vs direct repair, Pareto ablations, final report | **Jan 17** |

---

## Fallback Rule (decided in advance)

If **Gate 4 finishes more than two weeks past its target date**, switch Weeks 5–6 to a pretrained NeMo FastConformer checkpoint instead of the scratch encoder. Weeks 3–4 have already delivered their learning value by then; the shipped, measured system is what matters for everything after Gate 4.

---

## Add-On Labs

Small, self-contained labs that broaden the portfolio beyond the core project. Each is optional-if-under-pressure but strongly recommended, and each produces a measurable artifact.

### Add-on A — Diarization & VAD Lab *(after Gate 2, ~2 sessions)*
- **Build:** run pyannote (or equivalent) speaker diarization + voice activity detection over the frozen SpeechDamageBench set, clean and damaged variants.
- **Measure:** diarization error rate clean vs damaged; VAD boundary shift under dropouts.
- **Artifacts:** `results/addon_a_diarization_der.csv`, `docs/addon_a_notes.md`.
- **Compute:** Modal L4 or local CPU.

### Add-on B — Serving Deployment *(after Gate 5, ~2 sessions)*
- **Build:** wrap the streaming ASR in a FastAPI service, containerize with Docker, deploy on Modal.
- **Measure:** RTF p50/p95 under ~8 concurrent streams, cold-start time, peak GPU memory.
- **Artifacts:** `infra/serve/` (Dockerfile + app), `results/addon_b_serving.csv`.

### Add-on C — VLM Fine-Tune Lab *(after Gate 6, 1 weekend + 1 session)*
- **Purpose:** a second-modality artifact proving training/eval discipline transfers (document understanding).
- **Build:** LoRA fine-tune a small open VLM (Qwen2-VL-2B or SmolVLM) on a small form/document field-extraction set; build a strict eval.
- **Measure:** exact-match field accuracy before vs after fine-tuning.
- **Artifacts:** `experiments/addon_c_vlm/`, `results/addon_c_vlm_extraction.csv`.
- **Compute:** Modal L4.

### Add-on D — Voice-Agent Loop Demo *(after Gate 7, ~2 sessions)*
- **Build:** minimal end-to-end loop — streaming ASR → LLM → TTS (Week 7 model or API) — with one recorded demo clip.
- **Measure:** per-stage latency budget (ASR / LLM / TTS) and end-to-end response time.
- **Artifacts:** `app/voice_agent_demo.py`, `results/addon_d_latency_budget.csv`, demo clip in `results/`.

---

## Completion Definition

The original blueprint's Definition of Done still governs the project. Under v2, the plan is complete when:
1. All 56 days are executed (with the Day 40 quantization substitution),
2. Add-ons A, B, and D are shipped (C is the first thing to cut if the schedule collapses),
3. The Week 8 report is published with frozen numbers.
