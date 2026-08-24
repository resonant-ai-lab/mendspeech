# Metric Limitations

Week 1, Day 5. Every metric below reduces a complex perceptual phenomenon to
one scalar number. Each is useful for the specific failure mode it detects and
blind to others. The results in `results/week1_damage_metrics.csv` illustrate
these limitations on real speech.

## RMS Energy (dB)

**What it says:** overall loudness of a waveform. Useful for detecting gain
changes or energy loss after corruption.

**What it fails to say:** anything about quality, intelligibility, or
distortion type. A heavily reverberated clip and a clean clip can share the
same RMS while sounding very different. It also collapses all temporal detail:
you cannot tell whether energy is concentrated in speech or spread across noise.

## Peak Level (dBFS)

**What it says:** the single loudest sample. Useful for detecting digital
saturation and headroom violations.

**What it fails to say:** how distortion is distributed over time. Clipping
flattens many samples near the peak; peak level alone does not reveal how much
harmonic distortion was introduced. A brief transient spike can dominate peak
while the rest of the clip sounds fine.

## Signal-to-Noise Ratio (SNR, dB)

**What it says:** how much residual energy separates corrupted from clean,
expressed relative to signal power. Meaningful when corruption is additive
(e.g., background noise).

**What it fails to say:** quality for any non-additive distortion. Our data
shows this clearly:

- **Reverberation** produces negative SNR (-8 to -3 dB), implying massive
  error. Yet mild reverb at RT60 = 0.15 s sounds natural to human listeners.
  SNR treats correlated reflections as pure noise.
- **Bandwidth reduction** yields SNR around 9-13 dB even at mild severity
  (4 kHz cutoff). Perceptually, speech remains highly intelligible because
  consonant information survives below 4 kHz. SNR penalizes all removed high-
  frequency energy equally regardless of its perceptual importance.
- **Clipping** can return the sentinel value (100 dB) when no sample exceeds
  the threshold, meaning zero measurable change. At other clips it produces
  moderate SNR values that do not map cleanly to perceived harshness.

SNR assumes the difference between clean and corrupted is uncorrelated additive
noise. Every non-additive operator violates that assumption.

## Log-Mel Spectral Distance

**What it says:** how much frequency content changed between clean and
corrupted, averaged over Mel bands and time frames. Captures timbre shifts
better than waveform-level metrics.

**What it fails to say:** temporal structure, phase relationships, and
intelligibility. A dropout removes samples abruptly but produces a small
mel-distance because only a few frames change. Reverberation smears energy
across time without changing average spectral shape much, so mel-distance
understates the perceived echo. Two signals with similar average spectra can
sound completely different if their phase or temporal envelopes differ.

## Why No Single Metric Is Enough

The table below summarizes what each metric detects well versus where it is
misleading, using our actual Week 1 results as evidence.

| Metric | Best at detecting | Misleading for |
|--------|-------------------|----------------|
| RMS | Loudness/gain changes | Distortion type, quality |
| Peak | Saturation/headroom | Distribution over time |
| SNR | Additive noise | Reverb, bandwidth loss, clipping |
| Log-Mel distance | Timbre/frequency changes | Dropouts, temporal effects |

Later weeks add downstream metrics (WER/CER from ASR) that measure
intelligibility rather than signal fidelity. Together these layers give a more
honest picture of damage severity than any single scalar.
