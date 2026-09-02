# Week 8 Direct Audio Inpainting Baseline Selection & Install Notes

> **Document Status:** Day 08 Artifact (Week 2, Day 1)  
> **Objective:** Evaluate and document public, installable direct audio inpainting baselines for comparison against MendSpeech's cascaded (ASR $\to$ TTS) selective repair in Week 8.

---

## 1. Context & Architectural Comparison

In Week 8, MendSpeech evaluates a central hypothesis:
$$\text{Cascaded Selective Repair (ASR uncertainty } \to \text{ targeted TTS stitch)}$$
$$\text{vs.}$$
$$\text{Direct Audio Inpainting (end-to-end masked neural audio reconstruction)}$$

To make this comparison scientifically sound and reproducible, the inpainting baseline must satisfy three constraints:
1. **Publicly available and installable:** Clean open-source weights and code (Voicebox has no public checkpoint; F5-TTS is pure TTS text-to-speech, not masked audio inpainting).
2. **Deterministic or controllable interface:** Accepts a 16 kHz waveform and a time/sample mask indicating the damaged span.
3. **Reproducible compute requirements:** Runs inference on CPU or a single Modal L4 GPU.

---

## 2. Selected Primary Baseline: VoiceFixer

### Background
- **Paper:** *VoiceFixer: Toward General Speech Restoration with Neural Vocoder* (Liu et al., Interspeech 2022).
- **GitHub / Package:** `pip install voicefixer` / `https://github.com/haoheliu/voicefixer`
- **Architecture:** ResUNet backbone with TFi-Film conditioning to reconstruct corrupted spectrogram representations, followed by a pretrained HiFi-GAN neural vocoder to synthesize time-domain audio.
- **Why it fits:** Handles severe speech degradation including additive noise, clipping, low-pass bandwidth limitation, and packet dropout / missing spans without requiring a text transcript.

### Installation
```bash
pip install voicefixer
```

### Usage Pattern
```python
from voicefixer import VoiceFixer

vf = VoiceFixer()
# mode 0: original speech restoration; mode 1: add vocal harmonics; mode 2: complete dereverberation & inpainting
vf.restore(input="damaged.wav", output="restored.wav", mode=0, cuda=False)
```

---

## 3. Alternative Candidate: AudioLDM / AudioLDM2 (Inpainting Mode)

### Background
- **Paper:** *AudioLDM 2: Learning Holistic Audio Generation with Self-supervised Pretraining* (Liu et al., 2023).
- **Hugging Face / Package:** `diffusers`, `pip install diffusers transformers`
- **Architecture:** Latent Diffusion Model operating on Mel-spectrograms conditioned on mask and context.
- **Trade-off:** High synthesis quality for general audio, but higher latency, larger model size (~1.5 GB), and diffusion sampling stochasticity.

---

## 4. Deterministic Fallback Baseline: Spectrogram Masked Inpainting

If external neural inpainting models introduce dependency conflicts (e.g. PyTorch 2.x C extensions) during Week 8 integration, MendSpeech provides a standalone, zero-external-dependency mathematical fallback:

### Architecture
1. **STFT Analysis:** 25 ms window / 10 ms hop (400 / 160 samples) at 16 kHz.
2. **Time-Frequency Mask Interpolation:** Identify damaged frame indices $[t_{start}, t_{end}]$ from the damage manifest. Replace damaged log-magnitude bins using Hermite cubic spline interpolation across undamaged left and right temporal context.
3. **Phase Reconstruction:** Localized Griffin-Lim algorithm (GLA) or Griffin-Lim with momentum (FastGLA) applied strictly to the masked span while preserving the original phase of clean context.
4. **Inverse STFT:** Overlap-add reconstruction to 16 kHz time domain.

### Advantages of the Fallback
- Zero external network dependencies or unmaintained checkpoint risks.
- Bit-exact determinism across seeds.
- Runs in milliseconds on local CPU.
- Establishes a true signal-processing floor for Week 8: proves whether neural inpainting actually beats classical mathematical interpolation.
