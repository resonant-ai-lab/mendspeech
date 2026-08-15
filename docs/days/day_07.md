# Day 07: Review, explain, and freeze Week 1

> **Week 1 • Day 7 of 7**  
> **Navigation:** [← Day 06](day_06.md) | [Week 1 Plan](../Week_1_MendSpeech_Daily_Plan.md) | [Master Index](../INDEX.md) | [Day 08 →](day_08.md)

---

### Compute Target
`Local CPU`

---

### 1. Learn
- Review waveform, STFT, Mel features, SNR, clipping, dropouts, and reverberation.

---

### 2. Build in MendSpeech
- Clean repository structure.
- Freeze SpeechDamageBench v0.1 severity presets and a benchmark set of **≥30 utterances across ≥5 speakers with reference transcripts**, written as speaker-separated train/val/test manifest files.
- Tag the benchmark package schema and add a minimal usage example independent of MendSpeech.

---

### 3. Experiment and Measure
- From a blank notebook, recreate one corruption and one log Mel plot without copying previous cells.

---

### 4. Required Output Artifacts
- `reports/week1_audio_foundations.md`
- `data/benchmark_manifest.csv` (train/val/test splits, transcripts included)
- `speechdamagebench/README.md`
- `speechdamagebench/VERSION`

---

### 5. Completion Check
> **Definition of Done for Day 07:**  
> You can teach the complete path from clean waveform to controlled corruption and
feature tensor.

---

### 6. Study Method & Protocol
25 minutes focused reading. 65 minutes implementation or controlled experiment. 20 minutes research
notebook. 10 minutes commit and explain the result aloud. When debugging is incomplete, continue the
same task in the next session instead of pretending the day is finished.

---

### 7. References & Resources
- PyTorch and TorchAudio audio processing documentation
- A practical digital signal processing reference for STFT and filterbanks   Week 2: ASR, CTC, Confidence, and Repair Localization Build the recognition and uncertainty layer, plus a reusable Modal execution path.  Day  Focus  Minimum evidence  Compute  Day 8  Frame sequence to transcript
- Compare clean and corrupted transcripts on the exact same utterances.  Modal L4 optional, CPU acceptable for small runs  Day 9  CTC from first principles
- Enumerate several legal paths for a tiny target word.
- Break your decoder deliberately with repeated letters and fix it.  Local CPU  Day 10  WER, CER, and error taxonomy
- Score clean versus every SpeechDamageBench severity.
- Find which corruption type causes deletion errors fastest.  Local CPU  Day 11  Token confidence and uncertainty
- Compare confidence on clean, noisy, clipped, and dropout audio.
- Find confident but wrong examples and document them.  Modal L4 recommended  Day 12  Time alignment and uncertain spans
- Inject known 100 ms and 250 ms dropouts and test whether uncertainty overlaps them.  Modal L4 recommended  Day 13  Define selective repair policy v0
- Sweep confidence thresholds on SpeechDamageBench.
- Measure percentage of audio selected for repair and overlap with known damaged spans.  Local CPU after ASR outputs are cached  Day 14  Week 2 integration and review
- Run at least twenty corrupted utterances and manually inspect policy errors.  Modal L4 recommended
