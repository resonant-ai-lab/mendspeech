# MendSpeech Complete Learning and Research Roadmap

> **A 56-Day Systems & Research Curriculum for Selective Semantic Speech Restoration, Real-Time Streaming ASR, Calibrated Decisions, Boundary-Matched Reconstruction, and Direct Audio Repair Comparison.**

---

> [!IMPORTANT]
> **Timeline & Workload Realism:**  
> Eight weeks (56 days) is the foundational structure. A realistic execution window is **8 to 10 weeks** and roughly **150 to 185 focused engineering hours**. Do not sacrifice deep understanding to preserve an arbitrary calendar deadline.

---

## 1. Final Project Architecture & Flow

```
                      Damaged Audio Input
                               │
                SpeechDamageBench / Live Input
                               │
                     Streaming FastConformer
                               │
                 Alignment + Calibrated Uncertainty
                               │
            ┌──────────────────┴──────────────────┐
            ▼                                     ▼
   [ Preserve / Abstain ]                  [ Repair Spans ]
   Keep original audio                            │
                                   ┌──────────────┴──────────────┐
                                   ▼                             ▼
                          MendSpeech V1: Cascaded      Direct Audio Baseline:
                          Speaker-Conditioned TTS      Pretrained Latent /
                          + Boundary Matching          Codec Inpainting
                                   │                             │
                                   └──────────────┬──────────────┘
                                                  ▼
                                       Shared Evaluation Suite:
                               WER, Retained %, Speaker Similarity,
                               Latency, RTF, Seam Discontinuity
```

---

## 2. What the Revised Plan Changes
- **Explicit Real-Time Baseline:** The cascaded ASR $\rightarrow$ text $\rightarrow$ TTS path is designated as a low-latency systems baseline, not an exaggerated claim of state-of-the-art restoration.
- **Boundary Matching Layer:** Week 7 introduces short-time energy matching, local loudness equalization, room-tone handling, and equal-power crossfades with quantitative seam metrics.
- **Standalone `SpeechDamageBench`:** Packaged as an independent, deterministic, versioned Python library with seed-controlled degradations.
- **Direct Audio Inpainting Comparison:** Week 8 compares the cascaded baseline against a reproducible pretrained direct latent/codec audio model.
- **Honest Pacing:** Workload calibrated to 150–185 hours with risk hotspots flagged upfront.

---

## 3. Eight-Week Progression

| Week | Focus | Milestone | Weekly Plan Link |
| :--- | :--- | :--- | :--- |
| **Week 1** | Audio, Degradation, & Measurement Foundations | Build the audio laboratory and release `SpeechDamageBench` v0 as a standalone package. | [Week 1 Plan](Week_1_MendSpeech_Daily_Plan.md) |
| **Week 2** | ASR, CTC, Confidence, & Repair Localization | Build the recognition and uncertainty layer, plus a reusable Modal cloud execution pipeline. | [Week 2 Plan](Week_2_MendSpeech_Daily_Plan.md) |
| **Week 3** | Conformer From First Principles | Implement Conformer attention, convolutions, and Macaron feed-forwards from scratch in PyTorch. | [Week 3 Plan](Week_3_MendSpeech_Daily_Plan.md) |
| **Week 4** | FastConformer & Efficient Encoder Behavior | Profile subsampling, receptive fields, and establish a reproducible FastConformer baseline. | [Week 4 Plan](Week_4_MendSpeech_Daily_Plan.md) |
| **Week 5** | Streaming, Cache-Aware Inference, & Adaptive Context | Implement cache-aware streaming ASR and evaluate uncertainty-guided adaptive context spending. | [Week 5 Plan](Week_5_MendSpeech_Daily_Plan.md) |
| **Week 6** | Robustness, Fine-Tuning, RNN-T, & Calibration | Adapt the recognizer to damaged speech, explore RNN-T, and calibrate confidence scores. | [Week 6 Plan](Week_6_MendSpeech_Daily_Plan.md) |
| **Week 7** | TTS, Speaker Preservation, & Boundary-Matched Reconstruction | Build MendSpeech V1 cascaded selective repair with duration alignment and seam diagnostics. | [Week 7 Plan](Week_7_MendSpeech_Daily_Plan.md) |
| **Week 8** | Research Capstone: Cascaded vs. Direct Repair | Freeze benchmarks, run Pareto ablations, compare with direct audio inpainting, and publish report. | [Week 8 Plan](Week_8_MendSpeech_Daily_Plan.md) |

