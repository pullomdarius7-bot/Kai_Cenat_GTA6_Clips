"""Render Clip 1 (The 13-Year Prayer) as a finished 1080x1920 vertical video.

Layout (top to bottom):
  0-300     dark header: hook banner (white rounded box) + credit pill
  300-1068  Kai's facecam (40%), zooms per the blueprint
  1068-1920 GTA 6 PS5 screen + live chat (60%)
Captions sit on the seam at y=1068 (well above the bottom 25% UI dead zone).

Usage: python3 render_clip01.py <workspace_dir>
"""
import json
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

WS = Path(sys.argv[1] if len(sys.argv) > 1 else "workspaces/VZqAPdUvqnQ")
SRC = WS / "raw/clip01_src.mp4"
WORDS = json.loads((WS / "artifacts/clip01_words.json").read_text())
OUT = WS / "exports/clip01_prayer_FINAL.mp4"
FONT = "/usr/share/fonts/opentype/inter/InterDisplay-Black.otf"
FONT_XB = "/usr/share/fonts/opentype/inter/Inter-ExtraBold.otf"

HEADER_H, CAM_H = 300, 768
SEAM = HEADER_H + CAM_H  # 1068
BOT_H = 1920 - SEAM  # 852

# Facecam box in the 1920x1080 stream: x 0-376, y ~375-587. Kai's eyes ~ (200, 490).
CAM_X, CAM_Y, CAM_W, CAM_H_SRC = 51, 375, 298, 212  # 1.406 aspect = 1080x768 pane
FACE_CX, FACE_CY = 200, 488

# Edit list: (src_start, src_end, cam_zoom_start, cam_zoom_end)
SEGMENTS = [
    (6.15, 14.85, 1.00, 1.08),   # "I'm scared bro" -> thank-you prayer, slow creep, no cuts
    (14.85, 16.88, 1.08, 1.08),  # "before GTA..." held
    (16.88, 19.95, 1.55, 1.55),  # SHITS -> "I didn't mean to curse God" punch-in (panic beat kept)
    (20.50, 27.66, 1.20, 1.20),  # Lord's Prayer, tight crop
    (27.90, 30.10, 1.20, 1.20),  # breath >0.3s stripped
    (30.55, 30.95, 1.45, 1.45),  # AMEN. punch-in, hard cut right after the syllable
]

# Whisper mishears the prayer; fix to what he actually says (matches the handoff transcript).
REPLACE = {
    24.16: "this", 24.76: "bread,", 25.3: "our", 28.46: "into",
    29.2: "deliver", 29.28: "", 29.38: "", 29.5: "from",
}
YELLOW, RED, WHITE, CYAN = "&H0000E1FF&", "&H003C3CFF&", "&H00FFFFFF&", "&H00FFE100&"


def edited_time(t):
    off = 0.0
    for s, e, *_ in SEGMENTS:
        if s <= t <= e:
            return off + (t - s)
        off += e - s
    return None


def total():
    return sum(e - s for s, e, *_ in SEGMENTS)


def ass_ts(t):
    cs = int(round(t * 100))
    return f"{cs // 360000}:{cs // 6000 % 60:02}:{cs // 100 % 60:02}.{cs % 100:02}"


