# SpeechDamageBench

Standalone, seed-controlled speech damage. Install it without MendSpeech
and regenerate the same damaged clip from a manifest row.

## Install

```bash
pip install -e ./speechdamagebench
```

## Damage one file

```bash
speechdamagebench damage \
  --in clean.wav \
  --out damaged.wav \
  --corruption additive_noise \
  --severity medium \
  --seed 7 \
  --source-id clean_01
```

The JSON printed to stdout *is* the manifest entry: corruption, severity,
seed, parameters, source id, package version. Feed those fields back in
and the waveform matches.

Corruptions: `additive_noise`, `clipping`, `bandwidth`, `dropout`, `reverberation`.
Severities: `mild`, `medium`, `severe`.

## From Python

```python
from speechdamagebench import DamageConfig, apply_damage, load_mono

wave, sr = load_mono("clean.wav", target_sr=16000)
damaged, record = apply_damage(
    wave,
    sr,
    DamageConfig("additive_noise", "medium", seed=7, source_id="clean_01"),
)
```

Same seed → same waveform. Change only the seed → realization changes,
configured SNR / threshold / cutoff stay fixed.
