# AGENTS.md

Operating instructions for AI coding agents (Claude Code, Codex, OpenCode,
Cursor, Gemini CLI, etc.) working in this repository. Read this file before
doing anything. Where these rules conflict with defaults or habits, these
rules win.

---

## 1. Project Context

**MendSpeech** is a research and systems project for *selective semantic
speech restoration under real-time constraints*: detect damaged spans of
speech with calibrated ASR uncertainty, decide whether to preserve, inspect,
repair, or abstain, reconstruct only what is justified (cascaded ASR→TTS and
direct audio-inpainting baselines), and measure everything.

Two products matter:
1. **MendSpeech** — the end-to-end system (`src/`).
2. **SpeechDamageBench** — a standalone, versioned damage-generation benchmark
   that must remain usable without MendSpeech (becomes its own package).

The project is executed day-by-day from a fixed 56-day curriculum. An agent's
job on any given evening is to execute exactly one day file — not to redesign
the plan.

---

## 2. Critical Rules (Read First)

1. **Plan of record:** [`docs/REVISED_EXECUTION_PLAN.md`](docs/REVISED_EXECUTION_PLAN.md)
   (v1, October calendar) governs pacing, gates, scope, and compression. The
   blueprint and roadmap define content and depth. On any calendar or scope
   conflict, the execution plan wins.
2. **This repository is PUBLIC.** Personal content of any kind stays out of
   tracked files. `PRIVATE_PLAN_NOTES.md` is gitignored by design — never
   stage it, never commit it, never remove its ignore entry. Review
   `git diff --cached` before every commit.
3. **Never fake completion.** A day is done only when its day file's
   Completion Check passes and its Required Output artifacts exist. If work is
   incomplete, say so and continue the same task next session — do not claim
   the day is finished to protect a date.
4. **Never force-push or rewrite pushed history on `main`.**
5. **Do not redesign the plan unilaterally.** Adding experiments, reordering
   days, or changing scope is a human decision. Propose it; don't do it.

---

## 3. Repository Layout

```text
AGENTS.md                 # This file
README.md                 # Public navigation index
pyproject.toml            # Package: mendspeech (Python >=3.10)
src/                      # Source code, one package per blueprint subsystem
  audio/                  # EXISTS: waveform I/O, resampling, measurements
  asr/ streaming/ controller/ tts/ repair/ baselines/ metrics/ bench/
                          # PLANNED: create per blueprint as days reach them
tests/                    # pytest suite (test_*.py), mirrors src structure
notebooks/                # Research notebooks (dayNN_*.ipynb)
results/                  # Measured outputs: CSVs, PNGs, tables (dayNN_* naming)
data/                     # Manifests only (clean_manifest.csv etc.); audio is gitignored
docs/                     # All planning documents (see below)
  REVISED_EXECUTION_PLAN.md   # PLAN OF RECORD (v1 October calendar)
  MendSpeech_Project_Blueprint.md   # Architecture, metrics, definition of done
  MendSpeech_8_Week_Master_Roadmap.md  # Content order and depth
  MendSpeech_Complete_56_Day_Plan.md   # Compiled reference (original content)
  Week_N_MendSpeech_Daily_Plan.md     # Weekly guides + v1 compression maps
  days/day_NN.md          # Per-day prompt sheets — the unit of execution
pdfs/                     # Archived original PDFs — NEVER modify
PRIVATE_PLAN_NOTES.md     # Gitignored personal notes — NEVER touch or stage
```

---

## 4. Environment & Commands

- Python **>= 3.10**. Install: `pip install -e .` (deps: torch, torchaudio,
  soundfile, librosa, scipy, matplotlib, pandas, numpy).
- **Use the project venv** (system python has no dependencies installed):
  `.venv/bin/python -m pytest` or activate `.venv` first.
- Run tests: **`pytest`** from repo root (config in `pyproject.toml`:
  `pythonpath = ["."]`, `testpaths = ["tests"]`).
- Run a single module's tests: `pytest tests/test_audio_loader.py`.
- No GPU is required for Weeks 1–3 (Local CPU). Modal (L4) is used from
  Week 2 onward for cloud runs — see §9 Compute Discipline.
- Import style: modules live under `src/` (e.g. `from src.audio.loader
  import load_audio`), enabled by the `pythonpath` setting.

---

## 5. Executing a Day File (the Core Loop)

When given a day file (`docs/days/day_NN.md`):

1. **Read the v1 status banner** under the title. It overrides the file body:
   - `CORE` — full session; execute Learn → Build → Experiment → Artifacts.
   - `LEARN-ONLY` — theory only; no build session, no artifacts, no commit of code.
   - `MERGED` — its work happens inside the absorbing day; never run standalone.
   - `DROPPED` — never scheduled; optional reading at most.
