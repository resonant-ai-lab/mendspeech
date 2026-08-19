"""Command-line entry: damage a wav from a manifest-style argument list."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from speechdamagebench.audio_damage import (
    CORRUPTIONS,
    DamageConfig,
    apply_damage,
    load_mono,
    save_mono,
)
from speechdamagebench.presets import PACKAGE_VERSION, SEVERITIES


def _parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="speechdamagebench",
        description=(
            "Apply one seeded SpeechDamageBench corruption. "
            "The printed JSON record is enough to regenerate the file."
        ),
    )
    p.add_argument("--version", action="version", version=f"speechdamagebench {PACKAGE_VERSION}")
    sub = p.add_subparsers(dest="cmd", required=True)

    d = sub.add_parser("damage", help="damage one wav and write a regenerable record")
    d.add_argument("--in", dest="inp", required=True, help="clean wav path")
    d.add_argument("--out", dest="out", required=True, help="damaged wav path")
    d.add_argument("--corruption", required=True, choices=CORRUPTIONS)
    d.add_argument("--severity", required=True, choices=SEVERITIES)
    d.add_argument("--seed", required=True, type=int, help="integer seed (required)")
    d.add_argument(
        "--source-id",
        required=True,
        help="clean source identifier recorded in the manifest row",
    )
    d.add_argument(
        "--sr",
        dest="sample_rate",
        type=int,
        default=16000,
        help="working sample rate in Hz (default 16000)",
    )
    d.add_argument(
        "--record",
        default=None,
        help="optional path to write the JSON record",
    )
    return p


def main(argv: list[str] | None = None) -> int:
    """Run the CLI. Returns a process exit code."""
    args = _parser().parse_args(argv)
    if args.cmd != "damage":
        return 2
    wave, sr = load_mono(args.inp, target_sr=args.sample_rate)
    config = DamageConfig(
        corruption=args.corruption,
        severity=args.severity,
        seed=args.seed,
        source_id=args.source_id,
    )
    damaged, record = apply_damage(wave, sr, config)
    save_mono(args.out, damaged, sr)
    payload = record.to_dict()
    payload["input_path"] = str(Path(args.inp))
    payload["output_path"] = str(Path(args.out))
    text = json.dumps(payload, indent=2, sort_keys=True)
    print(text)
    if args.record:
        rec_path = Path(args.record)
        rec_path.parent.mkdir(parents=True, exist_ok=True)
        rec_path.write_text(text + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
