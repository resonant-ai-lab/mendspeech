# Day 04: Build SpeechDamageBench as a standalone package

> **Week 1 • Day 4 of 7**  
> **Navigation:** [← Day 03](day_03.md) | [Week 1 Plan](../Week_1_MendSpeech_Daily_Plan.md) | [Master Index](../INDEX.md) | [Day 05 →](day_05.md)

---

### Compute Target
`Local CPU`

> **Carry-forward from Day 01:** if `data/benchmark/` is still missing a
> labeled set, start it in this session. Day 07 only *freezes* the set; it
> does not collect it. Target: public transcripted speech (e.g. LibriSpeech
> `dev-clean`), relative paths, a `transcript` column, ≥5 speaker IDs.
> Reaching the full ≥30 utterances can finish on Day 05 — do not wait until
> Day 07.

---

### 1. Learn
- Deterministic corruption design and seed control.
- Additive noise, clipping, bandwidth limitation, dropouts, and reverberation.
- Why a benchmark should be reusable outside the main application.
- Versioned severity presets and manifest metadata.

---

### 2. Build in MendSpeech
- Create SpeechDamageBench as a **nested standalone package**. Do **not**
  overwrite the repo-root `pyproject.toml` (that file belongs to `mendspeech`).
- Implement noise, clipping, bandwidth reduction, dropout, and simple reverberation modules.
- Add a seed controlled configuration object and a small command line entry point.
- Record corruption name, severity, seed, parameters, and clean source id for every output.
- Presets live in `speechdamagebench/speechdamagebench/presets.py`. If you
  also want YAML, keep it inside the package (`presets/damage_levels.yaml`)
  so there is one source of truth.

---

### 3. Experiment and Measure
- Generate mild, medium, and severe examples from the same clean sentence.
- Reproduce the exact same damaged waveform from the same seed.
- Change only the seed and verify that the corruption changes while all configured parameters remain fixed.

---

### 4. Required Output Artifacts
- `speechdamagebench/pyproject.toml` (package name `speechdamagebench`; do not touch repo-root `pyproject.toml`)
- `speechdamagebench/speechdamagebench/audio_damage.py`
- `speechdamagebench/speechdamagebench/presets.py`
- `speechdamagebench/speechdamagebench/cli.py`
- `speechdamagebench/tests/test_determinism.py`
- `data/benchmark/` begun if still missing (manifest with relative paths + transcripts)

---

### 5. Completion Check
> **Definition of Done for Day 04:**  
> Another project can install SpeechDamageBench and regenerate the same damaged
clip from a manifest entry.

---

### 6. Study Method & Protocol
25 minutes focused reading. 65 minutes implementation or controlled experiment. 20 minutes research
notebook. 10 minutes commit and explain the result aloud. When debugging is incomplete, continue the
same task in the next session instead of pretending the day is finished.

---

### 7. References & Resources
- PyTorch and TorchAudio audio processing documentation
- A practical digital signal processing reference for STFT and filterbanks
