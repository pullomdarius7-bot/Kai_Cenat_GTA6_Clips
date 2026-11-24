"""Clip 4: GTA 6 vs. 2K Basketball ("Oh Hell No") -- Archetype B, 40/60 split-screen.

Usage: python3 render_clip04.py [workspace_dir]
"""
import sys
from pathlib import Path

import clipkit as ck

WS = Path(sys.argv[1] if len(sys.argv) > 1 else "workspaces/VZqAPdUvqnQ")
SRC = WS / "raw/clip04_src.mp4"

# (src_start, src_end, cam_zoom, gameplay_zoom)
SEGS = [
    (1.00, 3.95, 1.00, 1.00),    # "okay, let's see basketball."
    #  3.95-11.65 CUT: walking/loading pause + mumbled "oh one"
    (11.65, 12.95, 1.00, 1.10),  # "2K, you're finished"
    (12.95, 15.95, 1.00, 1.10),  # "okay, I can't cross over or nothing"  (gameplay pushed in on the dribble)
    #  15.95-18.50 CUT: dead air
    (18.50, 21.00, 1.40, 1.00),  # "OH HELL NO" x3   <- midpoint spike, facecam punch-in
    (21.00, 23.45, 1.60, 1.00),  # final "OH HELL NO"  hard cut before "you can't quit me"
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


# Whisper hears "hell no" as "how not / how now" -- caption words follow the verified handoff transcript.
raw = [
    (1.04, c(("OKAY,", W))),
    (2.14, c(("LET'S", W), ("SEE", W), ("BASKETBALL", Y))),
    (11.70, c(("2K", C), ("YOU'RE", C), ("FINISHED!", C))),
    (12.92, c(("OKAY...", W))),
    (14.60, c(("I", W), ("CAN'T", W), ("CROSS", Y))),
    (15.28, c(("OVER", Y), ("OR", W), ("NOTHING", W))),
    (18.58, c(("OH", W), ("HELL", R), ("NO", R))),
    (19.64, c(("OH", W), ("HELL", R), ("NO", R))),
    (20.36, c(("HELL", R), ("NO", R))),
    (20.80, c(("HELL", R), ("NO", R))),
]
cues = []
for i, (t, txt) in enumerate(raw):
    end = ed(raw[i + 1][0]) if i + 1 < len(raw) else ed(21.30)
    cues.append((ed(t), end, txt, False))
cues.append((ed(21.30), T, r"{\c" + R + "}OH HELL NO!", True))

tags = [
    (ed(14.60), ed(15.95), "*REALIZATION HITTING*", "yellow"),
    (ed(18.50), T, "*2K IS SAFE*", "red"),
]
overlay = ck.build_overlay(WS / "artifacts/clip04_overlay.png",
                           "HE THOUGHT GTA 6 WAS\nGOING TO END NBA 2K...",
                           "Source: @KaiCenatLive (YouTube / Twitch)", banner_y=40, matte_h=300)
ass = ck.build_ass(WS / "artifacts/clip04.ass", cues, tags, cap_y=1068, tag_y=1183)
out = WS / "exports/clip04_2k_basketball_FINAL.mp4"
total = ck.render_split(
    SRC, SEGS,
    cam=(30, 432, 309, 220), face=(185, 560),
    bot=(420, 0, 1369, 1080),   # court/player area right of the facecam + chat column
    overlay_png=overlay, ass_path=ass, out=out,
    sfx=[("thump", ed(18.55))],
)
print(f"wrote {out} ({total:.2f}s)")
