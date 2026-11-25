#!/usr/bin/env python3
"""
Phase 0: Audio-first stream/VOD ingestion, RMS vocal spike detection,
and CPU-friendly word-level transcription (faster-whisper int8).

Outputs into --out-dir:
  - audio_16k.wav           (16kHz mono WAV)
  - meta.json               (video title/duration/id if URL)
  - audio_peaks.json        (top RMS loudness spikes in MM:SS)
  - transcript_words.json   (word-level timestamps for kinetic ASS captions)
  - transcript_readable.txt ([MM:SS - MM:SS] readable log for Phase 1 scoring)
  - chat_peaks.json         (live-chat hype spikes; only with --with-chat or --chat-file)
"""

import argparse
import json
import math
import re
import shutil
import struct
import subprocess
import sys
import wave
from pathlib import Path
from urllib.parse import urlparse


def is_url(value: str) -> bool:
    parsed = urlparse(value)
    return parsed.scheme in ("http", "https") and bool(parsed.netloc)


def fmt_ts(seconds: float) -> str:
    seconds = max(0.0, float(seconds))
    mins = int(seconds // 60)
    secs = seconds - (mins * 60)
    return f"{mins:02d}:{secs:05.2f}"


def fmt_mmss(seconds: float) -> str:
    seconds = max(0.0, float(seconds))
    mins = int(seconds // 60)
    secs = int(round(seconds - (mins * 60)))
    if secs == 60:
        mins += 1
        secs = 0
    return f"{mins:02d}:{secs:02d}"


def require_bin(name: str) -> str:
    path = shutil.which(name)
    if not path:
        print(f"ERROR: '{name}' is not installed or not in PATH.", file=sys.stderr)
        sys.exit(1)
    return path


def run_cmd(cmd: list[str], capture: bool = False) -> subprocess.CompletedProcess:
    print(f"[run] {' '.join(cmd)}")
    result = subprocess.run(
        cmd,
        text=True,
        capture_output=capture,
        check=False,
    )
    if result.returncode != 0:
        if capture and result.stderr:
            print(result.stderr, file=sys.stderr)
        print(f"ERROR: command exited with status {result.returncode}", file=sys.stderr)
        sys.exit(result.returncode)
    return result


def ingest_audio(source: str, out_dir: Path, cookies_browser: str | None) -> Path:
    require_bin("ffmpeg")
    wav_path = out_dir / "audio_16k.wav"

    if is_url(source):
        require_bin("yt-dlp")
        cookie_args = ["--cookies-from-browser", cookies_browser] if cookies_browser else []

        # Fetch metadata
        meta_proc = run_cmd(
            ["yt-dlp", "--no-playlist", "--dump-single-json", *cookie_args, source],
            capture=True,
        )
        try:
            meta = json.loads(meta_proc.stdout)
            meta_summary = {
                "id": meta.get("id"),
                "title": meta.get("title"),
                "uploader": meta.get("uploader"),
                "duration": meta.get("duration"),
                "webpage_url": meta.get("webpage_url", source),
            }
            (out_dir / "meta.json").write_text(json.dumps(meta_summary, indent=2), encoding="utf-8")
        except json.JSONDecodeError:
            pass

        raw_audio = out_dir / "raw_audio.%(ext)s"
        run_cmd(
            [
                "yt-dlp",
                "--no-playlist",
                "-f",
                "bestaudio/best",
                "-x",
                "--audio-format",
                "wav",
                "--postprocessor-args",
                "ffmpeg:-ar 16000 -ac 1",
                "--write-auto-subs",
                "--sub-langs",
                "en.*",
                "--sub-format",
                "vtt",
                "-o",
                str(raw_audio),
                *cookie_args,
                source,
            ]
        )
        downloaded_wav = out_dir / "raw_audio.wav"
        if not downloaded_wav.exists():
            print("ERROR: Expected audio file raw_audio.wav was not created by yt-dlp.", file=sys.stderr)
            sys.exit(1)
        downloaded_wav.replace(wav_path)
    else:
        src_path = Path(source).expanduser().resolve()
        if not src_path.exists():
            print(f"ERROR: Local file not found: {src_path}", file=sys.stderr)
            sys.exit(1)
        run_cmd(
            [
                "ffmpeg",
                "-y",
                "-i",
                str(src_path),
                "-vn",
                "-ar",
                "16000",
                "-ac",
                "1",
                "-c:a",
                "pcm_s16le",
                str(wav_path),
            ]
        )

    return wav_path


def detect_audio_peaks(wav_path: Path, out_dir: Path, window_sec: float = 2.0, top_k: int = 15) -> list[dict]:
    """Pure-stdlib RMS loudness spike detector (zero extra dependencies)."""
    peaks: list[dict] = []
    with wave.open(str(wav_path), "rb") as wf:
        rate = wf.getframerate()
        n_channels = wf.getnchannels()
        sampwidth = wf.getsampwidth()
        if sampwidth != 2:
            return peaks

        frames_per_win = max(1, int(rate * window_sec))
        window_rms: list[tuple[float, float]] = []
        idx = 0
        while True:
            raw = wf.readframes(frames_per_win)
            if not raw:
                break
            count = len(raw) // 2
            samples = struct.unpack(f"<{count}h", raw)
            if n_channels > 1:
                samples = samples[::n_channels]
            if not samples:
                break
            mean_sq = sum(s * s for s in samples) / len(samples)
            rms = math.sqrt(mean_sq)
            db = 20.0 * math.log10(max(rms, 1.0) / 32768.0)
            window_rms.append((idx * window_sec, db))
            idx += 1

    if not window_rms:
        return peaks

    avg_db = sum(d for _, d in window_rms) / len(window_rms)
    ranked = sorted(window_rms, key=lambda x: x[1], reverse=True)

    # Deduplicate spikes within 12 seconds of each other
    selected: list[tuple[float, float]] = []
    for ts, db in ranked:
        if all(abs(ts - prev_ts) >= 12.0 for prev_ts, _ in selected):
            selected.append((ts, db))
        if len(selected) >= top_k:
            break

    selected.sort(key=lambda x: x[0])
    for ts, db in selected:
        peaks.append(
            {
                "timestamp": fmt_mmss(ts),
                "seconds": round(ts, 2),
                "db": round(db, 2),
                "delta_above_avg_db": round(db - avg_db, 2),
            }
        )

    (out_dir / "audio_peaks.json").write_text(json.dumps(peaks, indent=2), encoding="utf-8")
    return peaks


def transcribe_wav(wav_path: Path, out_dir: Path, model_name: str, language: str | None) -> None:
    try:
        from faster_whisper import WhisperModel
    except ImportError:
        print(
            "ERROR: faster-whisper is not installed. Run: pip install faster-whisper\n"
            "Or re-run with --skip-whisper to inspect yt-dlp subtitles instead.",
            file=sys.stderr,
        )
        sys.exit(1)

    print(f"[whisper] Loading model '{model_name}' (CPU, int8)...")
    model = WhisperModel(model_name, device="cpu", compute_type="int8")
    segments_iter, info = model.transcribe(
        str(wav_path),
        language=language,
        vad_filter=True,
        word_timestamps=True,
    )

    segments_out = []
    readable_lines = []
    for seg in segments_iter:
        words = []
        if seg.words:
            for w in seg.words:
                words.append(
                    {
                        "word": w.word.strip(),
                        "start": round(float(w.start), 3),
                        "end": round(float(w.end), 3),
                    }
                )
        text = seg.text.strip()
        segments_out.append(
            {
                "start": round(float(seg.start), 3),
                "end": round(float(seg.end), 3),
                "text": text,
                "words": words,
            }
        )
        readable_lines.append(f"[{fmt_mmss(seg.start)} - {fmt_mmss(seg.end)}] {text}")

    payload = {
        "language": getattr(info, "language", language or "en"),
        "duration": round(float(getattr(info, "duration", 0.0)), 2),
        "segments": segments_out,
    }
    (out_dir / "transcript_words.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")
    (out_dir / "transcript_readable.txt").write_text("\n".join(readable_lines) + "\n", encoding="utf-8")
    print(f"[done] Wrote {len(segments_out)} segments to {out_dir / 'transcript_readable.txt'}")


def fetch_live_chat(source: str, out_dir: Path, cookies_browser: str | None) -> Path | None:
    """Download YouTube chat replay. Non-fatal: chat is a bonus signal, so a
    failure (no replay saved, Twitch/Kick URL, rate limit) only warns."""
    cookie_args = ["--cookies-from-browser", cookies_browser] if cookies_browser else []
    cmd = ["yt-dlp", "--no-playlist", "--skip-download", "--write-subs", "--sub-langs", "live_chat",
           "-o", str(out_dir / "chat.%(ext)s"), *cookie_args, source]
    print(f"[run] {' '.join(cmd)}")
    print("[chat] Downloading chat replay (long streams can take several minutes)...")
    subprocess.run(cmd, check=False)
    found = sorted(out_dir.glob("chat*.live_chat.json"))
    if not found:
        print("[warn] No chat replay downloaded (none saved on this video, or not a YouTube "
              "stream). For Twitch, export chat with TwitchDownloaderCLI and pass --chat-file.",
              file=sys.stderr)
        return None
    return found[0]


def _vtt_ts(ts: str) -> float:
    h, m, rest = ts.split(":")
    return int(h) * 3600 + int(m) * 60 + float(rest)


def transcript_from_vtt(out_dir: Path) -> bool:
    """Build transcript files from yt-dlp auto-subtitles (fallback when Whisper is skipped).

    YouTube auto-captions repeat each line as it scrolls; repeated lines are dropped.
    Word timing is spread evenly across each cue, so captions are approximate.
    """
    vtts = sorted(out_dir.glob("raw_audio*.vtt"))
    if not vtts:
        return False
    cue_re = re.compile(r"(\d+:\d{2}:\d{2}\.\d{3})\s+-->\s+(\d+:\d{2}:\d{2}\.\d{3})")
    segments, readable, seen_last = [], [], ""
    lines = vtts[0].read_text(encoding="utf-8", errors="replace").splitlines()
    i = 0
    while i < len(lines):
        m = cue_re.search(lines[i])
        i += 1
        if not m:
            continue
        start, end = _vtt_ts(m.group(1)), _vtt_ts(m.group(2))
        body = []
        while i < len(lines) and lines[i].strip():
            body.append(re.sub(r"<[^>]+>", "", lines[i]).strip())
            i += 1
        new_lines = [b for b in body if b and b != seen_last]
        if body:
            seen_last = body[-1]
        if end - start < 0.05 or not new_lines:
            continue
        text = " ".join(new_lines)
        toks = text.split()
        step = (end - start) / max(1, len(toks))
        words = [
            {"word": t, "start": round(start + k * step, 3), "end": round(start + (k + 1) * step, 3)}
            for k, t in enumerate(toks)
        ]
        segments.append({"start": round(start, 3), "end": round(end, 3), "text": text, "words": words})
        readable.append(f"[{fmt_mmss(start)} - {fmt_mmss(end)}] {text}")
    if not segments:
        return False
    payload = {"language": "en", "duration": segments[-1]["end"], "segments": segments, "source": "auto-subtitles"}
    (out_dir / "transcript_words.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")
    (out_dir / "transcript_readable.txt").write_text("\n".join(readable) + "\n", encoding="utf-8")
    print(f"[subs] Built transcript from auto-subtitles ({len(segments)} segments, approximate word timing).")
    return True


def main() -> None:
    parser = argparse.ArgumentParser(description="Ingest stream/VOD audio and transcribe with faster-whisper.")
    parser.add_argument("source", help="YouTube/Twitch/Kick URL or local video/audio file path")
    parser.add_argument("--out-dir", default="./clip_workspace", help="Output directory (default: ./clip_workspace)")
    parser.add_argument("--model", default="base.en", help="faster-whisper model (default: base.en)")
    parser.add_argument("--language", default=None, help="Optional language code (e.g. en)")
    parser.add_argument("--cookies-from-browser", default=None, help="Browser name for yt-dlp cookies (e.g. chrome)")
    parser.add_argument("--skip-whisper", action="store_true", help="Skip Whisper; build the transcript from YouTube auto-subtitles (URLs only)")
    parser.add_argument("--with-chat", action="store_true", help="Also download YouTube chat replay and find chat hype spikes")
    parser.add_argument("--chat-file", default=None, help="Local chat export (TwitchDownloader JSON, yt-dlp live_chat.json, or seconds,message CSV)")
    parser.add_argument("--chat-lag", type=float, default=8.0, help="Seconds chat trails the stream (default 8)")
    args = parser.parse_args()

    out_dir = Path(args.out_dir).expanduser().resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    wav_path = ingest_audio(args.source, out_dir, args.cookies_from_browser)
    peaks = detect_audio_peaks(wav_path, out_dir)
    print(f"[peaks] Detected {len(peaks)} top audio spikes -> {out_dir / 'audio_peaks.json'}")

    chat_path = Path(args.chat_file).expanduser() if args.chat_file else None
    if chat_path is None and args.with_chat and is_url(args.source):
        chat_path = fetch_live_chat(args.source, out_dir, args.cookies_from_browser)
    if chat_path is not None:
        sys.path.insert(0, str(Path(__file__).resolve().parent))
        import chat_peaks  # bundled next to this script

        chat_peaks.run(chat_path, out_dir, lag=args.chat_lag)

    if not args.skip_whisper:
        transcribe_wav(wav_path, out_dir, args.model, args.language)
    else:
        print("[skip] Skipped faster-whisper transcription (--skip-whisper set).")
        if not transcript_from_vtt(out_dir):
            print(
                "[warn] No usable subtitles found, so there is no transcript. "
                "Install faster-whisper (pip install faster-whisper) and re-run without --skip-whisper.",
                file=sys.stderr,
            )


if __name__ == "__main__":
    main()
