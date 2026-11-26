#!/usr/bin/env python3
"""Draw the news-image-20261126 v2 front page (1024x1024 PNG).

Written from scratch for the make.fun news-image-20261126 competition.
Every headline below was verified against wire or primary sources carrying
a 26 November 2026 timestamp, confirmed by a second independent source.
Prior-day stories are listed in the printed DATE CHECK box, never as
headlines. Parent-session fix (2026-11-27): story 12 was the Cairo Ring
Road tanker fire, first reported Wed 25 Nov (AP/Reuters) — moved to the
DATE CHECK box; panel 12 is now UK net migration (ONS, 26 Nov) and list
28 is the 26 Nov arrest of the Cairo driver (AP). The UN Nigeria warning
was NOT promoted: the OHCHR statement was issued Wed 25 Nov (reported
26 Nov), so it stays out of the headlines. No external assets: every
scene is drawn with PIL primitives.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

# ---------------------------------------------------------------- stories
# n, headline, deck, region, utc_hhmm, label, source
LEADS = [
    (1, "Macy's 100th parade postponed to Saturday",
     "First weather postponement in its history, as a coastal storm bears down on New York.",
     "N. AMERICA", "05:43", "REPORTED", "AP"),
    (2, "India marks 18 years since the 26/11 attacks",
     "Candles at the Gateway of India; Jaishankar vows zero tolerance on terror.",
     "S. ASIA", "03:30", "OFFICIAL", "ANI/IANS"),
    (3, "Gukesh-Sindarov Game 3 ends in a 60-move draw",
     "Third straight draw in Geneva leaves the title match level at 1.5-1.5.",
     "EUROPE", "18:00", "CONFIRMED", "CHESS.COM"),
]
PANELS = [
    (4, "Bank of Korea lifts rate to 3.25%",
     "Third hike since July as chip exports boom; 2027 growth raised to 4.1%.",
     "E. ASIA", "00:30", "OFFICIAL", "BOK"),
    (5, "Kim orders wider tactical nuclear deployment",
     "North Korea's leader tours nuclear sites and calls for more tactical arms.",
     "E. ASIA", "01:00", "OFFICIAL", "KCNA"),
    (6, "Russian missiles hit Kyiv mall and grain ships",
     "Seven hurt in the capital; cargo vessels struck off Odesa.",
     "EUROPE", "02:30", "CONFIRMED", "REUTERS"),
    (7, "Israeli strikes kill nine in Gaza",
     "Dead include a Hamas-appointed deputy education minister.",
     "MIDDLE EAST", "03:00", "REPORTED", "BBC"),
    (8, "Israel threatens to displace one million in Gaza",
     "Katz: move unless Hamas disarms, as it promised.",
     "MIDDLE EAST", "12:28", "OFFICIAL", "REUTERS"),
    (9, "UK sanctions Houthis as Red Sea attacks widen",
     "Group claims strikes on Jeddah and Jazan ports; Jazan hit, minor damage.",
     "MIDDLE EAST", "10:00", "REPORTED", "REUTERS"),
    (10, "Two tankers hit mines in the Strait of Hormuz",
     "IRGC reports explosions off Khasab; Brent jumps to $96.57.",
     "MIDDLE EAST", "09:30", "CLAIM", "REUTERS"),
    (11, "Ebola cases in eastern Congo pass 12,000",
     "Outbreak spreads as fighting disrupts the response.",
     "AFRICA", "11:00", "REPORTED", "REUTERS"),
    (12, "UK net migration falls to 77,000",
     "Lowest since 1997 outside Covid; down from 204,000 a year earlier.",
     "EUROPE", "07:00", "OFFICIAL", "ONS"),
    (13, "Blast at Bangkok refinery injures nine",
     "Fire at Bangchak's Phra Khanong plant; three critical, output halted.",
     "SE ASIA", "07:45", "CONFIRMED", "AP"),
]
LISTED = [
    (14, "EU leaders split over \u20ac45bn Ukraine loan",
     "Brussels debates the 2028-34 budget and Kyiv funding for 2027.",
     "EUROPE", "13:00", "CONFIRMED", "REUTERS"),
    (15, "Ukrainian drone kills five in Zaporizhzhia",
     "Parking-lot strike in the Russian-held city; three wounded.",
     "EUROPE", "10:02", "REPORTED", "REUTERS"),
    (16, "Ukraine says it hit five jets at Russian airbase",
     "Kyiv claims three MiG-31s and two Su-34s damaged at Savasleyka.",
     "EUROPE", "14:00", "CLAIM", "REUTERS"),
    (17, "Spain votes Sunday; right bloc leads polls",
     "PP near 31% and Vox 18% ahead of the snap election.",
     "EUROPE", "16:00", "REPORTED", "REUTERS"),
    (18, "Shipping groups demand action on Hormuz threat",
     "Eight associations call for safeguards for freedom of navigation.",
     "GLOBAL", "10:38", "REPORTED", "SAFETY4SEA"),
    (19, "Germany arrests two over synagogue attack plot",
     "Iraqi suspects held in Cologne and Heidelberg over a March plot.",
     "EUROPE", "11:00", "REPORTED", "AP"),
    (20, "Myanmar rejects parts of ICJ genocide ruling",
     "Min Aung Hlaing defies the court in his first remarks since the verdict.",
     "SE ASIA", "10:25", "OFFICIAL", "AFP"),
    (21, "Bangladesh sets garment minimum wage",
     "Wage board finalises the pay floor for the export industry.",
     "S. ASIA", "10:00", "REPORTED", "REUTERS"),
    (22, "Gold mine flood in Indonesia kills 13",
     "Thirteen more missing in the flooded illegal pit near Bogor.",
     "SE ASIA", "06:00", "REPORTED", "AP"),
    (23, "Drone attack in Kuwait kills two Italians",
     "Kuwait blames Iranian drones; Tehran denies any role.",
     "MIDDLE EAST", "12:40", "CLAIM", "REUTERS"),
    (24, "ISIL suicide blast kills two in Hasakah",
     "Attack on a security checkpoint in north-east Syria; five hurt.",
     "MIDDLE EAST", "13:00", "REPORTED", "AFP"),
    (25, "Blast hits Sanaa as missiles fly at Riyadh",
     "Coalition says it downed missiles over the Saudi capital.",
     "MIDDLE EAST", "15:00", "REPORTED", "AL JAZEERA"),
    (26, "Anti-Netanyahu bloc agrees coalition deal",
     "Eisenkot pact signed, but still 25 seats short of a majority.",
     "MIDDLE EAST", "13:47", "REPORTED", "J. POST"),
    (27, "WFP warns of severe food shortage in Sudan",
     "Nineteen killed in Blue Nile drone strikes, monitors say.",
     "AFRICA", "16:00", "REPORTED", "WFP"),
    (28, "Egypt arrests driver in Cairo tanker crash probe",
     "Driver admits speeding before the Ring Road fire that killed 31.",
     "AFRICA", "08:00", "REPORTED", "AP"),
    (29, "Kyiv admits striking ships off Libya",
     "Ukraine says it hit Russian vessels at Benghazi on 22 Nov.",
     "AFRICA", "17:00", "CONFIRMED", "REUTERS"),
    (30, "Diesel tanker sinks off Ibiza; one crew dead",
     "Fuel tanker goes down near the Spanish island.",
     "EUROPE", "09:00", "REPORTED", "REUTERS"),
    (31, "UN: 47,000 women killed by family in 2025",
     "About five an hour, a new UN report finds.",
     "GLOBAL", "10:00", "OFFICIAL", "UN"),
    (32, "RAM prices triple as AI drains chip supply",
     "Memory kits cost 3x months ago; buyers squeezed before Black Friday.",
     "E. ASIA", "08:00", "REPORTED", "REUTERS"),
    (33, "Milei stays silent on Lula's win",
     "Argentina's leader still refuses to recognise Lula's re-election.",
     "S. AMERICA", "09:00", "REPORTED", "WNBC"),
    (34, "Jamaica advances 300 MW renewables plan",
     "State pushes green power procurement; trade gap widens.",
     "CARIBBEAN", "17:00", "REPORTED", "PBCJ"),
    (35, "Solomons opposition attacks Australia treaty",
     "Ex-PM Sogavare calls the A$740m pact a sell-out of sovereignty.",
     "OCEANIA", "06:00", "REPORTED", "AAP"),
    (36, "Nor'easter batters the US East Coast",
     "400,000+ homes lose power; hundreds of flights cancelled.",
     "N. AMERICA", "14:00", "REPORTED", "REUTERS"),
]
ALL = LEADS + PANELS + LISTED
assert len(ALL) == 36, len(ALL)
assert [s[0] for s in ALL] == list(range(1, 37))

DATE_CHECK = [
    "USTR tariff plan for 14 economies - Wed 25 Nov",
    "Cairo Ring Road tanker fire, 31 killed - Wed 25 Nov",
    "FCC clears SpaceX Starmind, 1m satellites - Wed 25 Nov",
    "Houthi claim: Ras Tanura refinery hit - Wed 25 Nov",
    "COP31 talks collapse in Antalya - Sun 22 Nov",
    "Puerto Rico court voids LUMA extension - Wed 25 Nov",
    "Greece 24-hour general strike - Wed 25 Nov",
    "Ramaphosa Phala Phala report set aside - Wed 25 Nov",
]

REGIONS = [("N. AMERICA", 2), ("CARIBBEAN", 1), ("S. AMERICA", 1),
           ("EUROPE", 9), ("MIDDLE EAST", 8), ("AFRICA", 4),
           ("S. ASIA", 2), ("E. ASIA", 3), ("SE ASIA", 3),
           ("OCEANIA", 1), ("GLOBAL", 2)]
assert sum(c for _, c in REGIONS) == 36
SOURCES = ["AP", "REUTERS", "AFP", "BBC", "ANI", "IANS", "BOK", "KCNA",
           "ONS", "UN", "WFP", "AAP", "PBCJ", "CHESS.COM", "AL JAZEERA",
           "WNBC", "J. POST", "SAFETY4SEA"]
assert len(SOURCES) == 18

TICKER = ("MARKETS  -  BRENT $96.5  +2.0%   -   NIKKEI 57,499  +0.9%   -   "
          "KOSPI 4,711  +0.3%   -   HANG SENG 22,227  +1.2%   -   "
          "DAX 25,180  +1.9%   -   US MARKETS CLOSED (THANKSGIVING)")

# ------------------------------------------------------------------ style
PAPER = (248, 244, 233)
INK = (25, 25, 25)
MUTED = (90, 84, 70)
RULE = (178, 168, 148)
CARD = (255, 255, 255)
CARD_EDGE = (216, 210, 192)
RED = (179, 38, 30)
NAVY = (31, 58, 95)
TEAL = (15, 107, 92)
GOLD = (176, 124, 0)
SKY = (198, 222, 235)
LABEL_BG = (31, 58, 95)

FD = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FD, name), size)


F_TITLE = lambda s: font("DejaVuSans-Bold.ttf", s)
F_BOLD = lambda s: font("DejaVuSans-Bold.ttf", s)
F_REG = lambda s: font("DejaVuSans.ttf", s)


def text_w(d, s, f):
    return d.textlength(s, font=f)


def wrap(d, s, f, max_w):
    """Word-boundary wrap; never splits a word."""
    words, lines, cur = s.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if d.textlength(trial, font=f) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def fit_lines(d, s, f, max_w, max_lines):
    """Wrap, shrinking the font until it fits in max_lines; returns lines."""
    size = f.size
    while size > 7:
        ff = font("DejaVuSans-Bold.ttf" if "Bold" in f.path else "DejaVuSans.ttf", size)
        lines = wrap(d, s, ff, max_w)
        if len(lines) <= max_lines:
            return lines, ff
        size -= 1
    return wrap(d, s, ff, max_w), ff


def meta_line(s):
    return "%s  \u2022  %s  \u2022  %s UTC" % (s[6], s[5], s[4])


def draw_label(d, x, y, label):
    f = F_BOLD(8)
    tw = d.textlength(label, font=f) + 8
    d.rounded_rectangle([x, y, x + tw, y + 12], radius=2, fill=LABEL_BG)
    d.text((x + 4, y + 1), label, font=f, fill=(255, 255, 255))
    return tw


# ------------------------------------------------------------------ scenes
def _flame(d, cx, by, s):
    d.polygon([(cx - s, by), (cx, by - 2.2 * s), (cx + s, by)], fill=(230, 90, 20))
    d.polygon([(cx - 0.5 * s, by), (cx, by - 1.3 * s), (cx + 0.5 * s, by)],
              fill=(250, 200, 60))


def _smoke(d, x, y, r, col=(150, 150, 150)):
    d.ellipse([x, y, x + r, y + r], fill=col)
    d.ellipse([x + r * 0.6, y - r * 0.5, x + r * 1.6, y + r * 0.5], fill=col)
    d.ellipse([x + r * 1.1, y + r * 0.2, x + r * 2.0, y + r * 1.1], fill=col)


def _burst(d, cx, cy, r, col=(240, 120, 30)):
    pts = []
    import math
    for i in range(16):
        a = math.pi * i / 8
        rr = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    d.polygon(pts, fill=col)


def scene(d, n, x, y, w, h):
    """Drawn scene for illustrated story n inside box (x,y,w,h)."""
    d.rectangle([x, y, x + w, y + h], fill=SKY)
    if n == 1:  # Macy's balloon over Manhattan
        for bx in (x + 8, x + w - 34):
            d.rectangle([bx, y + h - 46, bx + 24, y + h], fill=(70, 70, 90))
            for wy in range(y + h - 42, y + h - 4, 9):
                d.rectangle([bx + 4, wy, bx + 10, wy + 5], fill=(250, 220, 90))
                d.rectangle([bx + 15, wy, bx + 21, wy + 5], fill=(250, 220, 90))
        d.ellipse([x + w // 2 - 34, y + 6, x + w // 2 + 34, y + 52], fill=RED)
        d.ellipse([x + w // 2 - 34, y + 6, x + w // 2 - 8, y + 52], fill=(210, 70, 60))
        d.line([x + w // 2 - 12, y + 52, x + w // 2 - 8, y + 66], fill=INK, width=2)
        d.line([x + w // 2 + 12, y + 52, x + w // 2 + 8, y + 66], fill=INK, width=2)
        d.ellipse([x + w // 2 - 8, y + 64, x + w // 2 + 8, y + 74], fill=(250, 200, 60))
    elif n == 2:  # Gateway of India + candles
        d.rectangle([x, y + h - 14, x + w, y + h], fill=(120, 100, 70))
        d.rectangle([x + w // 2 - 52, y + 8, x + w // 2 + 52, y + h - 14], fill=(196, 164, 110))
        d.pieslice([x + w // 2 - 26, y + 30, x + w // 2 + 26, y + h - 14],
                   180, 360, fill=SKY)
        d.rectangle([x + w // 2 - 52, y + 4, x + w // 2 + 52, y + 12], fill=(170, 138, 88))
        for i, cx in enumerate((x + 22, x + w // 2, x + w - 26)):
            d.rectangle([cx - 3, y + h - 26, cx + 3, y + h - 14], fill=(250, 250, 240))
            _flame(d, cx, y + h - 26, 4)
    elif n == 3:  # chessboard
        sq = w // 8
        for r in range(2):
            for c in range(8):
                col = (240, 230, 210) if (r + c) % 2 == 0 else (60, 60, 70)
                d.rectangle([x + c * sq, y + r * (h // 2), x + (c + 1) * sq,
                             y + (r + 1) * (h // 2)], fill=col)
        d.rectangle([x, y + h - 4, x + w, y + h], fill=(120, 90, 40))
        d.ellipse([x + 14, y + h - 44, x + 44, y + h - 14], fill=(250, 250, 240),
                  outline=INK, width=2)
        d.text((x + 24, y + h - 40), "+", font=F_BOLD(20), fill=INK)
        d.ellipse([x + w - 44, y + 8, x + w - 14, y + 38], fill=(30, 30, 35),
                  outline=(200, 200, 200), width=2)
    elif n == 4:  # central bank + rising rate
        d.rectangle([x, y + h - 12, x + w, y + h], fill=(90, 90, 100))
        d.polygon([(x + w // 2 - 56, y + 26), (x + w // 2 + 56, y + 26),
                   (x + w // 2, y + 6)], fill=NAVY)
        for i in range(4):
            cx = x + w // 2 - 42 + i * 28
            d.rectangle([cx, y + 28, cx + 12, y + h - 12], fill=(240, 240, 235))
        d.line([x + 14, y + h - 22, x + w - 50, y + 12], fill=(20, 140, 60), width=4)
        d.polygon([(x + w - 50, y + 12), (x + w - 62, y + 16), (x + w - 50, y + 24)],
                  fill=(20, 140, 60))
    elif n == 5:  # missile + star
        d.rectangle([x, y, x + w, y + h], fill=(30, 34, 54))
        for sx, sy in ((x + 16, y + 6), (x + w - 26, y + 12), (x + w // 2 + 26, y + 4)):
            d.text((sx, sy), "*", font=F_BOLD(13), fill=(255, 255, 255))
        cx = x + w // 2
        d.polygon([(cx - 5, y + h - 10), (cx + 5, y + h - 10),
                   (cx + 3, y + 8), (cx - 3, y + 8)], fill=(235, 235, 230))
        d.polygon([(cx - 3, y + 8), (cx + 3, y + 8), (cx, y + 2)], fill=RED)
        _flame(d, cx, y + h - 10, 5)
        _smoke(d, cx - 22, y + h - 10, 8, (120, 120, 130))
    elif n == 6:  # Kyiv building + blast
        d.rectangle([x + 10, y + h - 52, x + 64, y + h], fill=(90, 90, 105))
        d.rectangle([x + w - 70, y + h - 40, x + w - 12, y + h], fill=(110, 110, 125))
        for wy in range(y + h - 46, y + h - 6, 10):
            d.rectangle([x + 18, wy, x + 26, wy + 6], fill=(250, 220, 90))
            d.rectangle([x + 40, wy, x + 48, wy + 6], fill=(250, 220, 90))
        _burst(d, x + w // 2 + 8, y + 26, 22)
        d.line([x + w // 2 + 8, y + 26, x + w - 30, y + h - 40], fill=(60, 60, 60), width=2)
        _smoke(d, x + w - 78, y + 8, 12)
    elif n == 7:  # Gaza skyline + smoke
        d.rectangle([x, y + h - 16, x + w, y + h], fill=(140, 120, 90))
        for bx, bh in ((8, 44), (44, 62), (86, 38), (122, 54)):
            d.rectangle([x + bx, y + h - 16 - bh, x + bx + 32, y + h - 16],
                        fill=(80, 76, 70))
        _smoke(d, x + 52, y + 6, 13)
        _smoke(d, x + 110, y + 16, 10)
        _flame(d, x + w // 2, y + h - 16, 8)
    elif n == 8:  # displacement warning: map + arrow + 1M
        d.rectangle([x, y, x + w, y + h], fill=(245, 230, 210))
        d.ellipse([x + 12, y + 12, x + w - 12, y + h - 10], outline=NAVY, width=3)
        d.line([x + 22, y + h - 26, x + w - 30, y + 18], fill=RED, width=4)
        d.polygon([(x + w - 30, y + 18), (x + w - 46, y + 20), (x + w - 34, y + 32)],
                  fill=RED)
        d.text((x + 12, y + 6), "1M", font=F_BOLD(20), fill=RED)
    elif n == 9:  # ship + drone over port
        d.rectangle([x, y + h - 26, x + w, y + h], fill=(40, 90, 140))
        d.polygon([(x + 14, y + h - 26), (x + w - 14, y + h - 26),
                   (x + w - 26, y + h - 8), (x + 26, y + h - 8)], fill=(60, 60, 70))
        for i, col in enumerate(((200, 60, 50), (240, 180, 40), (40, 120, 80))):
            d.rectangle([x + 24 + i * 30, y + h - 52, x + 50 + i * 30, y + h - 26],
                        fill=col)
        d.ellipse([x + w - 44, y + 10, x + w - 28, y + 26], fill=(40, 40, 40))
        d.line([x + w - 52, y + 8, x + w - 20, y + 8], fill=(40, 40, 40), width=2)
        d.line([x + w - 52, y + 28, x + w - 20, y + 28], fill=(40, 40, 40), width=2)
    elif n == 10:  # tanker + mine
        d.rectangle([x, y + h - 30, x + w, y + h], fill=(30, 80, 130))
        d.rectangle([x + 10, y + h - 52, x + w - 40, y + h - 30], fill=(120, 30, 25))
        d.rectangle([x + w - 40, y + h - 62, x + w - 14, y + h - 30], fill=(200, 200, 195))
        cx, cy = x + w - 66, y + 22
        for dx, dy in ((-14, 0), (14, 0), (0, -14), (0, 14), (-10, -10), (10, -10),
                       (-10, 10), (10, 10)):
            d.line([cx, cy, cx + dx, cy + dy], fill=INK, width=2)
        d.ellipse([cx - 10, cy - 10, cx + 10, cy + 10], fill=(40, 40, 40))
        _flame(d, x + 30, y + h - 52, 7)
    elif n == 11:  # virus + cross
        d.rectangle([x, y, x + w, y + h], fill=(232, 244, 238))
        cx, cy = x + w // 2, y + h // 2 + 2
        for dx, dy in ((-26, 0), (26, 0), (0, -24), (0, 24), (-19, -19), (19, -19),
                       (-19, 19), (19, 19)):
            d.line([cx, cy, cx + dx, cy + dy], fill=TEAL, width=3)
        d.ellipse([cx - 18, cy - 18, cx + 18, cy + 18], fill=TEAL)
        d.rectangle([cx - 9, cy - 3, cx + 9, cy + 3], fill=(255, 255, 255))
        d.rectangle([cx - 3, cy - 9, cx + 3, cy + 9], fill=(255, 255, 255))
    elif n == 12:  # net migration falling: descending bars + down arrow
        d.rectangle([x, y, x + w, y + h], fill=(235, 238, 245))
        d.line([x + 8, y + h - 8, x + w - 8, y + h - 8], fill=INK, width=2)
        bx = [x + 22, x + w // 2 - 8, x + w - 52]
        bh = [30, 16, 7]
        bc = [NAVY, TEAL, GOLD]
        for xx, hh, col in zip(bx, bh, bc):
            d.rectangle([xx, y + h - 8 - hh, xx + 26, y + h - 8], fill=col)
        d.line([x + 14, y + 8, x + w - 16, y + h - 14], fill=RED, width=3)
        d.polygon([(x + w - 16, y + h - 14), (x + w - 30, y + h - 16),
                   (x + w - 20, y + h - 26)], fill=RED)
        d.text((x + w - 52, y + 2), "77k", font=F_BOLD(13), fill=RED)
    else:  # 13: refinery towers + fire
        d.rectangle([x + 12, y + h - 58, x + 34, y + h], fill=(90, 90, 100))
        d.rectangle([x + 44, y + h - 74, x + 62, y + h], fill=(110, 110, 120))
        d.rectangle([x + 72, y + h - 48, x + 96, y + h], fill=(80, 80, 90))
        d.line([x + 53, y + h - 74, x + 53, y + h - 90], fill=(90, 90, 100), width=3)
        _flame(d, x + 53, y + h - 58, 9)
        _flame(d, x + 84, y + h - 48, 7)
        _smoke(d, x + 100, y + 4, 12)
        d.rectangle([x, y + h - 8, x + w, y + h], fill=(120, 100, 70))


# ---------------------------------------------------------------- world map
# Coarse land grid (56 cols x 24 rows); lon -180..180, lat 80..-60.
LAND = [
    (0, 0, 30, 48), (1, 1, 28, 49), (2, 2, 1, 10), (2, 2, 13, 15),
    (2, 3, 27, 50), (3, 3, 1, 11), (3, 3, 16, 18), (3, 4, 26, 50),
    (4, 4, 2, 11), (4, 4, 18, 20), (4, 5, 25, 49), (5, 5, 3, 11),
    (5, 5, 19, 21), (5, 6, 25, 48), (6, 6, 4, 12), (6, 6, 27, 33),
    (6, 7, 36, 48), (7, 7, 5, 13), (7, 7, 27, 33), (7, 8, 36, 49),
    (8, 8, 6, 13), (8, 8, 27, 32), (8, 9, 35, 49), (9, 9, 8, 14),
    (9, 9, 28, 36), (9, 10, 38, 49), (10, 10, 12, 15), (10, 10, 28, 36),
    (10, 11, 39, 47), (11, 11, 17, 22), (11, 11, 28, 35), (11, 12, 39, 46),
    (12, 12, 18, 22), (12, 12, 28, 35), (12, 13, 40, 45), (13, 13, 18, 22),
    (13, 13, 29, 35), (13, 14, 41, 47), (14, 14, 18, 21), (14, 14, 30, 34),
    (14, 15, 43, 48), (15, 15, 18, 21), (15, 15, 30, 34), (16, 16, 19, 20),
    (16, 16, 30, 33), (16, 17, 46, 52), (17, 17, 19, 20), (17, 17, 31, 33),
    (17, 18, 47, 52), (18, 18, 19, 20), (18, 19, 48, 52), (19, 19, 53, 54),
    (20, 20, 53, 54),
]
LAND_CELLS = set()
for r0, r1, c0, c1 in LAND:
    for r in range(r0, r1 + 1):
        for c in range(c0, c1 + 1):
            LAND_CELLS.add((r, c))

# lon/lat of illustrated stories 1-13 (+ small nudge to avoid overlaps)
PINS = {
    1: (-74.0, 40.7, 0, 0), 2: (72.8, 19.0, 0, 0), 3: (6.1, 46.2, 0, 0),
    4: (127.0, 37.5, 0, 0), 5: (125.7, 39.0, 6, -6), 6: (30.5, 50.4, 0, 0),
    7: (34.5, 31.5, 0, 0), 8: (35.2, 31.8, 9, 7), 9: (39.2, 21.5, 0, 0),
    10: (56.5, 26.5, 0, 0), 11: (29.2, -1.7, 0, 0), 12: (-0.1, 51.5, 12, -8),
    13: (100.5, 13.7, 0, 0),
}

# ------------------------------------------------------------------ layout
def draw_map(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(214, 230, 240), outline=CARD_EDGE)
    d.text((x + 6, y + 3), "WHERE IT HAPPENED  -  STORIES 1-13",
           font=F_BOLD(9), fill=NAVY)
    mx, my, mw, mh = x + 6, y + 16, w - 12, h - 20
    cw, ch = mw / 56.0, mh / 24.0
    for (r, c) in LAND_CELLS:
        d.ellipse([mx + c * cw, my + r * ch, mx + (c + 1) * cw - 0.5,
                   my + (r + 1) * ch - 0.5], fill=(110, 140, 110))
    for n in range(1, 14):
        lon, lat, dx, dy = PINS[n]
        px = mx + (lon + 180) / 360.0 * mw + dx
        py = my + (80 - lat) / 140.0 * mh + dy
        d.ellipse([px - 7, py - 7, px + 7, py + 7], fill=RED, outline=(255, 255, 255),
                  width=1)
        d.text((px - 2, py - 6), str(n), font=F_BOLD(8), fill=(255, 255, 255))


def draw_timeline(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=CARD, outline=CARD_EDGE)
    d.text((x + 6, y + 3), "THE DAY IN UTC  -  FIRST WIRE TIMES, STORIES 1-13",
           font=F_BOLD(9), fill=NAVY)
    tx, tw = x + 10, w - 20
    ty = y + h - 22
    d.line([tx, ty, tx + tw, ty], fill=INK, width=2)
    for hh in range(0, 25, 4):
        px = tx + tw * hh / 24.0
        d.line([px, ty - 4, px, ty + 4], fill=INK, width=2)
        d.text((px - 8, ty + 6), "%02d:00" % hh, font=F_REG(8), fill=MUTED)
    placed = []
    for s in LEADS + PANELS:
        hh, mm = int(s[4][:2]), int(s[4][3:])
        px = tx + tw * (hh + mm / 60.0) / 24.0
        row = 0
        for (ox, orow) in placed:
            if abs(px - ox) < 13 and orow == 0:
                row = 1
        placed.append((px, row))
        py = ty - 13 if row == 0 else ty - 26
        d.ellipse([px - 6, py - 6, px + 6, py + 6], fill=RED, outline=(255, 255, 255))
        d.text((px - 2, py - 5), str(s[0]), font=F_BOLD(7), fill=(255, 255, 255))
        d.line([px, py + 6, px, ty], fill=RED, width=1)


def draw_datecheck(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(255, 246, 220), outline=(200, 160, 60))
    d.text((x + 6, y + 3), "DATE CHECK  -  FIRST REPORTED EARLIER: EXCLUDED",
           font=F_BOLD(9), fill=(140, 90, 0))
    yy = y + 17
    for item in DATE_CHECK:
        d.text((x + 6, yy), "\u2717  " + item, font=F_REG(8), fill=(90, 60, 10))
        yy += 11


def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    warns = []

    # masthead
    d.rectangle([10, 8, W - 10, 86], fill=NAVY)
    d.text((20, 14), "THE WORLD IN ONE DAY", font=F_TITLE(34), fill=(255, 255, 255))
    d.text((20, 56), "Thursday 26 November 2026  \u2014  the day's world news in one picture",
           font=F_REG(14), fill=(220, 225, 235))
    d.text((W - 20, 20), "36 STORIES", font=F_BOLD(20), fill=(255, 210, 90),
           anchor="ra")
    d.text((W - 20, 48), "11 REGIONS  \u2022  18 SOURCES  \u2022  15 FIELDS",
           font=F_BOLD(11), fill=(255, 255, 255), anchor="ra")

    # leads
    lx, lw, lh = 10, 328, 204
    for i, s in enumerate(LEADS):
        x = lx + i * (lw + 10)
        y = 92
        d.rectangle([x, y, x + lw, y + lh], fill=CARD, outline=CARD_EDGE)
        d.rectangle([x, y, x + lw, y + 20], fill=RED)
        d.text((x + 8, y + 3), "LEAD %d  \u2014  %s" % (s[0], s[3]),
               font=F_BOLD(11), fill=(255, 255, 255))
        scene(d, s[0], x + 4, y + 24, lw - 8, 96)
        lines, f = fit_lines(d, s[1], F_BOLD(15), lw - 16, 2)
        if len(lines) > 2:
            warns.append("lead %d headline overflows" % s[0])
        yy = y + 126
        for ln in lines:
            d.text((x + 8, yy), ln, font=f, fill=INK)
            yy += 17
        lines, f = fit_lines(d, s[2], F_REG(11), lw - 16, 2)
        if len(lines) > 2:
            warns.append("lead %d deck overflows" % s[0])
        for ln in lines:
            d.text((x + 8, yy), ln, font=f, fill=MUTED)
            yy += 13
        d.text((x + 8, y + lh - 16), meta_line(s), font=F_REG(9), fill=MUTED)
        draw_label(d, x + lw - 74, y + lh - 17, s[5])

    # panels 4-13: 5 cols x 2 rows
    pw, ph, gap = 196, 126, 6
    for i, s in enumerate(PANELS):
        col, row = i % 5, i // 5
        x = 10 + col * (pw + gap)
        y = 302 + row * (ph + gap)
        d.rectangle([x, y, x + pw, y + ph], fill=CARD, outline=CARD_EDGE)
        d.text((x + 5, y + 3), "%d" % s[0], font=F_BOLD(11), fill=RED)
        d.text((x + 22, y + 3), s[3], font=F_BOLD(8), fill=MUTED)
        scene(d, s[0], x + 4, y + 17, pw - 8, 44)
        lines, f = fit_lines(d, s[1], F_BOLD(11), pw - 10, 2)
        if len(lines) > 2:
            warns.append("panel %d headline overflows" % s[0])
        yy = y + 64
        for ln in lines:
            d.text((x + 5, yy), ln, font=f, fill=INK)
            yy += 12
        lines, f = fit_lines(d, s[2], F_REG(9), pw - 10, 2)
        if len(lines) > 2:
            warns.append("panel %d deck overflows" % s[0])
        for ln in lines:
            d.text((x + 5, yy), ln, font=f, fill=MUTED)
            yy += 11
        d.text((x + 5, y + ph - 13), "%s \u2022 %s UTC" % (s[6], s[4]),
               font=F_REG(8), fill=MUTED)
        draw_label(d, x + pw - 62, y + ph - 14, s[5])

    # list 14-36: two columns
    d.text((10, 566), "THE REST OF THE DAY  \u2014  STORIES 14-36",
           font=F_BOLD(13), fill=NAVY)
    d.line([10, 584, W - 10, 584], fill=RULE, width=1)
    col_w, pitch = 497, 24
    for i, s in enumerate(LISTED):
        col = 0 if i < 12 else 1
        row = i if i < 12 else i - 12
        x = 10 + col * (col_w + 10)
        y = 590 + row * pitch
        head = "%d. %s" % (s[0], s[1])
        lines, f = fit_lines(d, head, F_BOLD(11), col_w - 4, 1)
        if len(lines) > 1:
            warns.append("list %d headline wraps" % s[0])
        d.text((x, y), lines[0], font=f, fill=INK)
        deck = "%s  \u2014  %s \u2022 %s \u2022 %s UTC" % (s[2], s[6], s[5], s[4])
        lines, f = fit_lines(d, deck, F_REG(9), col_w - 4, 1)
        if len(lines) > 1:
            warns.append("list %d deck wraps" % s[0])
        d.text((x + 16, y + 12), lines[0], font=f, fill=MUTED)

    # bottom row: map / timeline / date check
    by = 880
    draw_map(d, 10, by, 330, 84)
    draw_timeline(d, 348, by, 330, 84)
    draw_datecheck(d, 686, by, 328, 84)

    # region bar
    ry = 970
    d.rectangle([10, ry, W - 10, ry + 22], fill=(235, 230, 215))
    parts = "  \u2022  ".join("%s %d" % (r, c) for r, c in REGIONS)
    d.text((14, ry + 5), "REGIONS:  " + parts, font=F_BOLD(10), fill=INK)

    # ticker + sources
    d.text((10, 996), TICKER, font=F_BOLD(9), fill=NAVY)
    d.text((10, 1010), "SOURCES: " + ", ".join(SOURCES) + ".  ALL STORIES FIRST REPORTED 26 NOV 2026; PRIOR-DAY ITEMS IN DATE CHECK ONLY.",
           font=F_REG(8), fill=MUTED)

    img.save(OUT, optimize=True)
    size = os.path.getsize(OUT)
    print("wrote %s %d bytes %s" % (OUT, size, img.size))
    print("warnings:", warns if warns else "none")
    assert img.size[0] <= 1024 and img.size[1] <= 1024
    assert size <= 1048576, size
    return warns


if __name__ == "__main__":
    build()
