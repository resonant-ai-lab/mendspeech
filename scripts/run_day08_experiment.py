"""MendSpeech Day 08 Experiment: Clean versus Corrupted ASR Benchmark.

Transcribes identical speech clips in both clean condition and across 5 SpeechDamageBench
damage operators (additive noise, clipping, bandwidth limit, packet dropout, reverberation),
measuring transcript degradation and acoustic confidence collapse.
"""

from pathlib import Path
import sys
REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))
import pandas as pd
import soundfile as sf
import torch

from speechdamagebench.audio_damage import apply_damage, DamageConfig, CORRUPTIONS
from src.asr.baseline import ASRBaseline
from src.audio.loader import load_audio

SEED = 42
OUTPUT_CSV = Path("results/day08_baseline_transcripts.csv")

def main():
    print("--- Starting Day 08 Clean vs. Corrupted ASR Experiment ---")
    baseline = ASRBaseline(device="cpu")

    clean_manifest = pd.read_csv("data/clean_manifest.csv")
    results = []

    for _, row in clean_manifest.iterrows():
        clip_id = row["clip_id"]
        clean_path = Path(row["file_path"])
        if not clean_path.exists():
            clean_path = Path("data") / clean_path

        waveform_tensor, sr = load_audio(clean_path, target_sr=16000)
        clean_np = waveform_tensor.squeeze(0).numpy()

        # 1. Transcribe Clean
        clean_out = baseline.transcribe(waveform_tensor, sample_rate=sr, clip_id=clip_id)
        clean_transcript = clean_out.transcript

        results.append({
            "clip_id": clip_id,
            "condition": "clean",
            "severity": "none",
            "seed": -1,
            "duration_sec": clean_out.duration_sec,
            "avg_confidence": clean_out.average_confidence,
            "tokens_emitted": len(clean_out.tokens),
            "transcript": clean_out.transcript,
            "clean_reference": clean_transcript,
        })
        print(f"[{clip_id} - clean] conf: {clean_out.average_confidence:.4f} | {clean_out.transcript[:50]}...")

        # 2. Transcribe across 5 corruptions at medium severity
        for corruption in CORRUPTIONS:
            config = DamageConfig(
                corruption=corruption,
                severity="medium",
                seed=SEED,
                source_id=clip_id,
            )
            damaged_np, damaged_record = apply_damage(clean_np, sample_rate=16000, config=config)
            damaged_tensor = torch.from_numpy(damaged_np).unsqueeze(0)

            damaged_out = baseline.transcribe(damaged_tensor, sample_rate=16000, clip_id=f"{clip_id}_{corruption}")

            results.append({
                "clip_id": clip_id,
                "condition": corruption,
                "severity": "medium",
                "seed": SEED,
                "duration_sec": damaged_out.duration_sec,
                "avg_confidence": damaged_out.average_confidence,
                "tokens_emitted": len(damaged_out.tokens),
                "transcript": damaged_out.transcript,
                "clean_reference": clean_transcript,
            })
            print(f"[{clip_id} - {corruption}] conf: {damaged_out.average_confidence:.4f} | {damaged_out.transcript[:50]}...")

    df = pd.DataFrame(results)
    OUTPUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUTPUT_CSV, index=False)
    print(f"\nSaved {len(df)} experiment rows to {OUTPUT_CSV}")

if __name__ == "__main__":
    main()
