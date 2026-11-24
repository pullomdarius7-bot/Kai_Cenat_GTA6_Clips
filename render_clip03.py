"""Clip 3: Changed Servers to New Zealand to Beat FOMO (Archetype C, full-bleed 9:16 face crop).

Usage: python3 render_clip03.py [workspace_dir]
"""
import sys
from pathlib import Path

import clipkit as ck

WS = Path(sys.argv[1] if len(sys.argv) > 1 else "workspaces/VZqAPdUvqnQ")
SRC = WS / "raw/clip03_src.mp4"
words = ck.load_words(WS / "artifacts/clip03_words.json")

# (first_word, last_word, zoom) -- word indexes from clip03_words.json
SEGS = [
    (12, 16, 1.00, "track"),  # "We in New Zealand, bitch." -- he's running around, so the crop follows him
    (18, 21, 1.10),   # "don't even ask now"
    (43, 47, 1.00),   # "I did not sleep tonight"         (filler 00:03:53-00:04:01 cut)
    (49, 62, 1.00),   # "...first time in a long time where it felt like Christmas"
    (82, 87, 1.25),   # "but I was in my bed"             (tangent cut)
    (109, 114, 1.25), # "I'm just seeing GTA 6's out."
    (115, 122, 1.25), # "Everybody booing it up. I got FOMO immediately."
    (123, 130, 1.45), # "So what I did, I changed servers immediately"  <- midpoint spike
    (134, 138, 1.45), # "I hopped on that flight"         + whoosh
    (146, 152, 1.60), # "No shirt, no, I'm off the way."  hard cut on last syllable
]
REPLACE = {16: "B*TCH.", 46: "sleep", 113: "6", 114: "IS OUT.", 152: "way."}
COLORS = {14: "yellow", 15: "yellow", 62: "cyan", 121: "red", 122: "red",
          128: "yellow", 129: "yellow", 138: "cyan", 147: "yellow"}

segs_t = ck.segment_times(words, SEGS)
cues, total = ck.make_cues(words, segs_t, SEGS, REPLACE, COLORS)


def at(word_idx):
    """Edited-timeline time of a kept word."""
    off = 0.0
    for (s, e, *_), (a, b, *_) in zip(segs_t, SEGS):
        if a <= word_idx <= b:
            return off + words[word_idx][0] - s
        off += e - s
    raise ValueError(word_idx)


tags = [
    (at(43), at(82), "*NO SLEEP*", "cyan"),
    (at(109), at(123), "*ZERO SELF CONTROL*", "red"),
]
overlay = ck.build_overlay(WS / "artifacts/clip03_overlay.png",
                           "BRO REALLY CHANGED\nTIME ZONES FOR GTA 6",
                           "Source: @KaiCenatLive (YouTube / Twitch)",
                           chyron="8:00 AM • NEW ZEALAND SERVER", banner_y=150)
ass = ck.build_ass(WS / "artifacts/clip03.ass", cues, tags, cap_y=1200, tag_y=1320)
out = WS / "exports/clip03_new_zealand_FINAL.mp4"
T = ck.render_crop9x16(SRC, segs_t, overlay, ass, out, eye_frac=0.36,
                       sfx=[("whoosh", at(135) - 0.3)])
print(f"wrote {out} ({T:.2f}s)")
