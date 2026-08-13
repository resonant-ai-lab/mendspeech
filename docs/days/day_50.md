# Day 50: Freeze research questions and baselines

> **Week 8 • Day 1 of 7**  
> **Navigation:** [← Day 49](day_49.md) | [Week 8 Plan](../Week_8_MendSpeech_Daily_Plan.md) | [Master Index](../INDEX.md) | [Day 51 →](day_51.md)

---

### Compute Target
`Local CPU for planning, Modal L4 for
dry run`

---

### 1. Learn
- Primary question: can selective semantic repair improve intelligibility while preserving more original speech than full resynthesis?
- Secondary question: can uncertainty guided context allocation improve the latency versus accuracy operating point?
- Architecture question: when does cascaded ASR plus TTS repair beat or lose to a pretrained direct latent or codec audio inpainting baseline?
- Define null outcomes, failure criteria, and claims you will not make.

---

### 2. Build in MendSpeech
- Freeze code revision, model revisions, datasets, hardware, corruption configs, and metrics.
- Define baselines: raw damaged audio, full resynthesis, MendSpeech V1 cascaded repair, fixed context, adaptive context, and one pretrained direct audio inpainting baseline if reproducible.
- Do not train the direct inpainting model from scratch. The purpose is architectural comparison, not a second major training project.

---

### 3. Experiment and Measure
- Run a tiny dry run to ensure every result field is populated.

---

### 4. Required Output Artifacts
- `experiments/capstone_protocol.md`
- `configs/capstone_frozen.yaml`
- `docs/baseline_definitions.md`

---

### 5. Completion Check
> **Definition of Done for Day 50:**  
> Another engineer could reproduce the protocol and understand exactly which claims
compare cascaded repair with direct audio repair.

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
