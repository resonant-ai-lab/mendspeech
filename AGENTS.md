# AGENTS.md — Operating Rules for AI Coding Agents

Any AI agent working in this repository follows these rules. They exist to keep
the plan consistent, the history clean, and the public repo safe.

---

## What This Repo Is

MendSpeech: a selective speech-restoration research and systems project built
day-by-day with AI coding agents.

- **Plan of record:** [`docs/REVISED_EXECUTION_PLAN.md`](docs/REVISED_EXECUTION_PLAN.md) (v1, October calendar — gates, compression, add-on labs).
- The blueprint and roadmap define *content and depth*; the execution plan
  defines *pacing and scope*. When they conflict on calendar or scope, the
  execution plan wins.

## Working With the Daily Plan

- Day files (`docs/days/day_NN.md`) are the source of truth for daily content.
- Respect the **v1 status banners** on day files and the compression maps in
  the weekly guides:
  - `CORE` — runs as a full session.
  - `LEARN-ONLY` — theory only; no build session, no artifacts.
  - `MERGED` — its work happens inside the absorbing day; never run it standalone.
  - `DROPPED` — never scheduled; optional reading at most.
- If a day's status ever changes, update the day file banner, its week guide's
  compression map, and `docs/REVISED_EXECUTION_PLAN.md` in the same change.
- Session protocol: the Learn block and Build block may sit in separate sittings
  on the same calendar day; a build session never starts before its Learn block
  is read and never ends without a commit.
- A day is complete only when its day file's **Completion Check** passes and the
  **Required Output** artifacts exist. Never mark a day done to protect a date.

## Git Standards (Mandatory)

- **Conventional Commits:** `type(scope): imperative subject` — types:
  `feat`, `fix`, `docs`, `test`, `chore`, `refactor`.
- Subject ≤ 72 characters, lowercase, imperative mood, no trailing period.
- Body (when useful) wrapped at ≤ 72 characters, explaining **what and why**.
- **Atomic commits:** one logical change per commit; never mix plan edits with
  feature code in one commit.
- **Never force-push or rewrite pushed history** on `main`.
- Run `pytest` before committing code changes; keep the suite green.

## Privacy — This Repository Is Public

- **Never add personal-schedule or job-search content to tracked files.** That
  includes daytime/office reading arrangements, application tracking, company
  target lists, or anything about the author's employment situation.
- `PRIVATE_PLAN_NOTES.md` is deliberately gitignored. Never stage it, never
  commit it, and never remove its ignore entry.
- Before any commit, review the staged diff (`git diff --cached`) and confirm
  it contains nothing personal.

## Compute Discipline

- Respect the `Compute Target` in each day file; default is Modal L4.
- Keep total Modal spend within the project budget (~$15–30); prefer the
  cheapest tier that fits the experiment.
- **L40S is banned for latency, RTF, or memory comparisons** — it invalidates
  cross-run comparisons. L4 only for measured efficiency numbers.
- Generated audio, checkpoints, and model files are gitignored; commit metrics,
  tables, figures, and small manifests instead.
