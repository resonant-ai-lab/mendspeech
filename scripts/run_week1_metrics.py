#!/usr/bin/env python3
"""Run Day 5 objective audio measurements over the labeled benchmark corpus.

Reads data/benchmark/manifest.csv, applies every SpeechDamageBench corruption
at all severity levels with deterministic seeds, computes clean-vs-corrupted
metrics using src/metrics/audio_metrics.py, and writes a tidy CSV to
results/week1_damage_metrics.csv.

Usage:
    python scripts/run_week1_metrics.py [--min-clips 10]

Exits with an error if fewer than min_clips labeled clips are found,
per the Day 5 spec: "do not invent metrics on five unlabeled files."
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import sys
from pathlib import Path

repo_root = Path(__file__).resolve().parent.parent
if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))

from speechdamagebench.audio_damage import (
    CORRUPTIONS,
    DamageConfig,
    apply_damage,
    load_mono,
)
from speechdamagebench.presets import SEVERITIES

from src.metrics.audio_metrics import compute_pair_metrics


def clip_seed(clip_id: str) -> int:
    """Derive a stable integer seed from a clip ID so runs are reproducible."""
    digest = hashlib.sha256(clip_id.encode("utf-8")).digest()
    return int.from_bytes(digest[:4], byteorder="big") % 100_000


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Run Week 1 damage metrics on the benchmark corpus."
    )
    parser.add_argument(
        "--min-clips",
        type=int,
        default=10,
        help="Minimum number of labeled clips required (default 10).",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("results/week1_damage_metrics.csv"),
        help="Path to the output CSV.",
    )
    args = parser.parse_args(argv)

    manifest_path = Path("data/benchmark/manifest.csv")
    if not manifest_path.exists():
        print(f"ERROR: Manifest not found at {manifest_path}", file=sys.stderr)
        return 1

    with open(manifest_path, newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        rows = [row for row in reader if row.get("clip_id") and row.get("file_path")]

    if len(rows) < args.min_clips:
        print(
            f"ERROR: Only {len(rows)} labeled clips found; spec requires "
            f"at least {args.min_clips}. Finish the corpus first.\n"
            f"Missing {args.min_clips - len(rows)} clip(s) in {manifest_path}",
            file=sys.stderr,
        )
        return 2

    results = []
    for row in rows:
        clip_id = row["clip_id"]
        speaker_id = row["speaker_id"]
        file_path = Path(row["file_path"])
        sample_rate = int(row.get("sample_rate", 16000))

        if not file_path.exists():
            print(f"WARN: Skipping {clip_id}: audio not found at {file_path}",
                  file=sys.stderr)
            continue

        clean_wave, sr = load_mono(str(file_path), target_sr=sample_rate)
        base_seed = clip_seed(clip_id)

        for corruption in CORRUPTIONS:
            for severity in SEVERITIES:
                # Vary seed per corruption/severity so each realization is unique
                # but reproducible from the same (clip, corruption, severity).
                seed = base_seed + hash((corruption, severity)) % 10_000
                config = DamageConfig(
                    corruption=corruption,
                    severity=severity,
                    seed=seed,
                    source_id=clip_id,
                )
                corrupted_wave, _record = apply_damage(clean_wave, sr, config)
                metrics = compute_pair_metrics(
                    clean=clean_wave,
                    corrupted=corrupted_wave,
                    sample_rate=sr,
                    clip_id=clip_id,
                    speaker_id=speaker_id,
                    corruption=corruption,
                    severity=severity,
                    seed=seed,
                )
                results.append(metrics.to_dict())

    output_path = args.output
    output_path.parent.mkdir(parents=True, exist_ok=True)

    fieldnames = [
        "clip_id",
        "speaker_id",
        "corruption",
        "severity",
        "seed",
        "clean_rms_db",
        "corrupted_rms_db",
        "clean_peak_dbfs",
        "corrupted_peak_dbfs",
        "snr_db",
        "log_mel_distance",
    ]
    with open(output_path, "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)

    print(f"Wrote {len(results)} rows to {output_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
