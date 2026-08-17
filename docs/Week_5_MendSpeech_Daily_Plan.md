# Week 5: Streaming, Cache Aware Inference, and Adaptive Context

> **Days 29 to 35**  
> **Navigation:** [← Week 4](Week_4_MendSpeech_Daily_Plan.md) | [Master Index](INDEX.md) | [Master Roadmap](MendSpeech_8_Week_Master_Roadmap.md) | [Week 6 →](Week_6_MendSpeech_Daily_Plan.md)

---

> [!IMPORTANT]
> **Week Milestone:**  
> Turn the recognizer into a real time system and test uncertainty guided context spending.
>
> **v1 October calendar:** Gate 4 target **Sep 27**. Days 29–35 run as
> written with VAD/endpointing in the live milestone, then complete **Add-on
> B** (async serving and load behavior) on the Gate 4 weekend.

---

## Week Map

| Day | Focus | Minimum Evidence / Artifact | Compute | Daily Link |
| :--- | :--- | :--- | :--- | :--- |
| **Day 29** | Offline versus streaming ASR | You can explain why naive chunking creates boundary errors and redundant compute. | `Modal L4` | [Open Day 29](days/day_29.md) |
| **Day 30** | Buffered streaming | You can quantify the compute waste caused by overlapping history. | `Modal L4` | [Open Day 30](days/day_30.md) |
| **Day 31** | Cache aware streaming internals | You can explain what is cached, what is recomputed, and why cache aware inference
can be more efficient. | `Modal L4` | [Open Day 31](days/day_31.md) |
| **Day 32** | Lookahead ablation | You can defend a Balanced operating point using data rather than preference. | `Modal L4` | [Open Day 32](days/day_32.md) |
| **Day 33** | Break the cache on purpose | You can explain a concrete failure caused by incorrect state handling. | `Modal L4` | [Open Day 33](days/day_33.md) |
| **Day 34** | Adaptive context controller prototype | You have a falsifiable first answer to whether uncertainty can guide context spending. | `Modal L4` | [Open Day 34](days/day_34.md) |
| **Day 35** | Week 5 live streaming milestone | A person can speak and watch MendSpeech transcribe incrementally while exposing
the state that drives repair decisions. | `Modal L4` | [Open Day 35](days/day_35.md) |

---

## Reference Spine
- Stateful or cache aware Conformer primary material\nNVIDIA NeMo streaming ASR documentation and examples

---

## Daily Detailed Operating Plans

### DAY 29: Offline versus streaming ASR
- **Compute:** `Modal L4`
- **Dedicated Daily File:** [`docs/days/day_29.md`](days/day_29.md)

#### Learn
- Audio chunks.
- Algorithmic latency.
- Partial hypotheses.
- Endpointing and finalization.

#### Build in MendSpeech
- Create a chunk simulator that feeds audio incrementally.
- Log when each chunk becomes available and when text changes.

#### Experiment and Measure
- Compare offline transcript with naive chunk by chunk transcription.

#### Required Output
- `src/streaming/chunker.py`
- `results/day29_offline_vs_naive.csv`

#### Completion Check
> You can explain why naive chunking creates boundary errors and redundant compute.

---

### DAY 30: Buffered streaming
- **Compute:** `Modal L4`
- **Dedicated Daily File:** [`docs/days/day_30.md`](days/day_30.md)

#### Learn
- Overlapping windows.
- Buffer size.
- Stride.
- Repeated computation.

#### Build in MendSpeech
- Implement or run buffered streaming with configurable overlap.
- Measure how much audio is recomputed.

#### Experiment and Measure
- Sweep buffer and stride settings.
- Measure WER and latency tradeoffs.

#### Required Output
- `src/streaming/buffered.py`
- `results/day30_buffered_sweep.csv`

#### Completion Check
> You can quantify the compute waste caused by overlapping history.

---

### DAY 31: Cache aware streaming internals
- **Compute:** `Modal L4`
- **Dedicated Daily File:** [`docs/days/day_31.md`](days/day_31.md)

#### Learn
- Cached activations.
- Past context state.
- Streaming masks.
- Right context and lookahead.

#### Build in MendSpeech
- Use NeMo cache aware streaming inference on a supported FastConformer checkpoint.
- Log cache related configuration and chunk boundaries.

#### Experiment and Measure
- Compare buffered and cache aware inference on the same audio and same hardware.

#### Required Output
- `src/streaming/cache_aware_runner.py`
- `results/day31_buffered_vs_cache.csv`

