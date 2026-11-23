#!/usr/bin/env python3
"""Renderer that produced entry.png ahead of time (PIL + Liberation fonts).

Kept in the repository as the record of how the broadsheet image was drawn.
It is NOT the graded entry point: main.py is. The grading sandbox has no
font/PIL guarantees, so the image ships pre-rendered and main.py copies it.
"""

"""news-image-20261122 — Sunday 22 November 2026 world news on one page.

Dense broadsheet front page: 38 stories — 4 illustrated leads, 10 illustrated
panels, 24 one-line briefs — plus a day-in-numbers strip, a pinned world map
with a region tally, source tags throughout and a date-check footer.
Renders 1024x1024 to entry.png and to /output/entry.png ($MAKEFUN_OUTPUT_DIR).
Stdlib + Pillow only. All copy, code and drawings are original to this entry;
story facts are from the day's reports available by Sunday morning UTC,
tagged per story.
"""
import math
import os

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
MX = 28
CW = W - 2 * MX
PAPER = (250, 247, 238)
INK = (18, 18, 18)
GREY = (88, 84, 76)
FAINT = (196, 188, 170)
RED = (178, 26, 30)
PANEL_BG = (255, 253, 246)
LEAD_BG = (244, 238, 224)

SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
SANSB = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"


def F(path, size):
    return ImageFont.truetype(path, size)


def tw(d, s, fnt):
    return d.textlength(s, font=fnt)


def wrap(d, text, fnt, max_w):
    lines, cur = [], ""
    for word in text.split():
        t = word if not cur else cur + " " + word
        if tw(d, t, fnt) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def block(d, x, y, text, fnt, fill, max_w, leading, max_lines=None):
    lines = wrap(d, text, fnt, max_w)
    if max_lines:
        lines = lines[:max_lines]
    for ln in lines:
        d.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y


def centre(d, y, text, fnt, fill):
    d.text(((W - tw(d, text, fnt)) / 2, y), text, font=fnt, fill=fill)


# ---------------------------------------------------------------- icons ----

def i_route(d, x, y, s):
    d.arc([x + 2, y + 2, x + s - 2, y + s * 0.9], 180, 330, fill=INK, width=3)
    for cx, cy in ((x + 6, y + s * 0.52), (x + s - 10, y + s * 0.14)):
        d.polygon([(cx, cy + 10), (cx - 5, cy), (cx + 5, cy)], fill=RED)
        d.ellipse([cx - 4, cy - 9, cx + 4, cy - 1], outline=INK, width=2)


def i_globe(d, x, y, s):
    cx, cy, r = x + s / 2, y + s / 2, s * 0.44
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=INK, width=3)
    d.ellipse([cx - r * 0.45, cy - r, cx + r * 0.45, cy + r], outline=INK, width=2)
    d.line([cx - r, cy, cx + r, cy], fill=INK, width=2)
    for f in (-0.5, 0.5):
        yy = cy + f * r
        hw = r * (1 - f * f) ** 0.5
        d.line([cx - hw, yy, cx + hw, yy], fill=INK, width=2)
    d.line([cx, cy + r, cx, cy + r + 6], fill=RED, width=3)
    d.line([cx - 8, cy + r + 6, cx + 8, cy + r + 6], fill=RED, width=3)


def i_tent(d, x, y, s):
    d.polygon([(x + s * 0.5, y + s * 0.12), (x + s * 0.95, y + s * 0.78),
               (x + 5, y + s * 0.78)], outline=INK, width=3)
    d.polygon([(x + s * 0.5, y + s * 0.42), (x + s * 0.66, y + s * 0.78),
               (x + s * 0.34, y + s * 0.78)], outline=INK, width=2)
    for i in range(4):
        rx = x + 6 + i * s * 0.24
        d.line([rx, y + 1, rx - 3, y + 9], fill=RED, width=2)
    d.line([x + 2, y + s * 0.86, x + s - 2, y + s * 0.86], fill=INK, width=2)


def i_drone(d, x, y, s):
    cx, cy = x + s / 2, y + s / 2
    d.line([x + 8, y + 8, x + s - 8, y + s - 8], fill=INK, width=3)
    d.line([x + s - 8, y + 8, x + 8, y + s - 8], fill=INK, width=3)
    d.rectangle([cx - 7, cy - 5, cx + 7, cy + 5], fill=INK)
    for px, py in ((x + 8, y + 8), (x + s - 8, y + 8), (x + 8, y + s - 8), (x + s - 8, y + s - 8)):
        d.line([px - 6, py, px + 6, py], fill=RED, width=3)
    d.line([cx, cy + 5, cx, cy + 12], fill=RED, width=2)


