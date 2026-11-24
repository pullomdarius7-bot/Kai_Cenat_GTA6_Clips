"""Clip 2: Adaptive Triggers Ruined His First Robbery (Archetype B, 40/60 split-screen).

Usage: python3 render_clip02.py [workspace_dir]
"""
import sys
from pathlib import Path

import clipkit as ck

WS = Path(sys.argv[1] if len(sys.argv) > 1 else "workspaces/VZqAPdUvqnQ")
SRC = WS / "raw/clip02_src.mp4"

# (src_start, src_end, cam_zoom, gameplay_zoom)
SEGS = [
    (2.70, 7.22, 1.00, 1.00),    # "oh she like that... LUCIA like that... oh shit"
    (7.22, 15.90, 1.00, 1.10),   # "okay... this is a stick up, hands up... stick up"  (gameplay pushed in)
    #  15.90-28.30 CUT: 12s of game-only audio / dead air
    (28.30, 29.68, 1.00, 1.00),  # "Don't-- wait"
    (29.68, 32.00, 1.40, 1.00),  # "ADAPTIVE TRIGGERS?!"  <- midpoint spike, facecam punch-in
    (32.00, 34.05, 1.60, 1.00),  # "adaptive triggers is on, turn this off, NO NO NO"  hard cut mid-yell
]


def ed(t):
    """Source time -> edited time."""
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


# Caption cues (source times from Whisper words; ending words from the verified handoff transcript)
raw = [
    (2.82, c(("OH", W), ("SHE", W), ("LIKE", W))),
    (3.78, c(("THAT", W))),
    (4.04, c(("OH", W), ("OH", W), ("LUCIA", C))),
    (4.68, c(("LIKE", W), ("THAT", W))),
    (5.24, c(("OH", W), ("THIS", W), ("OH", W))),
    (6.10, c(("SHE", W), ("LIKE", W))),
    (6.38, c(("OH", W), ("SH*T", Y))),
    (7.22, c(("OKAY", W))),
    (10.40, c(("THIS", W), ("IS", W), ("A", W))),
    (11.20, c(("STICK", Y), ("UP", Y))),
    (11.60, c(("HANDS", Y), ("UP!", Y))),
    (12.90, c(("F*CKING", W), ("STICK", W), ("UP", W))),
    (28.32, c(("DON'T--", W))),
    (29.20, c(("WAIT...", W))),
    (29.70, c(("ADAPTIVE", R), ("TRIGGERS?!", Y))),
    (31.06, c(("ADAPTIVE...", R))),
    (32.00, c(("ADAPTIVE", R), ("TRIGGERS", R), ("IS ON", Y))),
    (33.00, c(("TURN", W), ("THIS", W), ("OFF!", R))),
]
cues = []
for i, (t, txt) in enumerate(raw):
    end = ed(raw[i + 1][0]) if i + 1 < len(raw) else ed(33.50)
    cues.append((ed(t), end, txt, False))
cues.append((ed(33.50), T, r"{\c" + R + "}NO NO NO!", True))

tags = [
    (ed(2.82), ed(7.22), "*LOCKED IN*", "cyan"),
    (ed(28.30), ed(29.68), "*TRIGGER LOCKS UP*", "yellow"),
    (ed(29.68), T, "*PANICKING*", "red"),
]

overlay = ck.build_overlay(WS / "artifacts/clip02_overlay.png",
                           "PS5 CONTROLLERS RUINED HIS\nFIRST GTA 6 ROBBERY",
                           "Source: @KaiCenatLive (YouTube / Twitch)", banner_y=40, matte_h=300)
ass = ck.build_ass(WS / "artifacts/clip02.ass", cues, tags, cap_y=1068, tag_y=1183)
out = WS / "exports/clip02_adaptive_triggers_FINAL.mp4"
total = ck.render_split(
    SRC, SEGS,
    cam=(40, 348, 312, 222), face=(195, 485),
    bot=(500, 60, 1217, 960),   # gameplay area right of the facecam/chat column, inside the letterbox bars
    overlay_png=overlay, ass_path=ass, out=out,
    sfx=[("thump", ed(29.68))],
)
print(f"wrote {out} ({total:.2f}s)")
