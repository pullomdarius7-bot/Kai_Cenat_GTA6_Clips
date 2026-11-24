"""Clip 5: 13 Years of Hype Ruined by Screen Narration -- Archetype A, 40/60 split-screen.

The downloaded window ends right on "Press square to enable", so the clip hard-cuts on the
robot voice (cliffhanger/loop) instead of the "OFF OFF OFF" payoff.

Usage: python3 render_clip05.py [workspace_dir]
"""
import sys
from pathlib import Path

import clipkit as ck

WS = Path(sys.argv[1] if len(sys.argv) > 1 else "workspaces/VZqAPdUvqnQ")
SRC = WS / "raw/clip05_src.mp4"

# (src_start, src_end, cam_zoom, gameplay_zoom)
SEGS = [
    (0.00, 3.95, 1.00, 1.00),    # "waiting 13 years. Holy shit, holy shit. Okay here we go. I'm done talking."
    (4.20, 6.00, 1.00, 1.00),    # "Everybody clap it up. Here we go."
    (7.00, 8.35, 1.10, 1.00),    # "Oh my God, I'm scared."
    #  8.35-13.40 CUT: fire monitor tangent
    (13.40, 14.40, 1.15, 1.00),  # "I have no shirt on."
    #  14.40-21.70 CUT: "let's get into this / do I sound good" + laughing
    (21.70, 22.75, 1.20, 1.00),  # "Oh my f*cking God."
    (25.60, 26.40, 1.20, 1.00),  # "Oh my God."
    (27.80, 28.65, 1.25, 1.00),  # "Oh my God."  (screen goes black, game loading)
    (30.20, 32.05, 1.60, 1.00),  # robot voice: "PRESS SQUARE TO ENABLE--"  hard cut
]


def ed(t):
    off = 0.0
    for s, e, *_ in SEGS:
        if s <= t <= e:
            return off + t - s
        off += e - s
    raise ValueError(t)


T = sum(e - s for s, e, *_ in SEGS)
W, Y, R, C = (ck.COL[k] for k in ("white", "yellow", "red", "cyan"))


def c(*parts):
    return " ".join(r"{\c" + col + "}" + w for w, col in parts)


raw = [
    (0.00, c(("WAITING", W), ("13", Y), ("YEARS", Y))),
    (1.18, c(("HOLY", W), ("SH*T", W))),
    (2.18, c(("HOLY", W), ("SH*T", W))),
    (2.56, c(("OKAY,", W), ("HERE", W), ("WE GO", W))),
    (3.30, c(("I'M", W), ("DONE", W), ("TALKING", W))),
    (4.26, c(("EVERYBODY", Y), ("CLAP", Y), ("IT UP!", Y))),
    (5.04, c(("HERE", W), ("WE", W), ("GO", W))),
    (7.04, c(("OH", W), ("MY", W), ("GOD", W))),
    (7.94, c(("I'M", W), ("SCARED", C))),
    (13.40, c(("I", W), ("HAVE", W), ("NO SHIRT", Y))),
    (14.08, c(("ON", Y))),
    (21.78, c(("OH", W), ("MY", W), ("F*CKING", W))),
    (22.46, c(("GOD", Y))),
    (25.66, c(("OH", W), ("MY", W), ("GOD", W))),
    (27.86, c(("OH", W), ("MY", W), ("GOD...", W))),
]
cues = []
for i, (t, txt) in enumerate(raw):
    end = ed(raw[i + 1][0]) if i + 1 < len(raw) else ed(30.20)
    cues.append((ed(t), end, txt, False))

narr_t = ed(30.28)
# Robot narration caption in the (now black) gameplay pane, monospace + cyan
robot = (r"{\fnDejaVu Sans Mono\b1\fs54\bord4\c" + C + r"}[PRESS SQUARE TO ENABLE\N SCREEN NARRATION]")
extra = [(narr_t, T, 540, 1300, robot)]

tags = [
    (ed(13.40), ed(28.65), "*PEAK HYPE*", "yellow"),
    (narr_t, T, "*MOOD KILLED*", "red"),
]
overlay = ck.build_overlay(WS / "artifacts/clip05_overlay.png",
                           "WAITED 13 YEARS FOR GTA 6\nJUST FOR THIS TO HAPPEN",
                           "Source: @KaiCenatLive (YouTube / Twitch)", banner_y=40, matte_h=300)
ass = ck.build_ass(WS / "artifacts/clip05.ass", cues, tags, cap_y=1068, tag_y=1183, extra=extra)
out = WS / "exports/clip05_screen_narration_FINAL.mp4"
total = ck.render_split(
    SRC, SEGS,
    cam=(83, 350, 309, 220), face=(240, 470),
    bot=(551, 0, 1369, 1080),   # GTA 6 home screen / loading art, right of the facecam + chat column
    overlay_png=overlay, ass_path=ass, out=out,
    # cinematic pad builds under the hype, then stops dead the frame the robot voice starts
    sfx=[(f"pad:{narr_t - 0.05:.2f}", 0.0)],
)
print(f"wrote {out} ({total:.2f}s)")
