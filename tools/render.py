"""Draw the front page for the 19 November 2026 news entry (variant A).

Classic broadsheet: big serif masthead, one lead story, a three-column
grid of the day's stories, and a "day in brief" strip at the bottom.

Everything is drawn with Pillow primitives from the verified story list
in the parent brief. No photos, no network, no randomness, no timestamps,
so running this script twice produces the same PNG bytes.

Usage: python3 tools/render.py   (paths are script-relative)
Output: assets/entry.png, 1024x1024, under 1 MiB.
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets" / "entry.png"

FONT_DIR = Path("/usr/share/fonts/truetype/dejavu")
SERIF_BOLD = FONT_DIR / "DejaVuSerif-Bold.ttf"
SANS_BOLD = FONT_DIR / "DejaVuSans-Bold.ttf"
SANS = FONT_DIR / "DejaVuSans.ttf"

W, H = 1024, 1024
MARGIN = 36
PAPER = (248, 244, 233)
INK = (26, 26, 26)
GRAY = (96, 96, 90)
FAINT = (205, 200, 186)
NAVY = (27, 42, 74)
BRICK = (178, 44, 32)


def load(path: Path, size: int) -> ImageFont.FreeTypeFont:
    if not path.exists():
        raise SystemExit(f"missing font file: {path}")
    return ImageFont.truetype(str(path), size)


def wrap_text(d: ImageDraw.ImageDraw, text: str,
              fnt: ImageFont.FreeTypeFont, width: int) -> list[str]:
    """Greedy word wrap measured with the real font; words never split."""
    lines: list[str] = []
    current = ""
    for word in text.split():
        trial = f"{current} {word}".strip()
        if d.textlength(trial, font=fnt) <= width or not current:
            current = trial
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def draw_wrapped(d: ImageDraw.ImageDraw, x: int, y: int, text: str,
                 fnt: ImageFont.FreeTypeFont, width: int,
                 fill: tuple[int, int, int], gap: int = 3,
                 limit: int = 3) -> int:
    """Draw wrapped text, return the y just below the last line."""
    for line in wrap_text(d, text, fnt, width)[:limit]:
        d.text((x, y), line, font=fnt, fill=fill)
        y += fnt.size + gap
    return y


def centred(d: ImageDraw.ImageDraw, cx: int, y: int, text: str,
            fnt: ImageFont.FreeTypeFont,
            fill: tuple[int, int, int]) -> None:
    d.text((cx - d.textlength(text, font=fnt) / 2, y), text,
           font=fnt, fill=fill)


# ---- small line icons (36x36 box, stroke 3) -------------------------------

def icon_rings(d: ImageDraw.ImageDraw, x: int, y: int, s: int,
               c: tuple[int, int, int]) -> None:
    """Three interlocking rings: three leaders at one table."""
    r = s // 3
    d.ellipse([x, y + r // 2, x + 2 * r, y + 2 * r + r // 2],
              outline=c, width=4)
    d.ellipse([x + r, y, x + 3 * r, y + 2 * r], outline=c, width=4)
    d.ellipse([x + 2 * r, y + r // 2, x + 4 * r, y + 2 * r + r // 2],
              outline=c, width=4)


def icon_burst(d: ImageDraw.ImageDraw, x: int, y: int, s: int,
               c: tuple[int, int, int]) -> None:
    cx, cy = x + s // 2, y + s // 3
    for ang in range(0, 360, 45):
        import math
        dx = int(13 * math.cos(math.radians(ang)))
        dy = int(13 * math.sin(math.radians(ang)))
        d.line([(cx, cy), (cx + dx, cy + dy)], fill=c, width=3)
    d.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=c)
    for yy in (y + s - 10, y + s - 4):
        d.line([(x + 2, yy), (x + s - 2, yy)], fill=c, width=2)


def icon_bridge(d: ImageDraw.ImageDraw, x: int, y: int, s: int,
                c: tuple[int, int, int]) -> None:
    d.line([(x + 2, y + s - 8), (x + s - 2, y + s - 8)], fill=c, width=3)
    d.arc([x + 4, y + 6, x + s - 4, y + s + 6], start=180, end=360,
          fill=c, width=3)
    for px in (x + 10, x + s // 2, x + s - 12):
        d.line([(px, y + s - 8), (px, y + s - 18)], fill=c, width=3)


def icon_chip(d: ImageDraw.ImageDraw, x: int, y: int, s: int,
              c: tuple[int, int, int]) -> None:
    d.rectangle([x + 8, y + 8, x + s - 8, y + s - 8], outline=c, width=3)
    d.rectangle([x + 14, y + 14, x + s - 14, y + s - 14],
                outline=c, width=2)
    for t in (x + 13, x + s // 2, x + s - 15):
        d.line([(t, y + 2), (t, y + 8)], fill=c, width=2)
        d.line([(t, y + s - 8), (t, y + s - 2)], fill=c, width=2)
        d.line([(x + 2, t), (x + 8, t)], fill=c, width=2)
        d.line([(x + s - 8, t), (x + s - 2, t)], fill=c, width=2)


def icon_flood(d: ImageDraw.ImageDraw, x: int, y: int, s: int,
               c: tuple[int, int, int]) -> None:
    d.ellipse([x + 4, y + 4, x + 20, y + 18], outline=c, width=3)
    d.ellipse([x + 14, y + 2, x + 32, y + 18], outline=c, width=3)
    d.line([(x + 4, y + 16), (x + 32, y + 16)], fill=c, width=3)
    for dx in (8, 16, 24):
        d.line([(x + dx, y + 22), (x + dx - 2, y + 27)], fill=c, width=2)
    d.arc([x + 2, y + s - 10, x + s - 2, y + s + 2], start=180, end=360,
          fill=c, width=2)


def icon_ballot(d: ImageDraw.ImageDraw, x: int, y: int, s: int,
                c: tuple[int, int, int]) -> None:
    d.rectangle([x + 6, y + 16, x + s - 6, y + s - 4], outline=c, width=3)
    d.line([(x + 13, y + 16), (x + s - 13, y + 16)], fill=PAPER, width=3)
    d.rectangle([x + 13, y + 4, x + s - 13, y + 16], outline=c, width=2)
    d.line([(x + 12, y + 26), (x + 17, y + 30)], fill=c, width=2)
    d.line([(x + 17, y + 30), (x + 26, y + 21)], fill=c, width=2)


def icon_scales(d: ImageDraw.ImageDraw, x: int, y: int, s: int,
                c: tuple[int, int, int]) -> None:
    cx = x + s // 2
    d.line([(cx, y + 4), (cx, y + s - 6)], fill=c, width=3)
    d.line([(x + 4, y + 10), (x + s - 4, y + 10)], fill=c, width=3)
    for px in (x + 6, x + s - 8):
        d.line([(px, y + 10), (px + 6, y + 10)], fill=c, width=2)
        d.polygon([(px - 3, y + 12), (px + 9, y + 12), (px + 3, y + 20)],
                  outline=c)
    d.line([(x + 8, y + s - 6), (x + s - 8, y + s - 6)], fill=c, width=3)


def icon_globe(d: ImageDraw.ImageDraw, x: int, y: int, s: int,
               c: tuple[int, int, int]) -> None:
    cx, cy = x + s // 2, y + s // 2
    d.ellipse([x + 3, y + 3, x + s - 3, y + s - 3], outline=c, width=3)
    d.ellipse([cx - 7, y + 3, cx + 7, y + s - 3], outline=c, width=2)
    d.line([(x + 3, cy), (x + s - 3, cy)], fill=c, width=2)
    d.arc([x + 6, y + 8, x + s - 6, y + s - 8], start=300, end=60,
          fill=c, width=2)


def icon_satellite(d: ImageDraw.ImageDraw, x: int, y: int, s: int,
                   c: tuple[int, int, int]) -> None:
    d.arc([x + 2, y + 2, x + s - 2, y + s - 2], start=200, end=340,
          fill=c, width=2)
    d.ellipse([x + s // 2 - 5, y + s // 2 - 5, x + s // 2 + 5,
               y + s // 2 + 5], fill=c)
    d.rectangle([x + 4, y + s // 2 - 3, x + 12, y + s // 2 + 3],
                outline=c, width=2)
    d.rectangle([x + s - 12, y + s // 2 - 3, x + s - 4,
                 y + s // 2 + 3], outline=c, width=2)
    d.ellipse([x + s - 8, y + 2, x + s - 3, y + 7], fill=c)


def icon_peaks(d: ImageDraw.ImageDraw, x: int, y: int, s: int,
               c: tuple[int, int, int]) -> None:
    d.polygon([(x + 2, y + s - 6), (x + 12, y + 8), (x + 22, y + s - 6)],
              outline=c)
    d.polygon([(x + 14, y + s - 6), (x + 26, y + 4), (x + s - 2, y + s - 6)],
              outline=c)
    for yy in range(y + 8, y + s - 4, 6):
        d.line([(x + s // 2, yy), (x + s // 2, yy + 3)], fill=c, width=2)


# ---- the page --------------------------------------------------------------

# (kicker, colour, headline, summary, icon)
STORIES = [
    ("GULF STRIKES", BRICK,
     "Iran hits U.S. bases; U.S. strikes Qeshm",
     "Iran fired at U.S. bases in Kuwait and Bahrain; U.S. hit Qeshm site.",
     icon_burst),
    ("UKRAINE WAR", BRICK,
     "Kerch Bridge hit for a third time this week",
     "Ukraine struck the Crimean Bridge again, days after the last strike.",
     icon_bridge),
    ("MARKETS", NAVY,
     "Anthropic debuts after record $81.3bn IPO",
     "Nasdaq debut under ANT at $83; valuation about $1.5 trillion.",
     icon_chip),
    ("GAZA", BRICK,
     "West presses Israel to let aid reach flooded Gaza",
     "Australia, Canada, Italy, UK: let aid in; rain displaced 46,000+ homes.",
     icon_flood),
    ("ISRAEL", NAVY,
     "Herzog asks Eisenkot to form a government",
     "Bypassing Netanyahu; Knesset elects Kahana speaker, 66 votes.",
     icon_ballot),
    ("THE HAGUE", NAVY,
     "World court to rule on Myanmar genocide case",
     "The ICJ is to rule on claims against Myanmar over the Rohingya.",
     icon_scales),
    ("TRADE", NAVY,
     "EU approves Indonesia trade deal",
     "EU governments back a pact to cut tariffs and offset U.S. tariff "
     "pressure.",
     icon_globe),
    ("SPACE", NAVY,
     "Voyager 1 reaches a light-day from Earth",
     "NASA's probe is believed to have passed the distance milestone.",
     icon_satellite),
    ("HORN OF AFRICA", BRICK,
     "Ethiopia, Eritrea mass troops at border",
     "Forces gathered near Badme; reports of clashes are unconfirmed.",
     icon_peaks),
]

BRIEF = [
    "IAEA: North Korea expands uranium enrichment at Yongbyon",
    "Bangladesh garment workers protest into a third week",
    "GTA 6 built with help of 1,600 developers in Bengaluru",
    "Gaza floods damage 40,000+ family shelters",
]


def main() -> None:
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    f_mast = load(SERIF_BOLD, 62)
    f_date = load(SERIF_BOLD, 24)
    f_side = load(SANS_BOLD, 17)
    f_kick = load(SANS_BOLD, 19)
    f_kick_s = load(SANS_BOLD, 14)
    f_lead = load(SERIF_BOLD, 40)
    f_lead_sum = load(SANS, 21)
    f_head = load(SERIF_BOLD, 21)
    f_sum = load(SANS, 16)
    f_brief_h = load(SANS_BOLD, 17)
    f_brief = load(SANS, 17)
    f_foot = load(SANS, 14)

    # Masthead
    centred(d, W // 2, 22, "THE WORLD TODAY", f_mast, INK)
    d.text((MARGIN, 100), "ALL THE WORLD'S NEWS", font=f_side, fill=INK)
    right = "ONE PAGE \u00b7 ONE DAY"
    d.text((W - MARGIN - d.textlength(right, font=f_side), 100), right,
           font=f_side, fill=INK)
    centred(d, W // 2, 96, "THURSDAY, 19 NOVEMBER 2026", f_date, BRICK)
    d.line([(MARGIN, 134), (W - MARGIN, 134)], fill=INK, width=4)
    d.line([(MARGIN, 142), (W - MARGIN, 142)], fill=INK, width=1)

    # Lead story: Shenzhen summit
    d.text((52, 160), "SHENZHEN SUMMIT \u2014 DIPLOMACY", font=f_kick,
           fill=BRICK)
    y = draw_wrapped(d, 52, 190,
                     "Trump, Xi and Putin meet in first three-way summit",
                     f_lead, 600, INK, gap=2, limit=2)
    draw_wrapped(d, 52, y + 10,
                 "The three leaders held their first three-way summit in "
                 "Shenzhen, on the APEC sidelines, with nuclear arms, "
                 "Ukraine and the Iran conflict on the agenda.",
                 f_lead_sum, 600, INK, gap=4, limit=3)
    icon_rings(d, 700, 180, 180, NAVY)
    centred(d, 790, 356, "SHENZHEN, CHINA", f_side, GRAY)
    d.line([(MARGIN, 412), (W - MARGIN, 412)], fill=INK, width=2)

    # Story grid: 3 columns x 3 rows
    cols = [MARGIN, 364, 692]
    rows = [428, 568, 708]
    for i, (kick, colour, head, summ, icon) in enumerate(STORIES):
        cx = cols[i % 3]
        cy = rows[i // 3]
        icon(d, cx, cy, 36, colour)
        d.text((cx + 44, cy + 9), kick, font=f_kick_s, fill=colour)
        y = draw_wrapped(d, cx, cy + 42, head, f_head, 296, INK,
                         gap=1, limit=2)
        draw_wrapped(d, cx, y + 3, summ, f_sum, 296, GRAY, gap=1, limit=2)
        if i // 3 < 2:
            d.line([(cx, cy + 134), (cx + 296, cy + 134)], fill=FAINT,
                   width=1)
    for vx in (348, 676):
        d.line([(vx, 428), (vx, 844)], fill=FAINT, width=1)
    d.line([(MARGIN, 856), (W - MARGIN, 856)], fill=INK, width=2)

    # The day in brief
    d.text((MARGIN, 868), "THE DAY IN BRIEF", font=f_brief_h, fill=BRICK)
    by = 894
    for item in BRIEF:
        d.text((MARGIN, by), "\u2022  " + item, font=f_brief, fill=INK)
        by += 22
    d.line([(MARGIN, 988), (W - MARGIN, 988)], fill=INK, width=1)
    centred(d, W // 2, 998, "DRAWN FROM REPORTS PUBLISHED 19 NOVEMBER 2026",
            f_foot, GRAY)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    img.save(OUT, format="PNG", optimize=True)
    print(f"wrote {OUT} ({OUT.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
