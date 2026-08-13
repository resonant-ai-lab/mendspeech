# Day 51: Release SpeechDamageBench v1 and freeze evaluation

> **Week 8 • Day 2 of 7**  
> **Navigation:** [← Day 50](day_50.md) | [Week 8 Plan](../Week_8_MendSpeech_Daily_Plan.md) | [Master Index](../INDEX.md) | [Day 52 →](day_52.md)

---

### Compute Target
`Local CPU`

---

### 1. Learn
- Severity grids.
- Speaker separated evaluation.
- Seed control and deterministic manifests.
- Package versioning and reproducibility.
- Clean regression cases that must remain untouched.

---

### 2. Build in MendSpeech
- Finalize the independent SpeechDamageBench package with noise, clipping, bandwidth, dropout, and reverberation presets.
- Generate the frozen test matrix and lock manifest checksums.
- Add an installation command and a one command example that reproduces one benchmark item.

---

### 3. Experiment and Measure
- Reinstall the package in a clean environment.
- Regenerate a sample from the manifest and verify its checksum.
- Validate that clean references remain unchanged.

---

### 4. Required Output Artifacts
- `speechdamagebench/`
- `speechdamagebench/README.md`
- `speechdamagebench/CHANGELOG.md`
- `benchmarks/speechdamagebench_manifest.csv`
- `benchmarks/README.md`

---

### 5. Completion Check
> **Definition of Done for Day 51:**  
> SpeechDamageBench is independently installable, deterministic, versioned, and
usable without MendSpeech.

---

### 6. Study Method & Protocol
25 minutes focused reading. 65 minutes implementation or controlled experiment. 20 minutes research
notebook. 10 minutes commit and explain the result aloud. When debugging is incomplete, continue the
same task in the next session instead of pretending the day is finished.

---

### 7. References & Resources
- Your frozen protocol and prior results
- A reproducible pretrained direct latent or codec audio inpainting baseline
- Primary papers only when needed to interpret a result