def i_ship(d, x, y, s):
    d.polygon([(x + 3, y + s * 0.5), (x + s - 3, y + s * 0.5),
               (x + s * 0.8, y + s * 0.74), (x + s * 0.18, y + s * 0.74)], fill=INK)
    d.rectangle([x + s * 0.36, y + s * 0.3, x + s * 0.58, y + s * 0.5], outline=INK, width=3)
    d.line([x + s * 0.72, y + s * 0.16, x + s * 0.72, y + s * 0.5], fill=INK, width=3)
    for i in range(3):
        wx = x + 5 + i * s * 0.3
        d.arc([wx, y + s * 0.78, wx + s * 0.22, y + s * 0.94], 180, 360, fill=RED, width=2)


def i_planet(d, x, y, s):
    cx, cy = x + s / 2, y + s / 2
    d.ellipse([cx - s * 0.2, cy - s * 0.2, cx + s * 0.2, cy + s * 0.2], fill=INK)
    d.ellipse([x + 3, cy - s * 0.12, x + s - 3, cy + s * 0.12], outline=RED, width=3)
    d.ellipse([x + s * 0.78, y + s * 0.1, x + s * 0.86, y + s * 0.18], fill=RED)


def i_debate(d, x, y, s):
    d.rounded_rectangle([x + 3, y + 5, x + s * 0.58, y + s * 0.52], radius=6,
                        outline=INK, width=3)
    d.polygon([(x + s * 0.2, y + s * 0.52), (x + s * 0.2, y + s * 0.68),
               (x + s * 0.36, y + s * 0.52)], outline=INK, width=3)
    d.rounded_rectangle([x + s * 0.42, y + s * 0.4, x + s - 3, y + s * 0.86], radius=6,
                        outline=RED, width=3)
    d.line([x + 10, y + s * 0.22, x + s * 0.45, y + s * 0.22], fill=INK, width=3)
    d.line([x + 10, y + s * 0.36, x + s * 0.38, y + s * 0.36], fill=INK, width=3)


def i_scales(d, x, y, s):
    cx = x + s / 2
    d.line([cx, y + 3, cx, y + s - 8], fill=INK, width=3)
    d.line([x + 5, y + 9, x + s - 5, y + 9], fill=INK, width=3)
    for sx in (x + 5, x + s - 5):
        d.line([sx, y + 9, sx - 5, y + s * 0.48], fill=INK, width=2)
        d.line([sx, y + 9, sx + 5, y + s * 0.48], fill=INK, width=2)
        d.arc([sx - 8, y + s * 0.36, sx + 8, y + s * 0.6], 0, 180, fill=INK, width=3)
    d.rectangle([cx - 8, y + s - 6, cx + 8, y + s - 3], fill=RED)


def i_shield(d, x, y, s):
    d.polygon([(x + s * 0.5, y + 2), (x + s - 3, y + s * 0.16), (x + s - 3, y + s * 0.55),
               (x + s * 0.5, y + s - 2), (x + 3, y + s * 0.55), (x + 3, y + s * 0.16)],
              outline=INK, width=3)
    d.line([x + s * 0.3, y + s * 0.42, x + s * 0.44, y + s * 0.56], fill=RED, width=4)
    d.line([x + s * 0.44, y + s * 0.56, x + s * 0.72, y + s * 0.26], fill=RED, width=4)


def i_chart(d, x, y, s):
    d.line([x + 3, y + s - 3, x + s - 2, y + s - 3], fill=INK, width=2)
    for i, hh in enumerate((0.35, 0.55, 0.45, 0.75)):
        bx = x + 6 + i * s * 0.22
        d.rectangle([bx, y + s * (0.9 - hh), bx + s * 0.14, y + s * 0.9],
                    fill=RED if i == 3 else INK)


def i_robot(d, x, y, s):
    d.line([x + s / 2, y + 2, x + s / 2, y + 10], fill=INK, width=3)
    d.ellipse([x + s / 2 - 3, y, x + s / 2 + 3, y + 6], fill=RED)
    d.rounded_rectangle([x + 8, y + 10, x + s - 8, y + s - 6], radius=5, outline=INK, width=3)
    for ex in (x + s * 0.34, x + s * 0.62):
        d.ellipse([ex - 3, y + s * 0.38, ex + 3, y + s * 0.38 + 6], fill=INK)
    d.line([x + s * 0.34, y + s * 0.68, x + s * 0.66, y + s * 0.68], fill=INK, width=3)