def build_ass():
    words = []
    for a, b, w in WORDS:
        w = REPLACE.get(a, w)
        if not w:
            continue
        ea = edited_time(a)
        if ea is None:
            continue
        words.append((ea, a, w.upper().strip(",")))

    # Group into cues of <=3 words, breaking on sentence ends and segment boundaries.
    cues, cur = [], []
    for item in words:
        cur.append(item)
        if len(cur) == 3 or item[2].endswith((".", "?")):
            cues.append(cur)
            cur = []
    if cur:
        cues.append(cur)

    def color(src_t, w):
        if w.rstrip(".") in ("13", "YEARS") and src_t < 11:
            return YELLOW
        if w.rstrip(".") == "SHITS" or (19.3 <= src_t <= 19.9):
            return RED
        return WHITE

    lines = []
    T = total()
    for i, c in enumerate(cues):
        start = c[0][0]
        end = cues[i + 1][0][0] if i + 1 < len(cues) else T
        if c[0][2].startswith("AMEN"):
            txt = r"{\fs170\c" + YELLOW + r"\bord10}AMEN."
            lines.append(f"Dialogue: 2,{ass_ts(start)},{ass_ts(T)},Cap,,0,0,0,,{txt}")
            continue
        txt = " ".join(r"{\c" + color(src, w) + "}" + w for _, src, w in c)
        pop = r"{\fscx80\fscy80\t(0,80,\fscx100\fscy100)}"
        lines.append(f"Dialogue: 1,{ass_ts(start)},{ass_ts(end)},Cap,,0,0,0,,{pop}{txt}")

    # Status tags (edited times)
    e = edited_time
    tags = [
        (e(9.54), e(14.85), "*GENUINELY LOCKED IN*", CYAN),
        (e(16.88), e(19.95), "*INSTANT REGRET*", RED),
        (e(20.50) + 0.4, e(30.10), "*DAMAGE CONTROL*", YELLOW),
    ]
    for s, en, t, col in tags:
        lines.append(f"Dialogue: 0,{ass_ts(s)},{ass_ts(en)},Tag,,0,0,0,,{{\\c{col}}}{t}")

    head = f"""[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 2

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Cap,Inter Display Black,92,&H00FFFFFF,&H00FFFFFF,&H00000000,&H80000000,0,0,0,0,100,100,0,0,1,8,3,5,40,40,0,1
Style: Tag,Inter Display Black,44,&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,0,1,0,0,100,100,2,0,1,5,0,5,40,40,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    # Position: captions on the seam, tags just below it
    body = []
    for l in lines:
        pre, txt = l.rsplit(",,", 1)
        y = SEAM if ",Cap," in l else SEAM + 115
        body.append(f"{pre},,{{\\an5\\pos(540,{y})}}{txt}")
    p = WS / "artifacts/clip01.ass"
    p.write_text(head + "\n".join(body) + "\n", encoding="utf-8")
    return p


def build_header():
    img = Image.new("RGBA", (1080, 1920), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, 1080, HEADER_H], fill=(12, 12, 14, 255))
    f = ImageFont.truetype(FONT, 58)
    text = "HE PRAYED BEFORE\nLOADING GTA 6..."
    bb = d.multiline_textbbox((0, 0), text, font=f, align="center", spacing=6)
    tw, th = bb[2] - bb[0], bb[3] - bb[1]
    bx, by = (1080 - tw) // 2 - 36, 40
    d.rounded_rectangle([bx, by, bx + tw + 72, by + th + 48], radius=28, fill="white")
    d.multiline_text((540, by + 24 - bb[1] + th // 2), text, font=f, fill="black",
                     anchor="mm", align="center", spacing=6)
    f2 = ImageFont.truetype(FONT_XB, 26)
    credit = "Source: @KaiCenatLive (YouTube / Twitch)"
    cb = d.textbbox((0, 0), credit, font=f2)
    cw = cb[2] - cb[0]
    cy = by + th + 48 + 22
    d.rounded_rectangle([540 - cw // 2 - 20, cy, 540 + cw // 2 + 20, cy + 44], radius=22,
                        fill=(255, 255, 255, 40), outline=(255, 255, 255, 110), width=2)
    d.text((540, cy + 22), credit, font=f2, fill=(235, 235, 235, 255), anchor="mm")
    p = WS / "artifacts/clip01_header.png"
    img.save(p)
    return p


def cam_filter(i, z0, z1, dur):
    """Crop the facecam, upscale, then zoom around Kai's eyes (eyeline kept consistent)."""
    up = "scale=2160:1536:flags=lanczos"
    base = f"crop={CAM_W}:{CAM_H_SRC}:{CAM_X}:{CAM_Y},{up}"
    # face position inside the upscaled pane
    fx = (FACE_CX - CAM_X) / CAM_W * 2160
    fy = (FACE_CY - CAM_Y) / CAM_H_SRC * 1536
    frames = max(1, int(dur * 60))
    zexpr = f"{z0}+({z1}-{z0})*on/{frames}" if z1 != z0 else f"{z0}"
    # keep eyes at the same relative height as at 100%
    x = f"max(0,min(iw-iw/zoom,{fx}-iw/zoom/2))"
    y = f"max(0,min(ih-ih/zoom,{fy}-({fy}/ih)*ih/zoom))"
    return f"{base},zoompan=z='{zexpr}':x='{x}':y='{y}':d=1:s=1080x768:fps=60"


def main():
    ass = build_ass()
    header = build_header()
    T = total()
    fc = []
    n = len(SEGMENTS)
    fc.append(f"[0:v]split={n}[" + "][".join(f"vs{i}" for i in range(n)) + "]")
    fc.append(f"[0:a]asplit={n}[" + "][".join(f"as{i}" for i in range(n)) + "]")
    for i, (s, e, z0, z1) in enumerate(SEGMENTS):
        fc.append(f"[vs{i}]trim={s}:{e},setpts=PTS-STARTPTS,split=2[c{i}][b{i}]")
        fc.append(f"[c{i}]{cam_filter(i, z0, z1, e - s)},setsar=1[cam{i}]")
        fc.append(f"[b{i}]crop=1369:1080:551:0,scale=1080:{BOT_H}:flags=lanczos,setsar=1[bot{i}]")
        fc.append(f"color=c=0x0c0c0e:s=1080x1920:r=60:d={e - s:.3f}[bg{i}]")
        fc.append(f"[bg{i}][cam{i}]overlay=0:{HEADER_H}[t{i}]")
        fc.append(f"[t{i}][bot{i}]overlay=0:{SEAM}:shortest=1,trim=duration={e - s:.3f}[v{i}]")
        fc.append(f"[as{i}]atrim={s}:{e},asetpts=PTS-STARTPTS,afade=t=in:d=0.01,afade=t=out:st={e - s - 0.012:.3f}:d=0.012[a{i}]")
    fc.append("".join(f"[v{i}][a{i}]" for i in range(n)) + f"concat=n={n}:v=1:a=1[vc][ac]")
    # Single bass thump on "SHITS" (no music: hard cut to silence feel comes from the dry voice)
    thump_at = sum(e - s for s, e, *_ in SEGMENTS[:2])
    fc.append("aevalsrc='0.9*sin(2*PI*(48+40*exp(-t*18))*t)*exp(-t*7)':s=48000:d=0.6,"
              f"adelay={int(thump_at * 1000)}|{int(thump_at * 1000)},aformat=channel_layouts=stereo[sfx]")
    fc.append("[ac][sfx]amix=inputs=2:duration=first:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=11,aresample=48000[aout]")
    fc.append(f"[vc][1:v]overlay=0:0[vh];[vh]ass={ass}[vout]")

    cmd = ["ffmpeg", "-y", "-nostdin", "-loglevel", "error", "-i", str(SRC), "-i", str(header),
           "-filter_complex", ";".join(fc), "-map", "[vout]", "-map", "[aout]",
           "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", "-r", "60",
           "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart",
           "-t", f"{T:.3f}", str(OUT)]
    subprocess.run(cmd, check=True)
    print(f"wrote {OUT} ({T:.2f}s)")


if __name__ == "__main__":
    main()
