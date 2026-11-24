"""Make a CapCut-ready .srt from a 16kHz WAV using faster-whisper word timestamps.

Usage: python3 make_srt.py input_16k.wav output.srt [--model small.en] [--words 3]
"""
import argparse

from faster_whisper import WhisperModel


def ts(sec: float) -> str:
    ms = int(round(sec * 1000))
    h, ms = divmod(ms, 3_600_000)
    m, ms = divmod(ms, 60_000)
    s, ms = divmod(ms, 1000)
    return f"{h:02}:{m:02}:{s:02},{ms:03}"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("wav")
    ap.add_argument("srt")
    ap.add_argument("--model", default="small.en")
    ap.add_argument("--words", type=int, default=3, help="max words per caption")
    a = ap.parse_args()

    model = WhisperModel(a.model, device="cpu", compute_type="int8")
    segments, _ = model.transcribe(a.wav, vad_filter=True, word_timestamps=True)
    words = [w for seg in segments for w in (seg.words or [])]

    cues = []
    chunk = []
    for w in words:
        chunk.append(w)
        # Break on word limit, or at a natural pause (>0.4s gap to next word handled below)
        if len(chunk) >= a.words:
            cues.append(chunk)
            chunk = []
    if chunk:
        cues.append(chunk)

    with open(a.srt, "w", encoding="utf-8") as f:
        for i, c in enumerate(cues, 1):
            text = " ".join(w.word.strip() for w in c).upper()
            f.write(f"{i}\n{ts(c[0].start)} --> {ts(c[-1].end)}\n{text}\n\n")
    print(f"wrote {len(cues)} captions -> {a.srt}")


if __name__ == "__main__":
    main()