---

## 4. Realistic Workload & Risk Matrix

| Phase | Expected Effort | Risk Level | Main Challenges & Risk Mitigation |
| :--- | :--- | :--- | :--- |
| **Weeks 1 to 3** | 35 to 45 hours | **Low** | Core PyTorch, NumPy, signal processing, and tensor math. Keep local tests fast. Freeze the reference-transcripted corpus (≥30 utterances, ≥5 speakers) early so Week 2 WER is meaningful. |
| **Weeks 4 to 5** | 45 to 55 hours | **High** | NVIDIA NeMo framework configuration, streaming cache tensors, chunk masks, GPU timing, and Modal deployment. |
| **Week 6** | 25 to 35 hours | **Medium** | Data splits, fine-tuning stability, SpecAugment, ECE temperature scaling, and evaluation discipline. |
| **Weeks 7 to 8** | 40 to 50 hours | **Medium–High** | Speaker-conditioned TTS latency, seam artifact debugging, direct audio baseline integration, and research synthesis. The direct inpainting baseline must be chosen and smoke-tested in Week 2 — never defer model selection to Week 8. |
| **Total** | **150 to 185 hours** | — | *Do not rush through days without fulfilling the completion checks.* |

---

## 5. Daily Operating Protocol (2-Hour Core Session)

| Time | Activity | Rule |
| :--- | :--- | :--- |
| **25 min** | **Theory & Reading** | Read only the specific paper section or framework doc needed for today's task. |
| **65 min** | **Build & Experiment** | Write code, run one controlled experiment, change one variable at a time, save output. |
| **20 min** | **Research Notebook** | Document: *Question, Hypothesis, Method, Result, Surprise, Limitation, Next Step*. |
| **10 min** | **Commit & Explain** | Save code/artifacts, name outputs cleanly, explain what you learned aloud without notes. |

> [!TIP]
> **Handling Incomplete Tasks:** If debugging takes longer than 65 minutes, continue the exact same task in the next session rather than pretending the day is finished.
>
> **Timebox rule:** any day may consume at most two extra sessions (~6 hours total). After that, log the remaining work as *deferred*, land the day's core deliverable in its minimal working form, and move on. A working end-to-end pipeline beats a perfect week.

---

## 6. Hardware Strategy
- **Weeks 1 to 3:** Run locally on CPU. Only use GPU when scaling test runs.
- **Weeks 4 to 8:** Default to **Modal L4 (24GB VRAM)** for reproducible inference, streaming, fine-tuning, and benchmarks.
- **Hardware Consistency:** Keep hardware strictly fixed across any latency, RTF, or memory comparison.
- **Budget Reality:** Modal L4 costs roughly $0.38/hour; expect 30–60 GPU-hours across Weeks 4–8 (≈ **$15–30 total**). Batch experiments to avoid per-run cold-start overhead, and never use a larger GPU (L40S/A100) for any latency, RTF, or memory comparison.

---

## 7. Core Research Questions
1. *Can selective semantic repair improve intelligibility while retaining more original speech than full resynthesis?*
2. *Can calibrated ASR uncertainty guide streaming context spending so extra latency is consumed only when speech is degraded?*
3. *Can boundary-matching DSP techniques reduce audible seam artifacts in short-span TTS reconstruction?*
4. *In what specific acoustic regimes does the cascaded real-time path outperform or underperform direct latent/codec audio inpainting?*

---

## 8. Primary Resource Spine
- **Audio DSP:** PyTorch & TorchAudio documentation, Oppenheim/Schafer signal processing fundamentals.
- **ASR & CTC:** Graves et al. Connectionist Temporal Classification, NeMo CTC decoders.
- **Conformer:** Gulati et al., *Conformer: Convolution-augmented Transformer for Speech Recognition*.
- **FastConformer:** Rekesh et al., *FastConformer with Linearly Scalable Attention for Efficient Speech Recognition*.
- **Streaming ASR:** NVIDIA Stateful Conformer with Cache-Based Streaming Inference.
- **Transducer:** Graves RNN-T papers and NeMo RNN-T decoders.
- **TTS & Vocoders:** FastSpeech 2, HiFi-GAN, VITS papers.
- **Direct Audio Baseline:** Pretrained latent / codec audio inpainting model (e.g., VoiceCraft / Voicebox / AudioMAE / F5-TTS).
