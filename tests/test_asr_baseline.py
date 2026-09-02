"""Unit tests for MendSpeech ASR baseline and CTC decoding."""

from pathlib import Path
import pytest
import torch

from src.asr.baseline import ASRBaseline, ASROutput, greedy_ctc_decode


def test_greedy_ctc_decode_collapse_and_blanks():
    """Verify CTC collapse rules: merge consecutive duplicates, preserve duplicates across blanks."""
    # Labels: index 0 is blank '-', 1 is '|', letters follow
    labels = ["-", "|", "C", "O", "L", "B", "K"]
    # Blank = 0
    # C = 2, O = 3, L = 4, B = 5, K = 6, Space = 1

    # Case 1: "C - O O L" -> without blank between Os -> "COL"
    # Create logits where desired token has highest logit
    # Frame sequence: [C, C, O, O, L, L] -> class [2, 2, 3, 3, 4, 4]
    seq1 = [2, 2, 3, 3, 4, 4]
    logits1 = torch.zeros(len(seq1), len(labels))
    for t, idx in enumerate(seq1):
        logits1[t, idx] = 10.0

    transcript1, tokens1, indices1, timestamps1, frame_conf1 = greedy_ctc_decode(
        emissions=logits1, labels=labels, blank_id=0, duration_sec=1.0
    )
    assert transcript1 == "COL"
    assert tokens1 == ["C", "O", "L"]

    # Case 2: "C - O - O - L" -> with blank between Os -> "COOL"
    seq2 = [2, 0, 3, 0, 3, 0, 4]
    logits2 = torch.zeros(len(seq2), len(labels))
    for t, idx in enumerate(seq2):
        logits2[t, idx] = 10.0

    transcript2, tokens2, indices2, timestamps2, frame_conf2 = greedy_ctc_decode(
        emissions=logits2, labels=labels, blank_id=0, duration_sec=1.0
    )
    assert transcript2 == "COOL"
    assert tokens2 == ["C", "O", "O", "L"]


def test_greedy_ctc_decode_word_separator():
    """Verify that the '|' token is mapped to whitespace in transcripts."""
    labels = ["-", "|", "H", "I"]
    # H = 2, | = 1, I = 3
    seq = [2, 1, 3]
    logits = torch.zeros(len(seq), len(labels))
    for t, idx in enumerate(seq):
        logits[t, idx] = 10.0

    transcript, tokens, _, _, _ = greedy_ctc_decode(
        emissions=logits, labels=labels, blank_id=0, duration_sec=0.5
    )
    assert transcript == "H I"


def test_asr_output_dataclass():
    """Verify ASROutput dataclass structure and field types."""
    output = ASROutput(
        clip_id="test_01",
        transcript="HELLO WORLD",
        duration_sec=2.5,
        num_frames=125,
        sample_rate=16000,
        tokens=["H", "E", "L", "L", "O", " ", "W", "O", "R", "L", "D"],
        token_indices=[8, 2, 4, 4, 5, 1, 15, 5, 14, 4, 12],
        token_timestamps_sec=[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1],
        average_confidence=0.95,
        frame_confidences=[0.95] * 125,
    )
    assert output.clip_id == "test_01"
    assert output.transcript == "HELLO WORLD"
    assert output.duration_sec == 2.5
    assert len(output.tokens) == 11
    assert len(output.frame_confidences) == 125


def test_asr_baseline_synthetic_waveform():
    """Verify ASRBaseline inference on a synthetic waveform tensor."""
    baseline = ASRBaseline(device="cpu")
    # 1 second of silence at 16000 Hz
    synthetic_audio = torch.zeros(1, 16000, dtype=torch.float32)
    output = baseline.transcribe(synthetic_audio, sample_rate=16000, clip_id="synthetic_silence")

    assert output.clip_id == "synthetic_silence"
    assert output.duration_sec == 1.0
    assert output.num_frames > 0
    assert output.sample_rate == 16000
    assert 0.0 <= output.average_confidence <= 1.0


def test_asr_baseline_clean_file():
    """Verify transcription on an actual clean baseline file if available."""
    clean_audio_path = Path("data/clean_16k/clean_01.wav")
    if not clean_audio_path.exists():
        pytest.skip("clean_01.wav not present")

    baseline = ASRBaseline(device="cpu")
    output = baseline.transcribe_file(clean_audio_path)

    assert output.clip_id == "clean_01"
    assert len(output.transcript) > 0
    assert output.duration_sec > 0
    assert len(output.token_timestamps_sec) == len(output.tokens)
    assert 0.0 <= output.average_confidence <= 1.0