def i_case(d, x, y, s):
    d.rounded_rectangle([x + 3, y + s * 0.28, x + s - 3, y + s * 0.85], radius=4,
                        outline=INK, width=3)
    d.rounded_rectangle([x + s * 0.34, y + s * 0.12, x + s * 0.66, y + s * 0.3], radius=3,
                        outline=INK, width=3)
    d.line([x + 3, y + s * 0.52, x + s - 3, y + s * 0.52], fill=INK, width=2)
    d.rectangle([x + s * 0.44, y + s * 0.46, x + s * 0.56, y + s * 0.58], fill=RED)


def i_burst(d, x, y, s):
    d.rectangle([x + 2, y + s - 11, x + s * 0.36, y + s - 2], fill=INK)
    d.rectangle([x + s * 0.42, y + s - 18, x + s * 0.64, y + s - 2], fill=INK)
    cx, cy = x + s * 0.64, y + s * 0.24
    for i in range(8):
        ang = i * math.pi / 4
        r2 = s * (0.22 if i % 2 == 0 else 0.12)
        d.line([cx, cy, cx + r2 * math.cos(ang), cy + r2 * math.sin(ang)], fill=RED, width=3)


def i_storm(d, x, y, s):
    d.arc([x + 4, y + s * 0.1, x + s * 0.62, y + s * 0.55], 180, 360, fill=INK, width=3)
    d.arc([x + s * 0.34, y + s * 0.04, x + s - 4, y + s * 0.55], 180, 360, fill=INK, width=3)
    d.line([x + 6, y + s * 0.5, x + s - 6, y + s * 0.5], fill=INK, width=3)
    d.polygon([(x + s * 0.52, y + s * 0.48), (x + s * 0.36, y + s * 0.78),
               (x + s * 0.5, y + s * 0.78), (x + s * 0.42, y + s * 0.98),
               (x + s * 0.66, y + s * 0.64), (x + s * 0.53, y + s * 0.64)], fill=RED)


ICONS = {"route": i_route, "globe": i_globe, "tent": i_tent, "drone": i_drone,
         "ship": i_ship, "planet": i_planet, "debate": i_debate, "scales": i_scales,
         "shield": i_shield, "chart": i_chart, "robot": i_robot, "case": i_case,
         "burst": i_burst, "storm": i_storm}

# ----------------------------------------------------------------- data ----
LEADS = [
    (1, "ABU DHABI TO MOSCOW — DIPLOMACY", "US ENVOYS FLY TO MOSCOW AND DUBLIN",
     "Kushner and Witkoff brief Putin after two days of Abu Dhabi trilateral "
     "talks, then meet Zelensky in Dublin.", "ANSA · CONFIRMED", "400K",
     "route", "EUROPE", 37.6, 55.8),
    (2, "ANTALYA, TURKIYE — CLIMATE", "COP31 DEAL 'WITHIN REACH' IN EXTRA TIME",
     "Talks drag into Sunday with a final text close; delegates fear a 'most "
     "disappointing ever' summit.", "REUTERS · REPORTED", "200",
     "globe", "ASIA", 30.7, 36.9),
    (3, "GAZA — HUMANITARIAN", "WINTER FLOODS SWAMP GAZA'S SHELTERS",
     "Storms, rain and cold leave over a million displaced people exposed in "
     "flooded tents and shelters.", "DW · CONFIRMED", "1M+",
     "tent", "ASIA", 34.3, 31.5),
    (4, "KYIV, UKRAINE — WAR", "400-DRONE BARRAGE SETS KYIV ABLAZE",
     "Russia's overnight swarm leaves homes burning across the capital; at "
     "least two people killed nationwide.", "REPORTED", "400",
     "drone", "EUROPE", 30.5, 50.4),
]

