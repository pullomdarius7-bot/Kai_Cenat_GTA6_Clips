"""Burn the @viralclipppps avatar watermark onto the finished clips.

Placement: left edge, just under the header -- clear of the hook banner, credit pill, captions,
status tags, and the bottom 25% where TikTok/Reels/Shorts draw their UI.

Usage: python3 add_watermark.py [workspace_dir]
"""
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).parent
WS = Path(sys.argv[1] if len(sys.argv) > 1 else ROOT / "workspaces/VZqAPdUvqnQ")
AVATAR = ROOT / "branding/avatar_profile_1080.png"
SIZE, RING = 180, 6

# clip file -> (x, y) of the watermark's top-left corner
CLIPS = {
    "clip01_prayer_FINAL.mp4": (24, 322),            # split layout: top-left of facecam pane
    "clip02_adaptive_triggers_FINAL.mp4": (24, 322),
    "clip03_new_zealand_FINAL.mp4": (24, 420),       # full-face crop: under the credit pill, left of face
    "clip04_2k_basketball_FINAL.mp4": (24, 322),
    "clip05_screen_narration_FINAL.mp4": (24, 322),
}


def build_badge(path):
    full = SIZE + 2 * RING
    av = Image.open(AVATAR).convert("RGB").resize((SIZE, SIZE), Image.LANCZOS)
    badge = Image.new("RGBA", (full, full), (0, 0, 0, 0))
    d = ImageDraw.Draw(badge)
    d.ellipse([0, 0, full - 1, full - 1], fill=(250, 200, 0, 255))  # yellow ring
    mask = Image.new("L", (SIZE, SIZE), 0)
    ImageDraw.Draw(mask).ellipse([0, 0, SIZE - 1, SIZE - 1], fill=255)
    badge.paste(av, (RING, RING), mask)
    badge.save(path)
    return path


def main():
    badge = build_badge(WS / "artifacts/watermark_badge.png")
    for name, (x, y) in CLIPS.items():
        src = WS / "exports" / name
        if not src.exists():
            print("missing", src)
            continue
        out = src.with_name(name.replace("_FINAL.mp4", "_POST.mp4"))
        subprocess.run(["ffmpeg", "-y", "-nostdin", "-loglevel", "error", "-i", str(src), "-i", str(badge),
                        "-filter_complex", f"[1:v]format=rgba,colorchannelmixer=aa=0.95[wm];[0:v][wm]overlay={x}:{y}",
                        "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p",
                        "-c:a", "copy", "-movflags", "+faststart", str(out)], check=True)
        print("wrote", out)


if __name__ == "__main__":
    main()
