#!/usr/bin/env python3
"""Draw THE WORLD TODAY — Monday 23 November 2026 — as a single 1024x1024
front page, then save it as entry.png next to this script.

Every story on the page was reported on 23 November 2026 (or is flagged in
the DATE CHECK footer when its event falls on another day). Sources are
named story by story in STORIES.md. Run:  python3 draw23.py
"""
import math
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 1024, 1024

PAPER = (247, 243, 232)
INK = (26, 26, 26)
INK_SOFT = (74, 74, 74)
RED = (179, 39, 30)
RED_DK = (140, 28, 22)
BLUE = (31, 78, 121)
BLUE_LT = (220, 233, 242)
GOLD = (201, 162, 39)
GREEN = (46, 125, 50)
LAND = (232, 224, 200)
LAND_LN = (185, 174, 142)
SEA = (214, 230, 240)
CARD = (255, 255, 255)
CARD_EDGE = (203, 196, 178)

_FONT_DIRS = [
    "/usr/share/fonts/truetype/dejavu",
    "/usr/share/fonts/truetype/liberation",
    "/usr/share/fonts/TTF",
]


def _find_font(bold, serif):
    names = []
    if serif:
        names = ["DejaVuSerif-Bold.ttf", "DejaVuSerif.ttf",
                 "LiberationSerif-Bold.ttf", "LiberationSerif-Regular.ttf"]
    elif bold:
        names = ["DejaVuSans-Bold.ttf", "LiberationSans-Bold.ttf"]
    else:
        names = ["DejaVuSans.ttf", "LiberationSans-Regular.ttf"]
    for d in _FONT_DIRS:
        for n in names:
            p = os.path.join(d, n)
            if os.path.exists(p):
                return p
    return None


_FONTS = {}


def F(size, bold=False, serif=False):
    key = (size, bold, serif)
    if key not in _FONTS:
        path = _find_font(bold, serif)
        if path:
            _FONTS[key] = ImageFont.truetype(path, size)
        else:
            _FONTS[key] = ImageFont.load_default()
    return _FONTS[key]


def tw(draw, text, font):
    """Text width in pixels."""
    b = draw.textbbox((0, 0), text, font=font)
    return b[2] - b[0]


def th(font):
    a, d = font.getmetrics()
    return a + d