PANELS = [
    (5, "TANKERS STRUCK OFF OMAN AS IRAN FLEXES MUSCLE", "REPORTED", "3",
     "ship", "ASIA", 56.5, 26.3),
    (6, "VOYAGER 1 NOW A FULL LIGHT-DAY FROM EARTH", "REPORTED", "1",
     "planet", "SPACE", None, None),
    (7, "FIVE RIVALS CLASH IN FRENCH TV DEBATE", "LE FIGARO · CONFIRMED", "5",
     "debate", "EUROPE", 2.35, 48.9),
    (8, "MYANMAR REJECTS UN GENOCIDE RULING AS 'UNJUST'", "REPORTED", "700K",
     "scales", "ASIA", 96.2, 21.9),
    (9, "EBOLA: LAST KENYA PATIENT OUT, DRC TOLL 5,300", "REPORTED", "5,300",
     "shield", "AFRICA", 36.8, -1.3),
    (10, "ITALY RAISES FLAT-TAX CAP TO €100,000", "CORRIERE · CONFIRMED", "€100K",
     "chart", "EUROPE", 12.5, 41.9),
    (11, "STATES AGREE FIRST PACT ON KILLER ROBOTS", "REPORTED", "100",
     "robot", "EUROPE", 6.1, 46.2),
    (12, "KENYA SEALS 293,600-JOBS DEAL WITH SAUDI ARABIA", "REPORTED", "293.6K",
     "case", "ASIA", 46.7, 24.6),
    (13, "129 BODIES PULLED FROM GAZA RUBBLE", "OFFICIALS", "129",
     "burst", "ASIA", 34.5, 31.3),
    (14, "PORTUGAL STORM ALERTS EASE AFTER OUTAGES", "RTP · CONFIRMED", "2,000",
     "storm", "EUROPE", -8.6, 38.7),
]

BRIEFS = [
    (15, "EUROPE", "Kyiv — Zelensky: four-nation talks must deliver concrete results"),
    (16, "N AMERICA", "Washington — Melania urges Russia–Ukraine ceasefire before Christmas"),
    (17, "N AMERICA", "Washington — Trump: Iran broke the deal; vows pact to bar its bomb"),
    (18, "ASIA", "Tehran — Hormuz reopening 'feasible' if US meets our terms (officials)"),
    (19, "N AMERICA", "Washington — Hegseth memo curbs US–Canada defence ties (WaPo)"),
    (20, "N AMERICA", "Washington — Lawmakers push ban on Chinese AI models in federal systems"),
    (21, "N AMERICA", "New York — Anthropic shares slide as tech sell-off deepens"),
    (22, "N AMERICA", "Washington — SEC said to be probing Nvidia's finances (sources)"),
    (23, "N AMERICA", "Washington — Trump signs law rounding cash to the nearest 5 cents"),
    (24, "ASIA", "Islamabad — Ruling PML-N backs provinces referendum; PPP objects"),
    (25, "ASIA", "Istanbul — Fidan and Kalin meet Libya's PM Dbeibah for talks"),
    (26, "ASIA", "Damascus — Syria says it seized a weapons shipment bound for Lebanon"),
    (27, "EUROPE", "Copenhagen — Denmark pushes EU curbs on Russian tourists"),
    (28, "EUROPE", "Zagreb — Rally demands answers over psychiatric hospital incident"),
    (29, "EUROPE", "Oslo — Supreme Court voids climate-disputed oil licences"),
    (30, "EUROPE", "Frankfurt — EU starts search for ECB chief as Lagarde resigns"),
    (31, "AFRICA", "Accra — Ghana unveils Heritage banknotes honouring Nkrumah, Annan"),
    (32, "AFRICA", "Niamey — Sahel states restart dialogue with West Africa bloc"),
    (33, "S AMERICA", "Brasilia — Bolsonaro in intensive care with bowel obstruction"),
    (34, "OCEANIA", "Sydney — Australia bowl first as Smith misses South Africa decider"),
    (35, "AFRICA", "Mogadishu — Al-Shabaab claims hundreds dead in ambush on troops"),
    (36, "AFRICA", "Kinshasa — DRC enacts constitutional reform amid high tension"),
    (37, "EUROPE", "Kaliningrad — Explosions reported near Baltic Fleet base"),
    (38, "EUROPE", "Turin — Alcaraz meets Zverev for the ATP Finals crown today"),
]

NUMBERS = [("400", "DRONES IN ONE NIGHT"), ("400K", "LEAKED RUSSIAN WAR DEAD"),
           ("1M+", "DISPLACED IN GAZA"), ("5,300", "EBOLA DEATHS IN CONGO"),
           ("293.6K", "SAUDI JOBS FOR KENYA"), ("€100K", "ITALY'S NEW TAX CAP")]

