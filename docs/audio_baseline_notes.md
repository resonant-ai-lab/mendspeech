# Day 01: Waveforms, Sampling, and Acoustic Baseline Notes

> **MendSpeech Research Notes • Week 1 (Audio Foundations)**  
> **Date:** 2026-08-14 • **Hardware:** Local CPU • **Environment:** Python 3.13 / PyTorch / TorchAudio

---

## 1. Physical Waveforms & Digital Representation

Audio is continuous pressure fluctuations propagating through a medium (air). To process speech digitally, continuous acoustic signals must be digitized through two orthogonal discretization processes:

1. **Temporal Discretization (Sampling):** Converting the continuous time axis $t$ into discrete time indices $n = 0, 1, 2, \dots$ at a fixed sampling frequency $f_s$:
   $$x[n] = x(n \cdot T_s) = x\left(\frac{n}{f_s}\right)$$
2. **Amplitude Discretization (Quantization):** Mapping continuous voltage levels into a finite number of discrete levels determined by the bit depth $B$ (e.g., 16-bit integer PCM has $2^{16} = 65,536$ levels).

---

## 2. Nyquist-Shannon Sampling Theorem & Speech Frequency Bounds

### The Theorem
To perfectly reconstruct a continuous band-limited signal without **aliasing** (frequency fold-over distortion), the sampling frequency $f_s$ must be strictly greater than twice the highest frequency component $f_{max}$ present in the signal:
$$f_s > 2 \cdot f_{max} \implies f_{Nyquist} = \frac{f_s}{2}$$

Any spectral energy above $f_{Nyquist}$ will fold back (alias) into the lower audible band as unnatural metallic distortion unless eliminated by an analog anti-aliasing low-pass filter prior to sampling.

### Spectral Content of Human Speech

```
 0 Hz            300 Hz          3.4 kHz          8.0 kHz          12.0 kHz         20.0 kHz
  │                │                │                │                │                │
  ▼────────────────▼────────────────▼────────────────▼────────────────▼────────────────▼
  [ Fundamental F0 ] [ Formants F1-F3 ] [ Formants F4-F5 ] [ Sibilance/Fricatives ] [ Air / Harmonics ]
  (Pitch: 80-300Hz)  (Vowels: /a/,/i/)   (Speaker timbre)   (Consonants: /s/, /f/, /th/) (High fidelity)
  └─────────────────────────────────┘
      Narrowband Telephony (8 kHz)
  └──────────────────────────────────────────────────┘
            Standard Speech ASR/TTS (16 kHz)
  └────────────────────────────────────────────────────────────────────────────────────┘
                              Full-Band Studio Audio (48 kHz)
```

---

## 3. Sampling Rate Trade-Off Analysis (Measured Data)

Using reference clip [`data/clean_16k/clean_01.wav`](../data/clean_16k/clean_01.wav), we measured the physical and acoustic properties across 4 standardized sample rates:

| Sample Rate ($f_s$) | Nyquist Cutoff ($f_s / 2$) | Number of Samples (6.0s) | Uncompressed Size (16-bit PCM) | Bandwidth & Phonetic Preservation |
| :--- | :--- | :--- | :--- | :--- |
| **8,000 Hz** (8 kHz) | **4,000 Hz** (4 kHz) | 48,000 | 93.8 KB | **Narrowband Telephony:** Captures core vowels ($F_1, F_2$), but severely attenuates voiceless fricatives (`/s/`, `/f/`, `/th/`, `/z/`, `/sh/`). Speech sounds muffled. |
| **16,000 Hz** (16 kHz) | **8,000 Hz** (8 kHz) | 96,000 | 187.6 KB | **Speech Standard (ASR/TTS Baseline):** Retains 99%+ of human phonetic intelligibility and consonant distinction while saving $3\times$ compute and memory compared to 48 kHz. |
| **24,000 Hz** (24 kHz) | **12,000 Hz** (12 kHz) | 144,000 | 281.3 KB | **Wideband Broadcast / Neural TTS:** Standard for expressive TTS models (e.g. VITS, HiFi-GAN) to reproduce natural breathiness and speaker timbre. |
| **48,000 Hz** (48 kHz) | **24,000 Hz** (24 kHz) | 288,000 | 562.6 KB | **Full-Band Studio Audio:** Covers beyond the entire human hearing range ($20 \text{ Hz} - 20 \text{ kHz}$). Essential for music mastering, but unnecessarily wasteful for real-time speech ASR. |

---

## 4. Energy & Amplitude Metrics

### 1. Root Mean Square (RMS) Energy
RMS measures the effective signal power over duration $N$:
$$\text{RMS} = \sqrt{\frac{1}{N}\sum_{n=1}^{N} x[n]^2}$$
Expressed in decibels relative to full scale (dBFS):
$$\text{RMS}_{\text{dBFS}} = 20 \log_{10}(\text{RMS})$$

*Speech Standard:* Clean speech is typically normalized between **$-23 \text{ dBFS}$ and $-18 \text{ dBFS}$** (EBU R128 / ITU-R BS.1770 standards) to provide sufficient dynamic headroom without digital clipping.

### 2. Peak Amplitude & Digital Clipping
$$\text{Peak} = \max_n |x[n]|$$
- In float32 representations, audio is bounded to $[-1.0, 1.0]$.
- When amplitude reaches or exceeds $\pm 1.0$, the waveform flattens (digital clipping), creating harsh odd harmonic distortion and destroying spectral peak information.
- Our loader implements **Headroom Protection** (`peak_limit=0.95`, $\approx -0.45\text{ dBFS}$) during RMS normalization.

---

## 5. Standardized Clean Dataset Manifest

The 5 baseline clean speech clips generated today are tracked in [`data/clean_manifest.csv`](../data/clean_manifest.csv):

| Clip ID | Speaker ID | Duration | Sample Rate | Channels | RMS (dBFS) | Peak (dBFS) | Clipping Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `clean_01` | `speaker_female_01` | 6.00s | 16,000 Hz | 1 (Mono) | -18.52 dB | -2.19 dB | 0.00% |
| `clean_02` | `speaker_female_01` | 6.00s | 16,000 Hz | 1 (Mono) | -18.83 dB | -3.72 dB | 0.00% |
| `clean_03` | `speaker_male_01` | 6.50s | 16,000 Hz | 1 (Mono) | -20.02 dB | -3.95 dB | 0.00% |
| `clean_04` | `speaker_male_01` | 6.50s | 16,000 Hz | 1 (Mono) | -23.32 dB | -7.21 dB | 0.00% |
| `clean_05` | `speaker_male_02` | 6.00s | 16,000 Hz | 1 (Mono) | -28.83 dB | -10.38 dB | 0.00% |

---

## 6. Key Takeaway for MendSpeech

> **Why MendSpeech standardizes on 16 kHz Mono Float32:**
> 1. FastConformer, CTC decoders, and acoustic feature extractors (80-channel log-Mel) require 16 kHz input.
> 2. Frequencies between 0 Hz and 8 kHz contain virtually all phonetic formant transitions required for ASR uncertainty localization and repair policy classification.
> 3. Resampling higher-rate audio (24 kHz / 48 kHz) to 16 kHz must use band-limited sinc interpolation with anti-aliasing filters to prevent high-frequency folding artifacts from polluting the log-Mel spectrogram.