#### Completion Check
> You can explain what is cached, what is recomputed, and why cache aware inference
can be more efficient.

---

### DAY 32: Lookahead ablation
- **Compute:** `Modal L4`
- **Dedicated Daily File:** [`docs/days/day_32.md`](days/day_32.md)

#### Learn
- Right context.
- Lookahead.
- Commit delay.
- WER and latency as competing objectives.

#### Build in MendSpeech
- Run several supported lookahead settings with everything else fixed.
- Store per utterance and aggregate metrics.

#### Experiment and Measure
- Plot WER versus latency and identify dominated operating points.

#### Required Output
- `experiments/lookahead_ablation.py`
- `results/day32_lookahead.csv`
- `results/day32_pareto.png`

#### Completion Check
> You can defend a Balanced operating point using data rather than preference.

---

### DAY 33: Break the cache on purpose
- **Compute:** `Modal L4`
- **Dedicated Daily File:** [`docs/days/day_33.md`](days/day_33.md)

#### Learn
- State continuity.
- Chunk boundary dependencies.
- Cache reset and truncation.

#### Build in MendSpeech
- Add controlled experiments that reset or shorten cache at selected boundaries.

#### Experiment and Measure
- Measure WER changes around the reset point.
- Inspect whether errors cluster near boundaries or propagate later.

#### Required Output
- `experiments/cache_break_test.py`
- `results/day33_cache_failures.md`

#### Completion Check
> You can explain a concrete failure caused by incorrect state handling.

---

### DAY 34: Adaptive context controller prototype
- **Compute:** `Modal L4`
- **Dedicated Daily File:** [`docs/days/day_34.md`](days/day_34.md)

#### Learn
- Policy driven context selection.
- Confidence smoothing.
- Latency budget.
- Stability versus oscillation.

#### Build in MendSpeech
- Implement a controller that classifies chunks as easy or uncertain.
- Map states to small or larger supported right context settings, even if the first prototype must simulate switching between runs.

#### Experiment and Measure
- Compare fixed fast, fixed accurate, and adaptive policies on a controlled subset.

#### Required Output
- `src/controller/adaptive_context.py`
- `results/day34_adaptive_context.csv`

#### Completion Check
> You have a falsifiable first answer to whether uncertainty can guide context spending.

---

### DAY 35: Week 5 live streaming milestone
- **Compute:** `Modal L4`
- **Dedicated Daily File:** [`docs/days/day_35.md`](days/day_35.md)

#### Learn
- Review buffered streaming, cache aware inference, lookahead, cache failures,
  adaptive context, VAD-driven endpointing, and partial-versus-final latency.

#### Build in MendSpeech
- Connect microphone or simulated live audio to the streaming recognizer.
- Reuse Add-on A VAD for endpointing and log speech start, speech end, and
  finalization timestamps.
- Show partial text, confidence timeline, VAD/endpointing state, current
  context mode, queue depth, and latency.

#### Experiment and Measure
- Record a short demo with clean and damaged speech.
- Measure time to first partial transcript, endpoint delay, false starts, and
  missed endpoints on the same cases.
- Document remaining technical limitations honestly.

#### Required Output
- `app/mendspeech_v2_streaming.py`
- `demos/week5_streaming_demo.mp4`
- `reports/week5_streaming.md`

#### Completion Check
> A person can speak and watch MendSpeech transcribe incrementally while exposing
the VAD, endpointing, cache, context, and uncertainty state that drives repair
decisions.

---

## Gate 4 Add-on B — Async Serving and Load Behavior

### Build

- Wrap the streaming recognizer in an async FastAPI/WebSocket service.
- Dockerize it and deploy on Modal using the same L4 for every comparison.
- Make per-stream queues, maximum queue depth, backpressure, timeout,
  disconnect, retry, and fallback behavior explicit.
- Propagate VAD start/end events and request/run identifiers through the
  service.

### Experiment and Measure

- Run 1, 4, and 8 concurrent streams with fixed audio, hardware, batching, and
  model configuration.
- Record time to first partial transcript, endpoint/finalization delay,
  end-to-end p50/p95/p99, RTF, cold start, CPU/GPU utilization, peak GPU memory,
  queue depth, and dropped or delayed chunks.
- Force one queue-overload or disconnect case and verify bounded, documented
  recovery behavior.

### Required Output

- `infra/serve/`
- `results/addon_b_serving.csv`
- `reports/addon_b_serving.md`

### Completion Check

> You can locate the measured bottleneck, explain the backpressure policy, and
> reproduce one controlled failure and recovery without silently losing audio.

---