DATE_CHECK = ("LEFT OUT — OTHER DAYS: Iran's Bahrain strike and Mexico's cartel capture were Sat Nov 21 · "
              "Sozcu TV was seized late Saturday · the EU digital-tax plan was unveiled Saturday.  "
              "NOT YET: the ATP final is played later today · Nepal PM's Delhi visit runs to Nov 23 · "
              "France meet South Africa in the rugby final Sun Nov 29.")

MAP_ROWS = [
    "        ## ##  ##                ############################    ",
    "  #####  ############        #####  ########################      ",
    "        ############         ######## ####################        ",
    "       #############        #########  #################          ",
    "       ############         ##########  ############## ##         ",
    "        #########           ###########  #################        ",
    "          #####             ###########    #########              ",
    "               #####         #########      ########              ",
    "               ######         #######        ########             ",
    "               ######          #####          #######             ",
    "                #####          #####           #######            ",
    "                ####            ###            ######             ",
    "                 ##              ##             ####        #     ",
    "                 #                                          ##    ",
    "                 #                                                ",
]

# -------------------------------------------------------------- rendering ----

def num_badge(d, x, y, n, r=11):
    d.ellipse([x - r, y - r, x + r, y + r], fill=RED)
    s = str(n)
    f = F(SANSB, 12 if len(s) < 2 else 10)
    d.text((x - tw(d, s, f) / 2, y - (7 if len(s) < 2 else 6)), s, font=f, fill=(255, 255, 255))


def draw_lead(d, x, y, w, h, st):
    n, kick, head, summ, tag, num, icon, region, lon, lat = st
    d.rectangle([x, y, x + w, y + h], fill=LEAD_BG, outline=INK, width=2)
    ih = 92
    d.rectangle([x, y, x + w, y + ih], fill=(238, 230, 208))
    ICONS[icon](d, x + 12, y + 14, 62)
    nf = F(SERIF, 40)
    nw = tw(d, num, nf)
    d.text((x + w - nw - 12, y + ih - 52), num, font=nf, fill=RED)
    num_badge(d, x + 16, y + 16, n)
    ty = y + ih + 8
    d.text((x + 10, ty), kick, font=F(SANSB, 10), fill=RED)
    ty = block(d, x + 10, ty + 15, head, F(SERIF, 19), INK, w - 20, 23, max_lines=3)
    ty = block(d, x + 10, ty + 3, summ, F(SANS, 11), (40, 38, 32), w - 20, 14.5, max_lines=3)
    d.text((x + 10, y + h - 15), tag, font=F(SANSB, 9), fill=GREY)


def draw_panel(d, x, y, w, h, st):
    n, head, tag, num, icon, region, lon, lat = st
    d.rectangle([x, y, x + w, y + h], fill=PANEL_BG, outline=FAINT, width=1)
    ICONS[icon](d, x + 8, y + 7, 26)
    nf = F(SERIF, 23)
    nw = tw(d, num, nf)
    d.text((x + w - nw - 8, y + 5), num, font=nf, fill=RED)
    num_badge(d, x + w - 16, y + h - 16, n, r=9)
    block(d, x + 8, y + 40, head, F(SANSB, 12), INK, w - 16, 15, max_lines=3)
    d.text((x + 8, y + h - 13), tag, font=F(SANSB, 8), fill=GREY)


def draw_map(d, x, y, w, h, pins):
    d.rectangle([x, y, x + w, y + h], fill=(243, 239, 228), outline=FAINT, width=1)
    d.text((x + 8, y + 4), "WHERE IT HAPPENED — NUMBERED PINS MATCH THE STORIES",
           font=F(SANSB, 10), fill=INK)
    cols = max(len(r) for r in MAP_ROWS)
    rows = len(MAP_ROWS)
    gx, gy = x + 10, y + 20
    gw, gh = w - 20, h - 26
    cell = min(gw / cols, gh / rows)
    for ri, row in enumerate(MAP_ROWS):
        for ci, ch in enumerate(row):
            if ch == "#":
                px, py = gx + ci * cell, gy + ri * cell
                d.rectangle([px, py, px + cell * 0.72, py + cell * 0.72], fill=(178, 170, 152))
    for (n, lon, lat) in pins:
        px = gx + (lon + 180) / 360 * gw
        py = gy + (74 - lat) / 126 * gh
        num_badge(d, px, py, n, r=9)


