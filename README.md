# MendSpeech

**Selective semantic speech restoration under real-time constraints.**

Speech recordings get damaged — packet loss, clipping, noise, dropouts. MendSpeech
does not resynthesize everything: it detects *which spans* of speech are damaged
using calibrated ASR uncertainty, decides whether to **preserve, inspect, repair,
or abstain**, and reconstructs only what the evidence justifies. Everything is
measured: accuracy, latency percentiles, real-time factor, calibration error,
and stitching quality.

The project also answers a research question with a controlled comparison:
**cascaded ASR→TTS repair vs. direct audio inpainting** on the same damaged
spans — where does each architecture win, and what does each lose?

---

## Deliverables

| Product | What it is |
| :--- | :--- |
| **MendSpeech** | The end-to-end system: streaming ASR → calibrated uncertainty → repair policy → selective reconstruction with boundary-matched stitching (`src/`). |
| **SpeechDamageBench** | A standalone, versioned damage-generation benchmark (additive noise, clipping, bandwidth limits, dropouts, reverberation). Fully deterministic: every damaged sample records its corruption, severity, seed, and source. Usable without MendSpeech. |

---

## Status

Early build — audio foundations first. Tracked against a milestone-gated plan
([execution plan](docs/REVISED_EXECUTION_PLAN.md)).

| Subsystem | Purpose | Status |
| :--- | :--- | :--- |
| `src/audio` | Waveform I/O, resampling, acoustic measurements, STFT/spectrograms | ✅ **exists** (tested) |
| `bench` (SpeechDamageBench) | Deterministic damage generation + frozen evaluation sets | 🚧 in progress |
| `asr` | FastConformer, CTC, token confidence, calibration | planned |
| `streaming` | Cache-aware real-time inference, lookahead control | planned |
| `controller` | Preserve / inspect / repair / abstain policy | planned |
| `tts`, `repair` | Speaker-conditioned synthesis, boundary matching, seam diagnostics | planned |
| `baselines`, `metrics` | Direct audio-inpainting comparison; WER, RTF, ECE, seam scores | planned |

Audio corpora and checkpoints are gitignored; manifests and all measured
results are tracked (see the [results index](results/README.md) — every
artifact is tied to the session and finding that produced it).

---

## Quickstart

```bash
git clone <this-repo> && cd mendspeech
python -m venv .venv && source .venv/bin/activate
pip install -e .
pytest          # 116 tests: audio modules + documentation link guard
```

Core dependencies: `torch`, `torchaudio`, `soundfile`, `librosa`, `scipy`,
`matplotlib`, `pandas`, `numpy` (Python ≥ 3.10). No GPU required for the
audio foundations; cloud experiments run on rented Modal L4 GPUs.

```python
from src.audio.loader import load_audio
from src.audio.stft import spectrogram_db

wave, sr = load_audio("clip.wav", target_sr=16000)
spec = spectrogram_db(wave, n_fft=400, hop_length=160)  # 25 ms / 10 ms speech defaults
```

---

## How the work is organized

The project is executed day-by-day from a fixed 56-day curriculum, with each
session producing code, measured artifacts, and a commit — much of the
implementation is agent-driven under the rules in [`AGENTS.md`](AGENTS.md).
The [revised execution plan](docs/REVISED_EXECUTION_PLAN.md) is the plan of
record (milestone gates and compression decisions); the
[blueprint](docs/MendSpeech_Project_Blueprint.md) defines architecture,
metrics, and the definition of done.

### 8-week progression

| Week | Focus | Weekly Plan | Daily Files |
| :--- | :--- | :--- | :--- |
| **1** | Audio, degradation, measurement foundations | [Guide](docs/Week_1_MendSpeech_Daily_Plan.md) | [01](docs/days/day_01.md) • [02](docs/days/day_02.md) • [03](docs/days/day_03.md) • [04](docs/days/day_04.md) • [05](docs/days/day_05.md) • [06](docs/days/day_06.md) • [07](docs/days/day_07.md) |
| **2** | ASR, CTC, confidence, repair localization | [Guide](docs/Week_2_MendSpeech_Daily_Plan.md) | [08](docs/days/day_08.md) • [09](docs/days/day_09.md) • [10](docs/days/day_10.md) • [11](docs/days/day_11.md) • [12](docs/days/day_12.md) • [13](docs/days/day_13.md) • [14](docs/days/day_14.md) |
| **3** | Conformer from first principles | [Guide](docs/Week_3_MendSpeech_Daily_Plan.md) | [15](docs/days/day_15.md) • [16](docs/days/day_16.md) • [17](docs/days/day_17.md) • [18](docs/days/day_18.md) • [19](docs/days/day_19.md) • [20](docs/days/day_20.md) • [21](docs/days/day_21.md) |
| **4** | FastConformer & efficient encoders | [Guide](docs/Week_4_MendSpeech_Daily_Plan.md) | [22](docs/days/day_22.md) • [23](docs/days/day_23.md) • [24](docs/days/day_24.md) • [25](docs/days/day_25.md) • [26](docs/days/day_26.md) • [27](docs/days/day_27.md) • [28](docs/days/day_28.md) |
| **5** | Streaming, cache-aware inference, adaptive context | [Guide](docs/Week_5_MendSpeech_Daily_Plan.md) | [29](docs/days/day_29.md) • [30](docs/days/day_30.md) • [31](docs/days/day_31.md) • [32](docs/days/day_32.md) • [33](docs/days/day_33.md) • [34](docs/days/day_34.md) • [35](docs/days/day_35.md) |
| **6** | Robust fine-tuning, quantization, calibration | [Guide](docs/Week_6_MendSpeech_Daily_Plan.md) | [36](docs/days/day_36.md) • [37](docs/days/day_37.md) • [38](docs/days/day_38.md) • [39](docs/days/day_39.md) • [40](docs/days/day_40.md) • [41](docs/days/day_41.md) • [42](docs/days/day_42.md) |
| **7** | TTS, speaker preservation, boundary-matched repair | [Guide](docs/Week_7_MendSpeech_Daily_Plan.md) | [43](docs/days/day_43.md) • [44](docs/days/day_44.md) • [45](docs/days/day_45.md) • [46](docs/days/day_46.md) • [47](docs/days/day_47.md) • [48](docs/days/day_48.md) • [49](docs/days/day_49.md) |
| **8** | Capstone: cascaded vs. direct repair | [Guide](docs/Week_8_MendSpeech_Daily_Plan.md) | [50](docs/days/day_50.md) • [51](docs/days/day_51.md) • [52](docs/days/day_52.md) • [53](docs/days/day_53.md) • [54](docs/days/day_54.md) • [55](docs/days/day_55.md) • [56](docs/days/day_56.md) |

---

## Core documentation

- [Revised execution plan — calendar, gates, compression](docs/REVISED_EXECUTION_PLAN.md)
- [Project blueprint — architecture, metrics, definition of done](docs/MendSpeech_Project_Blueprint.md)
- [8-week master roadmap — content order and depth](docs/MendSpeech_8_Week_Master_Roadmap.md)
- [Complete 56-day plan — compiled reference](docs/MendSpeech_Complete_56_Day_Plan.md)
- [Docs index](docs/INDEX.md) • [Results index](results/README.md)