def wrap(draw, text, font, width):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if tw(draw, trial, font) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def para(draw, x, y, text, font, width, fill=INK, leading=None, align="left"):
    lines = wrap(draw, text, font, width)
    lh = leading or int(th(font) * 1.18)
    for ln in lines:
        if align == "center":
            draw.text((x + (width - tw(draw, ln, font)) // 2, y), ln,
                      font=font, fill=fill)
        else:
            draw.text((x, y), ln, font=font, fill=fill)
        y += lh
    return y


def card(draw, x, y, w, h, fill=CARD, edge=CARD_EDGE, lw=1):
    draw.rounded_rectangle([x, y, x + w, y + h], radius=6,
                           fill=fill, outline=edge, width=lw)


def hline(draw, x, y, w, color=INK, lw=1):
    draw.line([(x, y), (x + w, y)], fill=color, width=lw)


def num_badge(draw, x, y, n, d=20):
    draw.ellipse([x, y, x + d, y + d], fill=RED, outline=(255, 255, 255),
                 width=2)
    t = str(n)
    f = F(11, bold=True)
    draw.text((x + (d - tw(draw, t, f)) // 2, y + (d - th(f)) // 2 + 1),
              t, font=f, fill=(255, 255, 255))


def flame(draw, cx, base, s):
    """A stylised flame, s = height in px."""
    outer = [(cx - 0.42 * s, base), (cx - 0.30 * s, base - 0.55 * s),
             (cx - 0.10 * s, base - 0.62 * s), (cx + 0.05 * s, base - s),
             (cx + 0.22 * s, base - 0.66 * s), (cx + 0.42 * s, base - 0.45 * s),
             (cx + 0.38 * s, base)]
    draw.polygon(outer, fill=(232, 90, 20))
    inner = [(cx - 0.22 * s, base), (cx - 0.14 * s, base - 0.38 * s),
             (cx, base - 0.55 * s), (cx + 0.16 * s, base - 0.30 * s),
             (cx + 0.20 * s, base)]
    draw.polygon(inner, fill=(245, 176, 20))
    core = [(cx - 0.10 * s, base), (cx - 0.05 * s, base - 0.22 * s),
            (cx + 0.08 * s, base - 0.26 * s), (cx + 0.10 * s, base)]
    draw.polygon(core, fill=(255, 236, 150))


def smoke(draw, x, y, r, color=(120, 120, 120)):
    draw.ellipse([x - r, y - r, x + r, y + r], fill=color)
    draw.ellipse([x - r * 0.6, y - r * 1.5, x + r * 0.7, y - r * 0.2],
                 fill=color)


def flag_id(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h // 2], fill=(210, 30, 30))
    draw.rectangle([x, y + h // 2, x + w, y + h], fill=(255, 255, 255))
    draw.rectangle([x, y, x + w, y + h], outline=INK, width=1)


def flag_us(draw, x, y, w, h):
    for i in range(7):
        draw.rectangle([x, y + i * h // 7, x + w, y + (i + 1) * h // 7],
                       fill=(178, 34, 52) if i % 2 == 0 else (255, 255, 255))
    draw.rectangle([x, y, x + w * 0.4, y + h * 4 // 7], fill=(60, 59, 110))
    draw.rectangle([x, y, x + w, y + h], outline=INK, width=1)


def flag_cn(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(222, 41, 16))
    draw.rectangle([x, y, x + w, y + h], outline=INK, width=1)
    cx, cy, r = x + w * 0.22, y + h * 0.28, h * 0.16
    pts = []
    for k in range(10):
        ang = -math.pi / 2 + k * math.pi / 5
        rr = r if k % 2 == 0 else r * 0.45
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    draw.polygon(pts, fill=(255, 222, 0))


def flag_ru(draw, x, y, w, h):
    for i, c in enumerate([(255, 255, 255), (0, 57, 166), (213, 0, 50)]):
        draw.rectangle([x, y + i * h // 3, x + w, y + (i + 1) * h // 3],
                       fill=c)
    draw.rectangle([x, y, x + w, y + h], outline=INK, width=1)


def globe(draw, cx, cy, r):
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(125, 180, 210),
                 outline=BLUE, width=2)
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(255, 255, 255),
                 width=1)
    for k in range(-2, 3):
        x0 = cx + k * r // 3
        draw.arc([cx - r, cy - r, cx + r, cy + r], -60, 60, fill=BLUE)
    draw.line([cx - r, cy, cx + r, cy], fill=BLUE, width=1)
    draw.ellipse([cx - r, cy - int(r * 0.45), cx + r, cy + int(r * 0.45)],
                 outline=BLUE, width=1)
    draw.polygon([(cx - r * 0.55, cy - r * 0.15), (cx - r * 0.1, cy - r * 0.5),
                  (cx + r * 0.3, cy - r * 0.3), (cx + r * 0.15, cy + r * 0.1),
                  (cx - r * 0.3, cy + r * 0.25)], fill=(96, 160, 90))
    draw.polygon([(cx + r * 0.35, cy + r * 0.35), (cx + r * 0.7, cy + r * 0.2),
                  (cx + r * 0.55, cy + r * 0.65), (cx + r * 0.2, cy + r * 0.6)],
                 fill=(96, 160, 90))


# ---------------------------------------------------------------- stories
# (region, kicker, headline, body, source, kind)
FEATURES = [
    ("ASIA", "BANTEN, INDONESIA",
     "24 KILLED IN CANDY FACTORY FIRE",
     "Rescuers pick through the burned ruins of the PT Fonusa Agung Mulia "
     "sweets plant for about 30 workers still missing. The toll was "
     "confirmed on Monday; DNA is needed to name the dead.",
     "Reuters", "fire"),
    ("MIDDLE EAST", "STRAIT OF HORMUZ",
     "MINES SET THREE TANKERS ABLAZE",
     "Iran's Revolutionary Guard says its mines hit three oil tankers in "
     "the strait, as a US naval blockade of Iranian oil enters its 130th "
     "day and shipping fears climb.",
     "Al Jazeera", "tanker"),
    ("GLOBAL", "ANTALYA, TURKIYE",
     "CLIMATE TALKS END WITH NO DEAL",
     "COP31 collapses after record-long talks: 190+ nations split over "
     "fossil fuels and adaptation finance, the first total COP failure "
     "since 2009.",
     "Reuters", "cop"),
]

SMALL = [
    ("AMERICAS", "SANTA CLARA", "HUANG IS BACK AT NVIDIA",
     "Board reinstates its CEO weeks after he quit in a spy row; Washington "
     "is said to be 'shocked'.", "AP", "chip"),
    ("AFRICA", "BENGHAZI, LIBYA", "UKRAINE SINKS RUSSIAN SHIP",
     "Naval drones strike a vessel in port; Kyiv claims the hit, Moscow "
     "warns of escalation.", "Reuters", "drone"),
    ("ASIA", "BEIJING", "TRUMP, XI AND PUTIN MEET",
     "Three-way summit in China yields little as Xi presses on Taiwan.",
     "Standard Topic", "summit"),
    ("ASIA", "NEW DELHI", "NEPAL GETS $1.62BN AID",
     "Flood-rebuilding package agreed after Modi talks with Nepal's PM.",
     "Reuters", "aid"),
    ("EUROPE", "BRUSSELS", "FLIGHTS GROUNDED BY STRIKE",
     "Austerity protest halts planes across Belgium for the day.",
     "BBC", "plane"),
    ("GLOBAL", "MERCURY", "PROBE REACHES MERCURY",
     "BepiColombo enters orbit after an 8-year cruise — but a thruster "
     "glitch cut its burn short.", "Gizmodo", "space"),
    ("GLOBAL", "MATHS", "DID AI PROVE RIEMANN?",
     "Anthropic's claim of an AI-assisted proof sparks a verification race.",
     "Nature", "maths"),
    ("GLOBAL", "MARKETS", "BITCOIN BOUNCES TO $61K",
     "Rebound from a two-year low as Wall Street futures recover.",
     "CoinDesk", "coin"),
    ("AMERICAS", "NEW YORK", "METS LAND SKUBAL IN RECORD DEAL",
     "Detroit ace agrees the richest pitcher deal in baseball.",
     "Standard Topic", "sport"),
    ("AMERICAS", "HOLLYWOOD", "'SUNRISE' OPENS WITH $120M",
     "Hunger Games prequel tops the box office; Miley Cyrus weds.",
     "Standard Topic", "film"),
]

BRIEFS = [
    ("ASIA", "SEOUL", "Education minister quits over exam-cheating chaos.", "Reuters"),
    ("EUROPE", "LONDON", "Burnham's EU deal reopens the Brexit debate.", "The Guardian"),
    ("ASIA", "ISLAMABAD", "Pakistan PM cancels Russia trip amid clashes.", "The Hindu"),
    ("AMERICAS", "WASHINGTON", "Trump orders contractors to check with the White House first.", "AP"),
    ("AMERICAS", "WASHINGTON", "Court lets Trump try again to move hush-money case.", "AP"),
    ("AMERICAS", "SEATTLE", "Masked ICE agents pull a father and daughter off a jet.", "CBS"),
    ("MIDDLE EAST", "GAZA", "Oxfam: attacks turned Gaza into a 'toxic wasteland'.", "Oxfam"),
    ("EUROPE", "PARIS", "Global wealth-tax campaign gathers momentum.", "10 Things"),
    ("EUROPE", "WARSAW", "Poland accuses Russia of provocation over missiles.", "10 Things"),
    ("MIDDLE EAST", "JERUSALEM", "Israeli coalition talks stall over leadership.", "10 Things"),
    ("ASIA", "JAKARTA", "EU and Indonesia sign a deal scrapping most tariffs.", "AP"),
    ("ASIA", "BEIJING", "China, South Korea, Taiwan step in to prop up stocks.", "Standard Topic"),
    ("ASIA", "NEW DELHI", "World Bank: India's extreme poverty fell to 2.6%.", "Standard Topic"),
    ("EUROPE", "LONDON", "NHS starts an AI trial in breast-cancer screening.", "Principia"),
    ("AMERICAS", "NEW YORK", "Anthropic shares slide 3% after IPO as AI sell-off grows.", "Standard Topic"),
    ("AMERICAS", "WASHINGTON", "FBI probes a possible hack of its crime database.", "Principia"),
    ("EUROPE", "LONDON", "Signal limits mobile screenshots, citing AI surveillance.", "Morning Brief"),
    ("AFRICA", "ABUJA", "Nigeria's presidential villa hit by water and power cuts.", "BBC"),
    ("AMERICAS", "MEXICO CITY", "Mexico and China agree a trade working group.", "Standard Topic"),
    ("OCEANIA", "CANBERRA", "Georgie Prespakis wins the AFLW best and fairest.", "ABC"),
]

NUMBERS = [
    ("24", "DEAD · ~30 MISSING", "BANTEN FACTORY FIRE"),
    ("3", "TANKERS ABLAZE", "STRAIT OF HORMUZ"),
    ("$1.62BN", "FLOOD AID", "INDIA TO NEPAL"),
    ("190+", "NATIONS, NO DEAL", "COP31 COLLAPSE"),
    ("$61K", "BITCOIN REBOUND", "FROM 2-YEAR LOW"),
]

# lon, lat of the 13 drawn stories, for the map
DOTS = [
    (106.0, -6.2), (56.5, 26.5), (30.7, 36.9), (-122.0, 37.4),
    (20.1, 32.1), (116.4, 39.9), (77.2, 28.6), (4.4, 50.8),
    (8.7, 49.9), (-0.1, 51.5), (-74.0, 40.7), (-83.0, 42.3),
    (-114.0, 33.0),
]

CONTINENTS = {
    "NA": [(-168, 66), (-140, 70), (-120, 72), (-95, 80), (-80, 73),
           (-60, 62), (-55, 52), (-70, 44), (-75, 35), (-80, 26),
           (-85, 20), (-90, 15), (-95, 17), (-105, 20), (-115, 28),
           (-125, 40), (-125, 49), (-140, 60), (-165, 60)],
    "SA": [(-80, 10), (-75, 5), (-60, 5), (-50, 0), (-35, -8),
           (-40, -20), (-48, -28), (-55, -35), (-65, -45), (-70, -52),
           (-73, -40), (-72, -20), (-77, -12), (-80, -5)],
    "AF": [(-17, 15), (-10, 30), (0, 36), (10, 37), (20, 32), (32, 31),
           (35, 28), (43, 12), (51, 11), (48, 0), (40, -15), (35, -25),
           (28, -33), (18, -35), (12, -18), (9, 0), (9, 4), (-8, 5),
           (-15, 10)],
    "EU": [(-10, 36), (-9, 43), (-2, 48), (0, 50), (5, 53), (8, 57),
           (10, 59), (18, 56), (21, 55), (24, 58), (28, 60), (30, 70),
           (40, 68), (45, 68), (40, 60), (35, 55), (30, 50), (28, 45),
           (23, 40), (19, 42), (12, 44), (8, 44), (3, 42), (0, 39),
           (-2, 37), (-9, 37)],
    "AS": [(30, 70), (45, 68), (60, 69), (75, 73), (90, 75), (110, 76),
           (130, 72), (150, 70), (170, 66), (178, 65), (170, 60),
           (160, 55), (158, 50), (142, 45), (140, 40), (130, 35),
           (127, 35), (122, 30), (120, 25), (110, 20), (105, 10),
           (100, 8), (97, 15), (92, 20), (88, 22), (80, 15), (76, 8),
           (72, 20), (66, 25), (60, 25), (55, 26), (50, 29), (48, 30),
           (43, 35), (40, 38), (35, 40), (30, 42), (28, 45)],
    "OC": [(113, -22), (114, -30), (115, -35), (124, -33), (130, -32),
           (137, -35), (140, -38), (145, -38), (150, -37), (153, -32),
           (153, -27), (146, -19), (142, -11), (136, -12), (132, -11),
           (126, -14), (122, -17), (118, -20)],
}

# ---------------------------------------------------------------- pictures

def illo_fire(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(52, 44, 40))
    draw.rectangle([x + 8, y + h - 46, x + w - 8, y + h - 8],
                   fill=(120, 116, 110))
    draw.rectangle([x + 8, y + h - 46, x + w - 8, y + h - 38],
                   fill=(70, 66, 60))
    for wx in (x + 26, x + w // 2 - 10, x + w - 46):
        draw.rectangle([wx, y + h - 34, wx + 20, y + h - 14],
                       fill=(245, 200, 90))
        draw.line([(wx + 10, y + h - 34), (wx + 10, y + h - 14)],
                  fill=INK, width=1)
    draw.polygon([(x + w * 0.2, y + h - 46), (x + w * 0.5, y + 8),
                  (x + w * 0.8, y + h - 46)], fill=(90, 84, 78))
    smoke(draw, x + w * 0.3, y + 16, 10)
    smoke(draw, x + w * 0.62, y + 10, 12)
    flame(draw, x + w * 0.30, y + h - 40, 34)
    flame(draw, x + w * 0.55, y + h - 40, 44)
    flame(draw, x + w * 0.78, y + h - 40, 30)
    flag_id(draw, x + w - 44, y + 8, 34, 20)


def illo_tanker(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(28, 68, 110))
    draw.rectangle([x, y + h - 26, x + w, y + h], fill=(18, 52, 88))
    for i in range(5):
        wx = x + 12 + i * 34
        draw.arc([wx, y + h - 30, wx + 26, y + h - 12], 0, 180,
                 fill=(220, 235, 245), width=2)
    draw.polygon([(x + 16, y + h - 34), (x + w - 16, y + h - 34),
                  (x + w - 30, y + h - 62), (x + 30, y + h - 62)],
                 fill=(150, 40, 30))
    draw.rectangle([x + w // 2 - 14, y + h - 84, x + w // 2 + 26,
                    y + h - 62], fill=(235, 235, 235))
    draw.line([(x + w // 2 + 6, y + h - 84), (x + w // 2 + 6, y + h - 98)],
              fill=INK, width=2)
    for mx, my in ((x + 34, y + 26), (x + w - 40, y + 34), (x + w // 2, y + 16)):
        draw.ellipse([mx - 7, my - 7, mx + 7, my + 7], fill=(40, 40, 40),
                     outline=(200, 200, 200), width=1)
        draw.ellipse([mx - 2, my - 2, mx + 2, my + 2], fill=(200, 200, 200))
    flame(draw, x + w * 0.30, y + h - 62, 30)
    flame(draw, x + w * 0.72, y + h - 62, 38)


def illo_cop(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(214, 232, 222))
    globe(draw, x + w // 2, y + h // 2 + 2, 46)
    draw.ellipse([x + w // 2 - 46, y + h // 2 - 46, x + w // 2 + 46,
                  y + h // 2 + 48], outline=RED, width=3)
    draw.line([(x + w // 2 - 34, y + h // 2 - 52),
               (x + w // 2 + 34, y + h // 2 + 54)], fill=RED, width=4)
    f = F(15, bold=True)
    t = "NO DEAL"
    draw.rectangle([x + 8, y + h - 30, x + 8 + tw(draw, t, f) + 16, y + h - 8],
                   fill=RED)
    draw.text((x + 16, y + h - 27), t, font=f, fill=(255, 255, 255))
    f2 = F(11, bold=True)
    t2 = "190+ NATIONS"
    draw.text((x + w - tw(draw, t2, f2) - 8, y + 8), t2, font=f2, fill=RED_DK)


def illo_chip(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(24, 32, 48))
    cx, cy = x + w // 2, y + h // 2
    for dx in (-26, 0, 26):
        draw.line([(cx + dx, y + 8), (cx + dx, cy - 20)], fill=(180, 200, 220),
                  width=2)
        draw.line([(cx + dx, cy + 20), (cx + dx, y + h - 8)],
                  fill=(180, 200, 220), width=2)
    for dy in (-18, 0, 18):
        draw.line([(x + 8, cy + dy), (cx - 22, cy + dy)],
                  fill=(180, 200, 220), width=2)
        draw.line([(cx + 22, cy + dy), (x + w - 8, cy + dy)],
                  fill=(180, 200, 220), width=2)
    draw.rectangle([cx - 22, cy - 20, cx + 22, cy + 20], fill=(60, 90, 130),
                   outline=(160, 200, 230), width=2)
    f = F(13, bold=True)
    t = "AI"
    draw.text((cx - tw(draw, t, f) // 2, cy - 9), t, font=f,
              fill=(255, 255, 255))


def illo_drone(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(30, 70, 110))
    for i in range(4):
        wx = x + 14 + i * 30
        draw.arc([wx, y + h - 26, wx + 22, y + h - 10], 0, 180,
                 fill=(220, 235, 245), width=2)
    draw.polygon([(x + 10, y + h - 30), (x + w - 10, y + h - 30),
                  (x + w - 26, y + h - 58), (x + 26, y + h - 58)],
                 fill=(90, 90, 95))
    draw.rectangle([x + w // 2 - 16, y + h - 76, x + w // 2 + 16,
                    y + h - 58], fill=(200, 200, 205))
    cx, cy = x + w - 34, y + 30
    draw.line([(cx - 14, cy), (cx + 14, cy)], fill=(60, 60, 60), width=3)
    draw.line([(cx, cy - 12), (cx, cy + 12)], fill=(60, 60, 60), width=3)
    draw.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=(220, 60, 40),
                 outline=INK, width=1)
    draw.line([(cx, cy + 6), (x + w // 2 + 20, y + h - 70)],
              fill=(220, 60, 40), width=1)
    draw.ellipse([cx - 14, cy - 3, cx - 4, cy + 3], fill=(200, 200, 200))
    draw.ellipse([cx + 4, cy - 3, cx + 14, cy + 3], fill=(200, 200, 200))


def illo_summit(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(238, 232, 214))
    fw, fh = 52, 30
    flag_us(draw, x + 10, y + 14, fw, fh)
    flag_cn(draw, x + w // 2 - fw // 2, y + 8, fw, fh)
    flag_ru(draw, x + w - 10 - fw, y + 14, fw, fh)
    cy = y + h - 26
    for cx, c in ((x + 36, (60, 59, 110)), (x + w // 2, (222, 41, 16)),
                  (x + w - 36, (0, 57, 166))):
        draw.ellipse([cx - 13, cy - 13, cx + 13, cy + 13], fill=(240, 220, 180),
                     outline=c, width=2)
        draw.ellipse([cx - 5, cy - 8, cx + 5, cy + 2], fill=c)
    draw.line([(x + 36, cy + 13), (x + w // 2, cy + 13)], fill=INK, width=1)
    draw.line([(x + w // 2, cy + 13), (x + w - 36, cy + 13)], fill=INK, width=1)


def illo_aid(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(222, 236, 222))
    draw.polygon([(x + 8, y + h - 30), (x + w // 2, y + 18),
                  (x + w - 8, y + h - 30)], fill=(120, 160, 110))
    draw.rectangle([x + 8, y + h - 30, x + w - 8, y + h - 22],
                   fill=(90, 120, 90))
    for i in range(4):
        bx = x + 18 + i * 34
        draw.rectangle([bx, y + h - 52, bx + 18, y + h - 30],
                       fill=(200, 150, 90), outline=INK, width=1)
    f = F(15, bold=True)
    t = "$1.62BN"
    draw.text((x + (w - tw(draw, t, f)) // 2, y + 6), t, font=f, fill=GREEN)
    draw.polygon([(x + w // 2 - 30, y + h - 52), (x + w // 2, y + h - 66),
                  (x + w // 2 + 30, y + h - 52)], fill=(200, 60, 50))


def illo_plane(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(210, 226, 240))
    for i in range(3):
        draw.ellipse([x + 18 + i * 46, y + 12, x + 38 + i * 46, y + 24],
                     fill=(255, 255, 255))
    cx, cy = x + w // 2, y + h // 2 + 4
    draw.ellipse([cx - 52, cy - 10, cx + 52, cy + 10], fill=(240, 240, 240),
                 outline=INK, width=2)
    draw.polygon([(cx + 30, cy - 8), (cx + 58, cy - 26), (cx + 58, cy - 2)],
                 fill=(200, 200, 205), outline=INK)
    draw.polygon([(cx - 6, cy + 8), (cx + 10, cy + 26), (cx + 22, cy + 8)],
                 fill=(200, 200, 205), outline=INK)
    draw.polygon([(cx - 52, cy - 4), (cx - 66, cy - 14), (cx - 66, cy + 2)],
                 fill=(200, 200, 205), outline=INK)
    for wx in range(cx - 34, cx + 30, 12):
        draw.ellipse([wx, cy - 3, wx + 5, cy + 2], fill=BLUE)
    f = F(16, bold=True)
    t = "✕"
    draw.text((x + w - 26, y + 6), t, font=f, fill=RED)


def illo_space(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(16, 20, 38))
    for sx, sy in ((x + 14, y + 12), (x + 40, y + 26), (x + w - 20, y + 16),
                   (x + w - 44, y + 34), (x + 24, y + h - 18),
                   (x + w - 16, y + h - 26)):
        draw.ellipse([sx - 1, sy - 1, sx + 1, sy + 1], fill=(255, 255, 255))
    draw.ellipse([x + w - 66, y + 10, x + w - 10, y + 66],
                 fill=(200, 170, 140), outline=(150, 120, 95), width=1)
    for cx, cy, r in ((x + w - 50, y + 26, 5), (x + w - 30, y + 44, 7),
                      (x + w - 46, y + 52, 4)):
        draw.ellipse([cx - r, cy - r, cx + r, cy + r],
                     fill=(170, 140, 115))
    cx, cy = x + 52, y + h // 2 + 8
    draw.rectangle([cx - 22, cy - 12, cx + 22, cy + 12], fill=(220, 220, 225),
                   outline=INK, width=1)
    draw.polygon([(cx - 22, cy - 8), (cx - 36, cy - 2), (cx - 22, cy + 4)],
                 fill=(180, 180, 190))
    draw.rectangle([cx - 34, cy - 18, cx - 22, cy + 18], fill=(90, 140, 200))
    draw.rectangle([cx + 22, cy - 18, cx + 34, cy + 18], fill=(90, 140, 200))
    draw.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=(245, 176, 20))


def illo_maths(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(250, 246, 230))
    f = F(34, bold=True, serif=True)
    t = "ζ(s)"
    draw.text((x + 12, y + 8), t, font=f, fill=INK)
    f2 = F(12, bold=True)
    draw.text((x + 12, y + 52), "Re(s) = 1/2 ?", font=f2, fill=RED_DK)
    for i in range(5):
        draw.line([(x + w - 46, y + 14 + i * 12),
                   (x + w - 14, y + 20 + i * 12)], fill=BLUE, width=2)
    draw.text((x + w - 46, y + h - 22), "Q.E.D.?", font=F(11, bold=True),
              fill=BLUE)


def illo_coin(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(250, 242, 214))
    pts = [(x + 10, y + h - 22), (x + 34, y + h - 44), (x + 52, y + h - 34),
           (x + 74, y + h - 52), (x + 96, y + h - 40), (x + w - 12, y + 16)]
    draw.line(pts, fill=GREEN, width=3)
    draw.polygon(pts + [(x + w - 12, y + h - 12), (x + 10, y + h - 12)],
                 fill=(46, 125, 50, 40))
    cx, cy, r = x + w - 40, y + 30, 22
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(245, 176, 20),
                 outline=(180, 120, 0), width=2)
    f = F(20, bold=True)
    t = "₿"
    draw.text((cx - tw(draw, t, f) // 2, cy - 13), t, font=f, fill=(255, 255, 255))
    f2 = F(13, bold=True)
    draw.text((x + 10, y + 8), "$61K", font=f2, fill=GREEN)


def illo_sport(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(222, 238, 222))
    cx, cy, r = x + w // 2, y + h // 2 - 4, 26
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 255, 255),
                 outline=RED, width=2)
    draw.arc([cx - r + 4, cy - r + 4, cx + r - 4, cy + r - 4], -50, 50,
             fill=RED, width=2)
    draw.arc([cx - r + 4, cy - r + 4, cx + r - 4, cy + r - 4], 130, 230,
             fill=RED, width=2)
    draw.rectangle([x + 10, y + h - 30, x + w - 10, y + h - 12],
                   fill=(30, 60, 120))
    f = F(12, bold=True)
    t = "METS"
    draw.text((x + (w - tw(draw, t, f)) // 2, y + h - 28), t, font=f,
              fill=(255, 255, 255))


def illo_film(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(32, 26, 40))
    cx, cy = x + w // 2, y + h // 2 - 6
    draw.ellipse([cx - 30, cy - 30, cx + 30, cy + 30], fill=(60, 55, 70),
                 outline=(200, 200, 210), width=2)
    for k in range(6):
        ang = k * math.pi / 3
        hx, hy = cx + 18 * math.cos(ang), cy + 18 * math.sin(ang)
        draw.ellipse([hx - 5, hy - 5, hx + 5, hy + 5], fill=(240, 240, 245))
    draw.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=(240, 240, 245))
    for i, t in enumerate(("HUNGER", "GAMES")):
        f = F(13, bold=True)
        draw.text((x + (w - tw(draw, t, f)) // 2, y + h - 34 + i * 15), t,
                  font=f, fill=(245, 176, 20))


ILLOS = {"fire": illo_fire, "tanker": illo_tanker, "cop": illo_cop,
         "chip": illo_chip, "drone": illo_drone, "summit": illo_summit,
         "aid": illo_aid, "plane": illo_plane, "space": illo_space,
         "maths": illo_maths, "coin": illo_coin, "sport": illo_sport,
         "film": illo_film}

def illo_small(img, kind, x, y, w, h):
    """Draw an illustration designed for a 92px-tall box, scaled down to
    fit a small card, so nothing overflows the card's picture area."""
    tmp = Image.new("RGB", (w, 92), CARD)
    td = ImageDraw.Draw(tmp)
    ILLOS[kind](td, 0, 0, w, 92)
    img.paste(tmp.resize((w, h), Image.LANCZOS), (x, y))


# ---------------------------------------------------------------- the page

def region_counts():
    counts = {}
    for src in (FEATURES, SMALL, BRIEFS):
        for item in src:
            region = item[0] if len(item) >= 4 else None
            if region is None:
                continue
            counts[region] = counts.get(region, 0) + 1
    return counts


def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 20  # margin

    # ---- masthead
    hline(d, M, 10, W - 2 * M, INK, 3)
    title = "THE WORLD TODAY"
    f_title = F(46, bold=True, serif=True)
    d.text((M, 16), title, font=f_title, fill=INK)
    f_date = F(20, bold=True)
    date_t = "MONDAY 23 NOVEMBER 2026"
    d.text((W - M - tw(d, date_t, f_date), 22), date_t, font=f_date,
           fill=RED_DK)
    f_sub = F(13, bold=True)
    sub = "33 STORIES  ·  7 REGIONS  ·  ALL FROM THIS ONE DAY"
    d.text((M, 68), sub, font=f_sub, fill=INK_SOFT)
    f_sub2 = F(12)
    sub2 = "One day. One page. Every story checked against its source."
    d.text((W - M - tw(d, sub2, f_sub2), 68), sub2, font=f_sub2,
           fill=INK_SOFT)
    hline(d, M, 88, W - 2 * M, INK, 2)

    # ---- big-number strip
    y0 = 94
    cw = (W - 2 * M) // 5
    for i, (num, lab, sub2) in enumerate(NUMBERS):
        x = M + i * cw
        if i:
            d.line([(x - 4, y0 + 4), (x - 4, y0 + 40)], fill=CARD_EDGE,
                   width=1)
        f_num = F(26, bold=True, serif=True)
        d.text((x + 4, y0), num, font=f_num, fill=RED_DK)
        f_lab = F(11, bold=True)
        d.text((x + 4, y0 + 32), lab, font=f_lab, fill=INK)
        f_s2 = F(10)
        d.text((x + 4, y0 + 46), sub2, font=f_s2, fill=INK_SOFT)
    counts = region_counts()
    order = ["ASIA", "EUROPE", "MIDDLE EAST", "AMERICAS", "AFRICA",
             "OCEANIA", "GLOBAL"]
    rc = "   ".join("%s %d" % (r, counts.get(r, 0)) for r in order)
    f_rc = F(11, bold=True)
    d.text((M, y0 + 62), rc, font=f_rc, fill=BLUE)
    hline(d, M, 168, W - 2 * M, INK, 2)

    # ---- three big features
    y0 = 176
    fw = (W - 2 * M - 2 * 12) // 3
    fh = 252
    for i, (region, kicker, head, body, source, kind) in enumerate(FEATURES):
        x = M + i * (fw + 12)
        card(d, x, y0, fw, fh)
        num_badge(d, x + 8, y0 + 8, i + 1)
        f_k = F(11, bold=True)
        d.text((x + 34, y0 + 11), kicker, font=f_k, fill=RED_DK)
        ILLOS[kind](d, x + 8, y0 + 32, fw - 16, 92)
        f_h = F(17, bold=True, serif=True)
        yy = para(d, x + 10, y0 + 132, head, f_h, fw - 20, leading=20)
        f_b = F(11)
        yy = para(d, x + 10, yy + 2, body, f_b, fw - 20, fill=INK_SOFT,
                  leading=14)
        f_s = F(10, bold=True)
        d.text((x + 10, y0 + fh - 20), "Source: " + source, font=f_s,
               fill=BLUE)

    # ---- ten small illustrated stories
    y0 = 440
    sw = (W - 2 * M - 4 * 10) // 5
    sh = 118
    for j, (region, kicker, head, body, source, kind) in enumerate(SMALL):
        r, c = divmod(j, 5)
        x = M + c * (sw + 10)
        y = y0 + r * (sh + 8)
        card(d, x, y, sw, sh)
        n = j + 4
        num_badge(d, x + 6, y + 6, n, d=17)
        f_k = F(9, bold=True)
        d.text((x + 27, y + 9), kicker, font=f_k, fill=RED_DK)
        illo_small(img, kind, x + 6, y + 26, sw - 12, 46)
        f_h = F(11, bold=True)
        yy = para(d, x + 7, y + 76, head, f_h, sw - 14, leading=13)
        f_s = F(9)
        d.text((x + 7, y + sh - 15), "Source: " + source, font=f_s,
               fill=BLUE)

    # ---- briefs 14-33
    y0 = 696
    d.text((M, y0), "ALSO ON MONDAY", font=F(14, bold=True, serif=True),
           fill=INK)
    f_n = F(10, bold=True)
    d.text((W - M - tw(d, "14–33", f_n), y0 + 2), "14–33", font=f_n,
           fill=RED_DK)
    hline(d, M, y0 + 20, W - 2 * M, INK, 1)
    bw = (W - 2 * M - 16) // 2
    f_b = F(11)
    f_p = F(11, bold=True)
    for j, (region, place, text, source) in enumerate(BRIEFS):
        c = j // 10
        r = j % 10
        x = M + c * (bw + 16)
        y = y0 + 24 + r * 16
        n = str(j + 14) + "."
        d.text((x, y), n, font=f_n, fill=RED_DK)
        px = x + 24
        d.text((px, y), place + " — ", font=f_p, fill=INK)
        w_place = tw(d, place + " — ", f_p)
        d.text((px + w_place, y), text + " ", font=f_b, fill=INK)
        w_text = tw(d, text + " ", f_b)
        f_src = F(10)
        d.text((px + w_place + w_text, y), "(" + source + ")", font=f_src,
               fill=BLUE)

    # ---- world map
    y0 = 880
    d.text((M, y0), "WHERE IT HAPPENED", font=F(14, bold=True, serif=True),
           fill=INK)
    f_m = F(10)
    d.text((M + 220, y0 + 3), "Numbered dots mark the 13 drawn stories.",
           font=f_m, fill=INK_SOFT)
    hline(d, M, y0 + 20, W - 2 * M, INK, 1)
    mx, my, mw, mh = M, y0 + 26, W - 2 * M, 68
    d.rectangle([mx, my, mx + mw, my + mh], fill=SEA, outline=CARD_EDGE)
    lat0, lat1 = -55.0, 75.0
    lon0, lon1 = -170.0, 190.0

    def proj(lon, lat):
        px = mx + (lon - lon0) / (lon1 - lon0) * mw
        py = my + (lat1 - lat) / (lat1 - lat0) * mh
        return px, py

    for pts in CONTINENTS.values():
        poly = [proj(lon, lat) for lon, lat in pts]
        d.polygon(poly, fill=LAND, outline=LAND_LN)
    for i, (lon, lat) in enumerate(DOTS):
        px, py = proj(lon, lat)
        r = 8
        d.ellipse([px - r, py - r, px + r, py + r], fill=RED,
                  outline=(255, 255, 255), width=1)
        t = str(i + 1)
        f = F(9, bold=True)
        d.text((px - tw(d, t, f) / 2, py - 5), t, font=f,
               fill=(255, 255, 255))

    # ---- footer / date check
    y0 = 978
    hline(d, M, y0, W - 2 * M, INK, 2)
    f_f = F(10, bold=True)
    d.text((M, y0 + 6), "DATE CHECK ✓", font=f_f, fill=GREEN)
    f_f2 = F(10)
    line1 = ("Every story above happened or was first reported on Monday "
             "23 November 2026, unless marked below.")
    d.text((M + 92, y0 + 6), line1, font=f_f2, fill=INK)
    line2 = ("NOT 23 NOV NEWS: Cyclone Akvan made landfall 20 Nov (372,000 "
             "sheltered, 0 deaths)  ·  BepiColombo reached Mercury 21 Nov  ·  "
             "Riemann proof claim announced 20 Nov.  Sources: Reuters · AP · "
             "AFP · BBC · Al Jazeera · The Guardian · Nature · CoinDesk · "
             "ESA · Oxfam · Standard Topic.")
    para(d, M, y0 + 20, line2, f_f2, W - 2 * M, fill=INK_SOFT, leading=11)
    return img


def main():
    img = build()
    out = os.path.join(HERE, "entry.png")
    img.save(out, format="PNG")
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