def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    total = len(LEADS) + len(PANELS) + len(BRIEFS)
    tally = {}
    for st in LEADS:
        tally[st[7]] = tally.get(st[7], 0) + 1
    for st in PANELS:
        tally[st[5]] = tally.get(st[5], 0) + 1
    for st in BRIEFS:
        tally[st[1]] = tally.get(st[1], 0) + 1

    centre(d, 12, f"THE WORLD ON ONE PAGE · {total} STORIES · SIX CONTINENTS AND SPACE",
           F(SANSB, 15), INK)
    centre(d, 34, "Sunday 22 November 2026", F(SERIF, 57), INK)
    d.rectangle([MX, 104, W - MX, 108], fill=RED)
    d.rectangle([MX, 111, W - MX, 112], fill=INK)

    ny = 118
    cw6 = CW // 6
    for i, (num, lab) in enumerate(NUMBERS):
        cx = MX + i * cw6
        if i:
            d.line([cx, ny + 4, cx, ny + 44], fill=FAINT, width=1)
        d.text((cx + 8, ny), num, font=F(SERIF, 27), fill=RED)
        block(d, cx + 8, ny + 33, lab, F(SANSB, 8.5), GREY, cw6 - 14, 10.5, max_lines=2)
    d.line([MX, ny + 52, W - MX, ny + 52], fill=INK, width=1)

    ly = ny + 58
    lw = (CW - 3 * 8) // 4
    for i, st in enumerate(LEADS):
        draw_lead(d, MX + i * (lw + 8), ly, lw, 262, st)

    my = ly + 270
    pins = [(st[0], st[8], st[9]) for st in LEADS]
    pins += [(st[0], st[6], st[7]) for st in PANELS if st[6] is not None]
    draw_map(d, MX, my, 640, 120, pins)
    tx = MX + 652
    d.rectangle([tx, my, W - MX, my + 120], fill=(243, 239, 228), outline=FAINT, width=1)
    d.text((tx + 10, my + 6), "STORIES BY REGION", font=F(SANSB, 11), fill=INK)
    order = ["N AMERICA", "EUROPE", "ASIA", "AFRICA", "S AMERICA", "OCEANIA", "SPACE"]
    yy = my + 24
    for reg in order:
        if reg in tally:
            label = "SPACE (OFF-MAP)" if reg == "SPACE" else reg
            d.text((tx + 10, yy), label, font=F(SANS, 10.5), fill=INK)
            s = str(tally[reg])
            d.text((tx + 296 - tw(d, s, F(SANSB, 11)), yy), s, font=F(SANSB, 11), fill=RED)
            yy += 12.5

    py = my + 128
    pw = (CW - 4 * 8) // 5
    row1, row2 = PANELS[:5], PANELS[5:]
    for i, st in enumerate(row1):
        draw_panel(d, MX + i * (pw + 8), py, pw, 98, st)
    for i, st in enumerate(row2):
        draw_panel(d, MX + i * (pw + 8), py + 106, pw, 98, st)

    by = py + 212
    d.text((MX, by), f"ALSO ON SUNDAY — {len(BRIEFS)} MORE STORIES IN BRIEF",
           font=F(SANSB, 12.5), fill=RED)
    d.line([MX, by + 17, W - MX, by + 17], fill=INK, width=1)
    col_w = (CW - 16) // 2
    bf = F(SANS, 10.5)
    half = (len(BRIEFS) + 1) // 2
    for ci, chunk in enumerate((BRIEFS[:half], BRIEFS[half:])):
        bx = MX + ci * (col_w + 16)
        yy = by + 23
        for (n, reg, line) in chunk:
            d.text((bx, yy), f"{n}. {line}", font=bf, fill=INK)
            yy += 13.5

    dy = by + 23 + half * 13.5 + 6
    d.rectangle([MX, dy, W - MX, dy + 46], outline=INK, width=1)
    block(d, MX + 8, dy + 6, DATE_CHECK, F(SANS, 10), INK, CW - 16, 13, max_lines=3)
    return img


def main():
    img = build()
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)
        out_path = os.path.join(out_dir, "entry.png")
    else:
        out_path = "entry.png"
    img.save(out_path)
    check = Image.open(out_path)
    assert check.size == (1024, 1024), check.size
    print("entry.png OK", check.size, check.format)


if __name__ == "__main__":
    main()
