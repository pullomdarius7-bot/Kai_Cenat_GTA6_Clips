"""YouTube channel banner for @viralclipppps (2560x1440, text kept inside YouTube's 1546x423 safe area).

Usage: python3 make_banner.py [avatar_image] [out.png]
Swap in the new laughing avatar later by passing its path -- everything else stays the same.
"""
import random
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = Path(__file__).parent
AVATAR = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "avatar_current.png"
OUT = Path(sys.argv[2]) if len(sys.argv) > 2 else HERE / "youtube_banner.png"
W, H = 2560, 1440
SAFE = (507, 508, 2053, 931)  # visible on every device (TV, desktop, phone)
RED, YEL, GRN = (226, 35, 42), (250, 200, 0), (22, 168, 72)
BLACK = "/usr/share/fonts/opentype/inter/InterDisplay-Black.otf"
XB = "/usr/share/fonts/opentype/inter/Inter-ExtraBold.otf"
random.seed(7)

img = Image.new("RGB", (W, H), (8, 8, 10))

# --- paint-splash band: the same red/yellow/green as the avatar ring, as one diagonal brush sweep
splash = Image.new("RGBA", (W, H), (0, 0, 0, 0))
d = ImageDraw.Draw(splash)
cy = (SAFE[1] + SAFE[3]) // 2
for i, col in enumerate((RED, YEL, GRN)):
    off = (i - 1) * 120
    for _ in range(900):  # rough brush texture
        x = random.uniform(-100, W + 100)
        y = cy + off + (x - W / 2) * -0.06 + random.gauss(0, 34)
        r = abs(random.gauss(26, 14))
        d.ellipse([x - r * 2.2, y - r, x + r * 2.2, y + r], fill=col + (random.randint(130, 230),))
    for _ in range(70):  # paint drips/specks
        x = random.uniform(0, W)
        y = cy + off + (x - W / 2) * -0.06 + random.gauss(0, 140)
        r = random.uniform(3, 11)
        d.ellipse([x - r, y - r, x + r, y + r], fill=col + (220,))
splash = splash.filter(ImageFilter.GaussianBlur(1.2))
# fade the band toward the safe-area text so the title stays readable
mask = Image.new("L", (W, H), 0)
md = ImageDraw.Draw(mask)
md.rectangle([0, 0, W, H], fill=150)
md.rounded_rectangle([SAFE[0] + 470, SAFE[1] + 30, SAFE[2] + 40, SAFE[3] - 30], radius=60, fill=55)
mask = mask.filter(ImageFilter.GaussianBlur(60))
a = splash.split()[3].point(lambda v: v)
splash.putalpha(Image.composite(a, Image.new("L", (W, H), 0), mask))
img.paste(splash, (0, 0), splash)

# --- avatar badge on the left of the safe area
D = 340
av = Image.open(AVATAR).convert("RGB").resize((D, D), Image.LANCZOS)
circ = Image.new("L", (D, D), 0)
ImageDraw.Draw(circ).ellipse([0, 0, D - 1, D - 1], fill=255)
bx, by = SAFE[0] + 60, cy - D // 2
ring = ImageDraw.Draw(img)
ring.ellipse([bx - 14, by - 14, bx + D + 14, by + D + 14], fill=(8, 8, 10))
ring.ellipse([bx - 10, by - 10, bx + D + 10, by + D + 10], outline=YEL, width=8)
img.paste(av, (bx, by), circ)

# --- title + tagline + platforms (all inside the safe area)
dr = ImageDraw.Draw(img)
tx = bx + D + 60
avail = SAFE[2] - 50 - tx  # keep 50px margin inside the phone-safe area
size = 150
while ImageDraw.Draw(img).textlength("VIRAL CLIPPPPS", font=ImageFont.truetype(BLACK, size)) > avail:
    size -= 2
title_f = ImageFont.truetype(BLACK, size)
dr.text((tx + 6, cy - size + 8), "VIRAL", font=title_f, fill=(0, 0, 0))
dr.text((tx, cy - size), "VIRAL", font=title_f, fill="white")
vw = dr.textlength("VIRAL ", font=title_f)
dr.text((tx + vw + 6, cy - size + 8), "CLIPPPPS", font=title_f, fill=(0, 0, 0))
dr.text((tx + vw, cy - size), "CLIPPPPS", font=title_f, fill=YEL)

tag_f = ImageFont.truetype(XB, 44)
dr.text((tx + 4, cy + 12), "The stream moments you missed.", font=tag_f, fill="white")

pill_f = ImageFont.truetype(XB, 30)
px = tx
for label, col in (("YouTube", RED), ("TikTok", GRN), ("Instagram", YEL)):
    w = dr.textlength(label, font=pill_f)
    dr.rounded_rectangle([px, cy + 88, px + w + 40, cy + 138], radius=25, fill=col)
    dr.text((px + 20 + w / 2, cy + 113), label, font=pill_f, fill="black" if col == YEL else "white", anchor="mm")
    px += w + 58
dr.text((px + 6, cy + 113), "@viralclipppps", font=pill_f, fill="white", anchor="lm")

img.save(OUT)
print("wrote", OUT)
