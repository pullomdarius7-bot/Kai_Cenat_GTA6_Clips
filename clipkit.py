"""Reusable 9:16 edit engine for the Kai Cenat GTA 6 clips.

A clip is described by a config dict (see render_clip03.py):
  - segments: list of (first_word_idx, last_word_idx, zoom) from the Whisper word list
  - layout "crop9x16": full-bleed vertical crop that follows Kai's face (OpenCV), eyes at a fixed height
  - hook banner + credit pill + optional chyron drawn as one PNG overlay
  - kinetic captions (<=3 words, color highlights) + status tags rendered with libass
  - optional synthesized SFX (bass thump / whoosh) at given words, then -14 LUFS loudness
"""
import json
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

FONT = "/usr/share/fonts/opentype/inter/InterDisplay-Black.otf"
FONT_XB = "/usr/share/fonts/opentype/inter/Inter-ExtraBold.otf"
COL = {"white": "&H00FFFFFF&", "yellow": "&H0000E1FF&", "red": "&H003C3CFF&", "cyan": "&H00FFE100&"}


def ass_ts(t):
    cs = int(round(t * 100))
    return f"{cs // 360000}:{cs // 6000 % 60:02}:{cs // 100 % 60:02}.{cs % 100:02}"


def load_words(path):
    return [tuple(w) for w in json.loads(Path(path).read_text())]


def segment_times(words, segs, pad_in=0.06, pad_out=0.12):
    """Turn word-index ranges into (src_start, src_end, zoom) without clipping neighbouring words."""
    out = []
    for seg in segs:
        a, b, z = seg[:3]
        s = words[a][0] - pad_in
        if a > 0:
            s = max(s, words[a - 1][1] + 0.01)
        e = words[b][1] + pad_out
        if b + 1 < len(words):
            e = min(e, words[b + 1][0] - 0.01)
        out.append((round(max(0, s), 3), round(e, 3), z) + tuple(seg[3:]))
    return out


def track_x_expr(src, s, e, cw, step=0.12):
    """Follow the face across a segment: piecewise-linear crop-x expression (smoothed)."""
    times = [s + k * step for k in range(int((e - s) / step) + 1)]
    pts = []
    for t in times:
        fx, _ = detect_face_x(src, [t])
        pts.append(fx)
    # fill misses (detect_face_x returns centre 960 when nothing found) with the previous good value
    good = [p if p != 960.0 else None for p in pts]
    last = next((p for p in good if p is not None), 960.0)
    filled = []
    for p in good:
        last = p if p is not None else last
        filled.append(last)
    sm = [sum(filled[max(0, i - 2): i + 3]) / len(filled[max(0, i - 2): i + 3]) for i in range(len(filled))]
    xs = [min(max(0, v - cw / 2), 1920 - cw) for v in sm]
    rel = [t - s for t in times]
    expr = f"{xs[-1]:.0f}"
    for i in range(len(xs) - 2, -1, -1):
        t0, t1, x0, x1 = rel[i], rel[i + 1], xs[i], xs[i + 1]
        expr = f"if(lt(t,{t1:.3f}),{x0:.0f}+({x1 - x0:.0f})*(t-{t0:.3f})/{t1 - t0:.3f},{expr})"
    return expr


def detect_face_x(src, times, src_w=1920, src_h=1080):
    """Median face centre (x, eye_y) over a few sample times. Falls back to frame centre."""
    import cv2
    import numpy as np

    casc = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    xs, ys = [], []
    for t in times:
        raw = subprocess.run(
            ["ffmpeg", "-nostdin", "-loglevel", "error", "-ss", f"{t:.2f}", "-i", str(src),
             "-frames:v", "1", "-f", "rawvideo", "-pix_fmt", "gray", "-"],
            capture_output=True).stdout
        if len(raw) < src_w * src_h:
            continue
        img = np.frombuffer(raw[: src_w * src_h], np.uint8).reshape(src_h, src_w)
        faces = casc.detectMultiScale(img, 1.1, 6, minSize=(90, 90))
        if len(faces):
            x, y, w, h = max(faces, key=lambda f: f[2] * f[3])
            xs.append(x + w / 2)
            ys.append(y + h * 0.42)  # eyes sit ~42% down the detected face box
    if not xs:
        return src_w / 2, src_h * 0.4
    return float(np.median(xs)), float(np.median(ys))


