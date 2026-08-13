# MendSpeech Project Blueprint

> **Selective Semantic Speech Restoration Under Real-Time Constraints, with Cascaded and Direct Audio Repair Baselines.**

---

### Core Principle
> *Preserve trustworthy original speech, spend compute only where uncertainty justifies it, and never hide architectural limitations.*

---

## 1. Product Behavior
- Accept microphone audio or an uploaded recording.
- Optionally generate controlled damage through `SpeechDamageBench`.
- Transcribe incrementally with cache-aware FastConformer inference.
- Align confidence and uncertainty to time.
- Classify intervals as **Preserve**, **Inspect**, **Repair**, or **Abstain**.
- **For MendSpeech V1:** Reconstruct only repair intervals with speaker-conditioned TTS, then apply acoustic boundary matching before stitching.
- **For the Research Comparison:** Run the same damaged spans through a pretrained direct latent or codec audio inpainting baseline.
- Show exactly which milliseconds were preserved, reconstructed, or left unrepaired.

---

## 2. Two Repair Architectures

| Dimension | MendSpeech V1: Cascaded Baseline | Direct Audio Inpainting Baseline |
| :--- | :--- | :--- |
| **Pipeline** | Streaming ASR $\rightarrow$ Calibrated Uncertainty $\rightarrow$ Repair Policy $\rightarrow$ Speaker-Conditioned TTS $\rightarrow$ Duration Alignment $\rightarrow$ Boundary Matching $\rightarrow$ Waveform Stitching | Damaged Audio $\rightarrow$ Latent/Codec Representation $\rightarrow$ Masked/Conditioned Reconstruction $\rightarrow$ Restored Audio |
| **Key Strengths** | Deterministic semantic control and a practical, low-latency streaming systems path. | Preserves acoustic context, prosody, inflection, breathing, and room reverberation without a text bottleneck. |
| **Key Limitations** | Discards pitch, emotion, breathing, co-articulation, and other acoustic context at the text interface. | Requires higher compute, is harder to control semantically, and is less suited for strict low-latency streaming constraints. |

---

## 3. Boundary Matching Layer
- Select a repair window with context padding.
- Match generated duration to the target interval.
- Compare short-time energy around both boundaries.
- Match local loudness before mixing.
- Estimate simple spectral mismatch and room tone difference.
- Compare linear and equal-power crossfades.
- Record seam diagnostics so subjective listening is not the only evidence.

---

## 4. SpeechDamageBench
`SpeechDamageBench` is designed as a standalone, versioned package, not a private utility inside MendSpeech.

| Damage Family | Controlled Variables | Purpose |
| :--- | :--- | :--- |
| **Additive Noise** | SNR, noise type, random seed | Test masking robustness. |
| **Clipping** | Threshold, severity | Test lost peaks and saturation. |
| **Bandwidth Limits** | Sample rate, filter settings | Simulate narrow channels (telephony, codecs). |
| **Dropouts** | Span length, frequency, random seed | Simulate missing speech and packet loss. |
| **Reverberation** | Impulse response / room severity | Test temporal smearing. |

> [!NOTE]
> Every generated sample records corruption name, severity, random seed, clean source ID, parameter values, and package version.

---

## 5. Research Console Metrics

| Metric | Why It Matters |
| :--- | :--- |
| **WER & CER** | Recognition correctness. |
| **Latency Percentiles (p50, p90, p99)** | Responsiveness and tail behavior under real-time constraints. |
| **Real-Time Factor (RTF)** | Measures whether processing keeps up with live speech. |
| **GPU Memory** | Captures deployment cost and memory pressure. |
| **Repair Percentage** | Measures how much of the audio was regenerated. |
| **Original Retained Percentage** | Measures original audio preservation directly. |
| **Speaker Similarity Proxy** | Imperfect signal for identity consistency across repairs. |
| **Calibration (ECE / Brier)** | Tests whether confidence values support reliable policy decisions. |
| **Boundary Energy Discontinuity** | Quantitative signal for stitching and seam quality. |
| **Abstention Outcomes** | Measures whether the system avoids hallucinating unrecoverable content. |

---

## 6. Required Ablations
- **Context Policy:** Fixed low lookahead vs. fixed high lookahead vs. adaptive context.
- **Uncertainty:** Raw confidence vs. calibrated confidence (temperature scaling).
- **Threshold Policies:** Preserve, Balanced, and Rescue repair thresholds.
- **Granularity:** Selective span repair vs. full utterance resynthesis.
- **Stitching Quality:** Naive waveform stitching vs. boundary-matched stitching.
- **ASR Robustness:** Base ASR vs. robustness-adapted (fine-tuned) ASR.
- **Architecture:** Cascaded V1 vs. direct latent/codec audio inpainting baseline.
- **Span Sensitivity:** Short vs. long missing dropout spans.
- **Clean Speech Regression:** Ensuring already clean speech is not degraded by the pipeline.

---

## 7. Repository Target Structure

```text
mendspeech/
├── src/
│   ├── audio/          # Waveform loaders, STFT, log-Mel, normalization
│   ├── asr/            # FastConformer, CTC, transducer, confidence, calibration
│   ├── streaming/      # Cache-aware runners and lookahead controllers
│   ├── controller/     # Repair policies, adaptive context, abstention logic
│   ├── tts/            # Synthesis and speaker conditioning
│   ├── repair/         # Timing alignment, boundary matching, crossfade stitching
│   ├── baselines/      # Pretrained direct latent / codec audio inpainting
│   ├── metrics/        # WER, CER, RTF, seam discontinuity, speaker similarity
│   └── bench/          # Benchmark harnesses and runners
├── speechdamagebench/  # Standalone benchmark package
│   ├── speechdamagebench/
│   ├── tests/
│   ├── presets/
│   ├── pyproject.toml
│   └── README.md
├── infra/              # Modal cloud execution scripts and container definitions
├── app/                # Live interactive demo and research console
├── experiments/        # Frozen experiment configs
├── results/            # Run outputs, logs, and benchmark tables
└── reports/            # Research report, figures, and failure casebooks
```

---

## 8. Definition of Done
1. A new user can reproduce benchmark results with documented, single-command sequences.
2. The interactive demo visually highlights preserved, repaired, and abstained millisecond spans.
3. Boundary matching is quantitatively measured (discontinuity scores), not just evaluated by ear.
4. The final research report includes at least one surprising result and one limitation that materially constrains claims.
5. The system explicitly abstains from hallucinating speech when audio is too damaged.
6. The direct audio baseline is evaluated fairly, with clear documentation of where it outperforms the cascaded path.
7. You can explain every major model and systems component from first principles without relying on library names as explanations.