2. **Learn block first.** Never start building before the day's Learn content
   is understood; the human, not the agent, must be able to defend it later.
3. **Build and measure** exactly what the day file specifies — minimum viable
   version, then measure. Resist scope creep beyond Required Output.
4. **Produce the Required Output artifacts** at the exact paths the day file
   names (`results/dayNN_*.csv`, `src/...`, `docs/*notes*.md`). Paths are
   contracts.
5. **Check the Completion Check** honestly. If it fails, the day is not done.
6. **End with a commit** (see §8) containing the day's code + artifacts.

If a day's status ever changes, the day-file banner, its week guide's
compression map, and `docs/REVISED_EXECUTION_PLAN.md` must change together in
one commit.

---

## 6. Coding Standards

Match the style already established in `src/audio/`:

- **Type hints everywhere** on public functions; `typing` module forms
  (`Optional`, `Tuple`, `Union`, `Dict`) as currently used.
- **Docstrings:** module-level summary + Google-style `Args:`/`Returns:` on
  public functions. Explain units (Hz, dB, seconds) — this is an audio project.
- **Dataclasses** for structured records (see `AudioMetadata`).
- **Determinism is a product feature:** every damage/ corruption /
  augmentation operation takes an explicit random seed; every generated
  artifact records corruption name, severity, seed, source ID, parameters,
  and package version. No unseeded randomness, ever.
- **Tests live in `tests/test_*.py`** and mirror the src layout. New public
  functions get tests in the same session; shape/gradient assertions for
  tensor code (see `tests/test_audio_loader.py` for the pattern).
- **numpy ↔ torch boundary:** keep conversions explicit; prefer torch
  tensors at module boundaries, numpy inside measurement utilities.
- Notebooks are for exploration and figures only (`notebooks/dayNN_*.ipynb`);
  all reusable logic goes in `src/` with tests.

---

## 7. Data & Artifact Policy

- Audio files (`*.wav/mp3/flac/ogg`), checkpoints (`*.pt/*.pth/*.ckpt/*.onnx/
  *.nemo`), wandb/runs logs are **gitignored — never commit them.**
- Commit instead: manifests (`data/*.csv|json`), metric tables
  (`results/dayNN_*.csv`), figures (`results/*.png`), notes
  (`docs/*notes*.md`), and code/tests.
- Result files are named `dayNN_<what>.<ext>` (e.g.
  `results/day40_quantization_tradeoffs.csv`) exactly as day files specify.
- The frozen evaluation set (≥30 transcripted utterances, ≥5 speakers,
  speaker-separated splits) is immutable once frozen. Never regenerate or
  re-split it; new experiments get new corruption configs, not a new test set.

---

## 8. Git Standards (Mandatory)

- **Conventional Commits:** `type(scope): imperative subject` — types:
  `feat`, `fix`, `docs`, `test`, `chore`, `refactor`. Scopes by subsystem:
  `audio`, `asr`, `bench`, `plan`, `week3`, etc.
- Subject ≤ 72 chars, lowercase, imperative, no trailing period. Body wrapped
  ≤ 72 chars, explaining **what and why**.
- **Atomic commits:** one logical change per commit — never mix plan edits
  with feature code; day-session commits include that day's code + artifacts.
- `pytest` green before committing code changes.
- Never force-push, never rebase pushed commits, never amend pushed history.

---

## 9. Compute Discipline

- Respect the `Compute Target` in each day file. Default cloud tier: **Modal
  L4**.
- **L40S is banned for latency, RTF, or memory comparisons** — it invalidates
  cross-run comparisons. Measured efficiency numbers come from L4 only.
- Total Modal budget for the project is ~$15–30. Prefer the cheapest tier
  that fits the experiment; cache ASR outputs to avoid re-running inference.
- Batch-size / hardware changes invalidate comparisons — if an experiment
  needs different hardware, note it in the results file rather than silently
  mixing tiers.

---

## 10. Behavior Boundaries

- **Touch:** `src/`, `tests/`, `notebooks/`, `results/`, `data/` manifests,
  and — when explicitly asked — the planning docs in `docs/`.
- **Never touch:** `pdfs/` (archived originals), `PRIVATE_PLAN_NOTES.md`,
  `.gitignore`'s private-notes entry, the frozen evaluation set, and any
  `results/` file belonging to a previously frozen benchmark run.
- **When uncertain:** follow the day file literally and flag the question in
  your response. Smallest correct change beats clever refactors.
- **Never mark, claim, or imply a day is complete when it is not.** Partial
  work is committed as partial, with an honest message.