def build_overlay(path, banner, credit, chyron=None, banner_y=150, matte_h=0):
    img = Image.new("RGBA", (1080, 1920), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    if matte_h:
        d.rectangle([0, 0, 1080, matte_h], fill=(12, 12, 14, 255))
    f = ImageFont.truetype(FONT, 58)
    bb = d.multiline_textbbox((0, 0), banner, font=f, align="center", spacing=6)
    tw, th = bb[2] - bb[0], bb[3] - bb[1]
    bx = (1080 - tw) // 2 - 36
    d.rounded_rectangle([bx, banner_y, bx + tw + 72, banner_y + th + 48], radius=28, fill="white")
    d.multiline_text((540, banner_y + 24 - bb[1] + th // 2), banner, font=f, fill="black",
                     anchor="mm", align="center", spacing=6)
    f2 = ImageFont.truetype(FONT_XB, 26)
    cb = d.textbbox((0, 0), credit, font=f2)
    cw = cb[2] - cb[0]
    cy = banner_y + th + 48 + 18
    d.rounded_rectangle([540 - cw // 2 - 20, cy, 540 + cw // 2 + 20, cy + 44], radius=22,
                        fill=(0, 0, 0, 120), outline=(255, 255, 255, 140), width=2)
    d.text((540, cy + 22), credit, font=f2, fill=(240, 240, 240, 255), anchor="mm")
    if chyron:
        f3 = ImageFont.truetype(FONT_XB, 30)
        hb = d.textbbox((0, 0), chyron, font=f3)
        hw = hb[2] - hb[0]
        x1 = 1080 - 40
        d.rounded_rectangle([x1 - hw - 44, 60, x1, 110], radius=25, fill=(220, 30, 60, 230))
        d.text((x1 - hw / 2 - 22, 85), chyron, font=f3, fill="white", anchor="mm")
    img.save(path)
    return path


def build_ass(path, cues, tags, cap_y, tag_y):
    head = """[Script Info]
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
    rows = []
    for s, e, txt, big in cues:
        pop = r"{\fscx80\fscy80\t(0,80,\fscx100\fscy100)}"
        size = r"{\fs150\bord10}" if big else ""
        rows.append(f"Dialogue: 1,{ass_ts(s)},{ass_ts(e)},Cap,,0,0,0,,{{\\an5\\pos(540,{cap_y})}}{pop}{size}{txt}")
    for s, e, txt, col in tags:
        rows.append(f"Dialogue: 0,{ass_ts(s)},{ass_ts(e)},Tag,,0,0,0,,{{\\an5\\pos(540,{tag_y})\\c{COL[col]}}}{txt}")
    Path(path).write_text(head + "\n".join(rows) + "\n", encoding="utf-8")
    return path


def make_cues(words, segs_t, seg_idx, replace, colors, max_words=3, big_last=None):
    """Captions from the kept words only, timed on the edited timeline."""
    items = []
    off = 0.0
    for (s, e, *_), (a, b, *_) in zip(segs_t, seg_idx):
        for i in range(a, b + 1):
            w = replace.get(i, words[i][2])
            if w:
                items.append((off + max(0.0, words[i][0] - s), i, w.upper()))
        items.append(None)  # segment break forces a new cue
        off += e - s
    total = off
    groups, cur = [], []
    for it in items:
        if it is None:
            if cur:
                groups.append(cur)
            cur = []
            continue
        cur.append(it)
        if len(cur) == max_words or it[2].endswith((".", "?", "!")):
            groups.append(cur)
            cur = []
    if cur:
        groups.append(cur)
    cues = []
    for gi, g in enumerate(groups):
        start = g[0][0]
        end = groups[gi + 1][0][0] if gi + 1 < len(groups) else total
        txt = " ".join(r"{\c" + COL[colors.get(i, "white")] + "}" + w.rstrip(",") for _, i, w in g)
        cues.append((start, end, txt, big_last and gi == len(groups) - 1))
    return cues, total


def sfx_filter(kind, at, label):
    ms = int(at * 1000)
    if kind == "thump":
        src = "aevalsrc='0.9*sin(2*PI*(48+40*exp(-t*18))*t)*exp(-t*7)':s=48000:d=0.6"
    else:  # whoosh: band-passed noise swell
        src = ("anoisesrc=d=0.7:c=pink:a=0.6:r=48000,bandpass=f=1800:w=1400,"
               "afade=t=in:d=0.45:curve=exp,afade=t=out:st=0.45:d=0.25,volume=0.35")
    return f"{src},adelay={ms}|{ms},aformat=channel_layouts=stereo[{label}]"


def render_split(src, segs, cam, face, bot, overlay_png, ass_path, out,
                 header_h=300, cam_h=768, sfx=(), fps=30):
    """40/60 split: small stream facecam box on top, gameplay crop below, dark header for the banner.

    segs: (src_start, src_end, cam_zoom, bottom_zoom)
    cam:  (x, y, w, h) of the facecam crop in the 1920x1080 source (aspect must be 1080:cam_h)
    face: (x, y) of Kai's eyes in the source, kept at the same relative height on every zoom
    bot:  (x, y, w, h) of the gameplay crop (aspect 1080:(1920-header_h-cam_h))
    """
    seam = header_h + cam_h
    bot_h = 1920 - seam
    cx, cy, cw, ch = cam
    fxr, fyr = (face[0] - cx) / cw, (face[1] - cy) / ch
    bx, by, bw, bh = bot
    n = len(segs)
    fc = [f"[0:v]split={n}[" + "][".join(f"vs{i}" for i in range(n)) + "]",
          f"[0:a]asplit={n}[" + "][".join(f"as{i}" for i in range(n)) + "]"]
    for i, (s, e, cz, bz) in enumerate(segs):
        zw, zh = cw / cz, ch / cz
        zx = min(max(cx, face[0] - fxr * zw), cx + cw - zw)
        zy = min(max(cy, face[1] - fyr * zh), cy + ch - zh)
        bzw, bzh = bw / bz, bh / bz
        bzx, bzy = bx + (bw - bzw) / 2, by + (bh - bzh) / 2
        d = e - s
        fc.append(f"[vs{i}]trim={s}:{e},setpts=PTS-STARTPTS,fps={fps},split=2[c{i}][b{i}]")
        fc.append(f"[c{i}]crop={zw:.0f}:{zh:.0f}:{zx:.0f}:{zy:.0f},scale=1080:{cam_h}:flags=lanczos,setsar=1[cam{i}]")
        fc.append(f"[b{i}]crop={bzw:.0f}:{bzh:.0f}:{bzx:.0f}:{bzy:.0f},scale=1080:{bot_h}:flags=lanczos,setsar=1[bot{i}]")
        fc.append(f"color=c=0x0c0c0e:s=1080x1920:r={fps}:d={d:.3f}[bg{i}]")
        fc.append(f"[bg{i}][cam{i}]overlay=0:{header_h}[t{i}]")
        fc.append(f"[t{i}][bot{i}]overlay=0:{seam}:shortest=1,trim=duration={d:.3f}[v{i}]")
        fc.append(f"[as{i}]atrim={s}:{e},asetpts=PTS-STARTPTS,afade=t=in:d=0.01,"
                  f"afade=t=out:st={d - 0.012:.3f}:d=0.012[a{i}]")
    fc.append("".join(f"[v{i}][a{i}]" for i in range(n)) + f"concat=n={n}:v=1:a=1[vc][ac]")
    mix = "[ac]"
    for k, (kind, at) in enumerate(sfx):
        fc.append(sfx_filter(kind, at, f"sfx{k}"))
        mix += f"[sfx{k}]"
    fc.append(f"{mix}amix=inputs={1 + len(sfx)}:duration=first:normalize=0,"
              "loudnorm=I=-14:TP=-1.5:LRA=11,aresample=48000[aout]")
    fc.append(f"[vc][1:v]overlay=0:0[vh];[vh]ass={ass_path}[vout]")
    total = sum(e - s for s, e, *_ in segs)
    subprocess.run(["ffmpeg", "-y", "-nostdin", "-loglevel", "error", "-i", str(src), "-i", str(overlay_png),
                    "-filter_complex", ";".join(fc), "-map", "[vout]", "-map", "[aout]",
                    "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p",
                    "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart",
                    "-t", f"{total:.3f}", str(out)], check=True)
    return total


def render_crop9x16(src, segs_t, overlay_png, ass_path, out, eye_frac=0.36, sfx=(), fps=30):
    """Full-bleed vertical crop following Kai's face; per-segment zoom with eyes locked at eye_frac."""
    n = len(segs_t)
    fc = [f"[0:v]split={n}[" + "][".join(f"vs{i}" for i in range(n)) + "]",
          f"[0:a]asplit={n}[" + "][".join(f"as{i}" for i in range(n)) + "]"]
    for i, seg in enumerate(segs_t):
        s, e, z = seg[:3]
        track = len(seg) > 3 and seg[3] == "track"
        fx, fy = detect_face_x(src, [s + (e - s) * k / 4 for k in range(1, 4)])
        ch = 1080 / z
        cw = ch * 9 / 16
        x = f"{min(max(0, fx - cw / 2), 1920 - cw):.0f}"
        if track:
            x = "'" + track_x_expr(src, s, e, cw) + "'"
        y = min(max(0, fy - ch * eye_frac), 1080 - ch)
        print(f"seg {i}: {s:.2f}-{e:.2f}s zoom {z} face=({fx:.0f},{fy:.0f}){' tracked' if track else ''}")
        fc.append(f"[vs{i}]trim={s}:{e},setpts=PTS-STARTPTS,"
                  f"crop={cw:.0f}:{ch:.0f}:{x}:{y:.0f},scale=1080:1920:flags=lanczos,setsar=1,fps={fps}[v{i}]")
        fc.append(f"[as{i}]atrim={s}:{e},asetpts=PTS-STARTPTS,afade=t=in:d=0.01,"
                  f"afade=t=out:st={e - s - 0.012:.3f}:d=0.012[a{i}]")
    fc.append("".join(f"[v{i}][a{i}]" for i in range(n)) + f"concat=n={n}:v=1:a=1[vc][ac]")
    mix = "[ac]"
    for k, (kind, at) in enumerate(sfx):
        fc.append(sfx_filter(kind, at, f"sfx{k}"))
        mix += f"[sfx{k}]"
    fc.append(f"{mix}amix=inputs={1 + len(sfx)}:duration=first:normalize=0,"
              "loudnorm=I=-14:TP=-1.5:LRA=11,aresample=48000[aout]")
    fc.append(f"[vc][1:v]overlay=0:0[vh];[vh]ass={ass_path}[vout]")
    total = sum(seg[1] - seg[0] for seg in segs_t)
    subprocess.run(["ffmpeg", "-y", "-nostdin", "-loglevel", "error", "-i", str(src), "-i", str(overlay_png),
                    "-filter_complex", ";".join(fc), "-map", "[vout]", "-map", "[aout]",
                    "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p",
                    "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart",
                    "-t", f"{total:.3f}", str(out)], check=True)
    return total
