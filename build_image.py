#!/usr/bin/env python3
"""Render the news-image-20261125 v2 entry: one 1024x1024 PNG summing up
Wednesday 25 November 2026. Flat editorial illustration, PIL shapes only.
Written fresh for this entry."""
import os, random
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (248, 244, 234)
INK = (25, 25, 25)
MUTED = (90, 86, 72)
LINE = (216, 210, 192)
RED = (179, 38, 30)
NAVY = (30, 58, 95)
GOLD = (166, 124, 0)
GREEN = (46, 125, 50)
TEAL = (15, 118, 110)
BLUE = (37, 99, 235)
ORANGE = (194, 65, 12)
PURPLE = (107, 33, 168)
PINK = (190, 24, 93)
DARKGREEN = (21, 128, 61)
SKY = (3, 105, 161)
CREAM = (255, 251, 235)

FD = "/usr/share/fonts/truetype/dejavu"
def F(name, size):
    return ImageFont.truetype(os.path.join(FD, name), size)
SERIF_B = lambda s: F("DejaVuSerif-Bold.ttf", s)
SERIF = lambda s: F("DejaVuSerif.ttf", s)
SANS_B = lambda s: F("DejaVuSans-Bold.ttf", s)
SANS = lambda s: F("DejaVuSans.ttf", s)

def wrap(draw, text, font, max_w):
    words, lines, cur = text.split(), [], ""
    for wd in words:
        t = (cur + " " + wd).strip()
        if draw.textlength(t, font=font) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = wd
    if cur:
        lines.append(cur)
    return lines

def trunc(draw, text, font, max_w):
    if draw.textlength(text, font=font) <= max_w:
        return text
    while text and draw.textlength(text + "...", font=font) > max_w:
        text = text[:-1]
    return text + "..."

BADGE_FILL = {"OFFICIAL": GREEN, "CONFIRMED": NAVY, "REPORTED": (120, 113, 96)}
def badge(d, x, y, kind, font=None):
    f = font or SANS_B(9)
    w = int(d.textlength(kind, font=f)) + 12
    d.rounded_rectangle([x, y, x + w, y + 14], radius=7, fill=BADGE_FILL[kind])
    d.text((x + 6, y + 2), kind, font=f, fill=(255, 255, 255))
    return w

REGION_COLOR = {
    "North America": BLUE, "South America": TEAL, "Europe": PURPLE,
    "Middle East": RED, "Africa": ORANGE, "South Asia": GOLD,
    "East Asia": PINK, "Southeast Asia": DARKGREEN, "Oceania": SKY,
    "Global": MUTED,
}

UTC = [
    ("00:18", "Shenzhou-24 lifts off from Jiuquan"),
    ("03:56", "Shenzhou-24 docks at Tiangong station"),
    ("06:00", "Nikkei closes -2.78% at 57,011"),
    ("06:30", "Kospi closes -6.2% at 4,697"),
    ("13:30", "US Q3 GDP +4.3%; core PCE out"),
    ("17:55", "FCC clears SpaceX Starmind plan"),
    ("21:00", "Wall St closes: Dow +0.33%"),
]
NUMBERS = [
    ("14", "TRADING PARTNERS HIT BY NEW US TARIFFS"),
    ("-6.2%", "KOSPI'S FALL AS ASIAN CHIPS ROUT"),
    ("31", "KILLED IN THE GIZA TANKER FIRE"),
    ("1,000,000", "SPACEX SATELLITES CLEARED BY FCC"),
    ("490,334", "RUSSIAN SOLDIERS DEAD, BBC LEAK SHOWS"),
    ("+36%", "BANGLADESH GARMENT WAGE RISE"),
]

LEADS = [
    dict(banner="20-40%", bcol=RED, scene="tariffs",
         title="TRUMP HITS 14 PARTNERS WITH NEW TARIFFS",
         body="USTR proposes duties after an 8-month probe; China capped at 20%, 40% if the truce fails. Hearing set for Jan 25.",
         badge="OFFICIAL"),
    dict(banner="-6.2%", bcol=NAVY, scene="chips",
         title="CHIP ROUT SWEEPS ASIA",
         body="Kospi -6.2%, Taiex -4.8%, Nikkei -2.78% as AI doubts return. Samsung -9.9%, SK Hynix -11.1%, SoftBank -14.8%.",
         badge="CONFIRMED"),
    dict(banner="31 KILLED", bcol=ORANGE, scene="tanker",
         title="TANKER FIRE KILLS 31 NEAR CAIRO",
         body="A fuel tanker overturned on Cairo's Ring Road at Warraq, Giza, and burst into flames. 31 killed, 21 hurt; 27 cars and motorcycles burned.",
         badge="OFFICIAL"),
]

TILES = [
    dict(title="PAKISTAN'S FIRST ASTRONAUT", fact="Shenzhou-24 docks; Ali aboard",
         badge="OFFICIAL", scene="rocket", bg=(16, 42, 67)),
    dict(title="TWO TANKERS HIT IN HORMUZ", fact="IRGC: mines hit two vessels",
         badge="CONFIRMED", scene="hormuz", bg=(12, 74, 110)),
    dict(title="DOW'S 1,100-POINT COMEBACK", fact="Dow +0.33% to 50,182.95; S&P -0.25%",
         badge="CONFIRMED", scene="dow", bg=(240, 238, 228)),
    dict(title="FCC CLEARS 1M SPACE SATELLITES", fact="SpaceX Starmind: first satellite by 2033",
         badge="OFFICIAL", scene="spacex", bg=(10, 20, 40)),
    dict(title="HUAWEI FOUND GUILTY IN US", fact="Trade-secret conspiracy, bank fraud",
         badge="CONFIRMED", scene="court", bg=(232, 228, 214)),
    dict(title="BANGLADESH WAGE UP 36%", fact="Garment floor now 17,000 taka a month",
         badge="CONFIRMED", scene="garment", bg=(146, 64, 14)),
    dict(title="SOLOMONS SAY NO TO BASES", fact="Australia pact; A$740M over 10 years",
         badge="OFFICIAL", scene="island", bg=(14, 116, 144)),
    dict(title="RSF DRONES KILL 19 IN SUDAN", fact="Damazin homes hit; 20 more wounded",
         badge="CONFIRMED", scene="drone", bg=(120, 53, 15)),
    dict(title="26 MINERS TRAPPED IN BOGOR", fact="Flooded illegal gold mine; 3 bodies found",
         badge="CONFIRMED", scene="mine", bg=(68, 64, 60)),
    dict(title="EUROSTAR STRIKE AXES 8 TRAINS", fact="Paris-London hit; 4 in 5 trains still run",
         badge="CONFIRMED", scene="train", bg=(30, 58, 95)),
]

# (region, headline, fact, badge)
INDEX = [
    ("Middle East", "RAS TANURA REFINERY HIT", "Houthis claim strike; Brent +2.4% to $93.60", "CONFIRMED"),
    ("Middle East", "ISRAEL KILLS HAMAS COLONEL", "Abuelouf, wife and two children dead in Gaza", "CONFIRMED"),
    ("Europe", "RUSSIA HITS ODESA, 2 KILLED", "Child hurt; Kyiv apartment block ablaze", "CONFIRMED"),
    ("Europe", "490,334 RUSSIAN SOLDIERS DEAD", "Leaked figures analysed by the BBC", "REPORTED"),
    ("Europe", "PUTIN: STRIKES ON REFINERIES GO ON", "Despite Trump's plea to stop, he says", "CONFIRMED"),
    ("Middle East", "LIBYA VOWS RETALIATION", "After Ukraine hit a Russian ship off Benghazi", "REPORTED"),
    ("Middle East", "EVACUATE HODEIDAH, COALITION SAYS", "Port residents told to leave as strikes go on", "CONFIRMED"),
    ("Middle East", "GAZA CHILDREN'S HOSPITAL DARK", "Power outage disrupts medical services", "REPORTED"),
    ("Global", "POPE LAMENTS COP31 FAILURE", "Climate extremes 'more frequent', Leo XIV says", "OFFICIAL"),
    ("Global", "UN CHIEF: AI IS CHANGING WAR", "Calls for curbs on autonomous weapons", "OFFICIAL"),
    ("North America", "CIA, ODNI HIT BY CYBER BREACH", "Some unclassified data taken, source says", "REPORTED"),
    ("North America", "TRUMP FLOATS STAKE IN NVIDIA", "Calls chipmaker vital to AI leadership", "REPORTED"),
    ("North America", "US BLACKLISTS MEGASPEED", "In Nvidia chip probe, Washington acts", "REPORTED"),
    ("North America", "MELANIA REUNITES 9 CHILDREN", "9 kids back with their families", "REPORTED"),
    ("North America", "US GDP REVISED UP TO +4.3%", "Q3 second estimate; core PCE +0.3% m/m", "OFFICIAL"),
    ("North America", "DEERE PROFIT FALLS", "Farm equipment sales sag; shares slide", "CONFIRMED"),
    ("Global", "SHEIN PROFIT RISES", "Despite lower revenue, trade shift pays off", "CONFIRMED"),
    ("North America", "'EL CHAPO ISIDRO' CAPTURED", "Mexico used US drones in the arrest", "REPORTED"),
    ("South America", "ECUADOR, US WEIGH JOINT OPS", "Talks on bilateral military activities", "REPORTED"),
    ("South America", "BRAZIL HIT HARDER ON TARIFFS", "Sugar duties up; 10% on Embraer jets", "CONFIRMED"),
    ("Europe", "BBC JOURNALISTS GO ON STRIKE", "Over staff cuts and rising workloads", "REPORTED"),
    ("Europe", "POLAND PLANS EASTERN NO-FLY ZONE", "To harden NATO's flank, Warsaw says", "REPORTED"),
    ("Europe", "FRANCE TO PUTIN: DROP DELUSION", "Paris denounces 'colonial' ambitions", "REPORTED"),
    ("Europe", "PUIGDEMONT TO RETURN DEC 12", "Catalan leader renews independence push", "REPORTED"),
    ("Europe", "DECATHLON BREACH HITS 130,000", "Customer data exposed in cyberattack", "REPORTED"),
    ("East Asia", "JAPAN EYES NO. 3 AI SPOT", "Aims to rank behind US and China only", "REPORTED"),
    ("East Asia", "SEOUL WATCHES N. KOREAN BOAT", "'Coast guard' vessel spotted near NLL", "REPORTED"),
    ("East Asia", "CHINA EXECUTES LEAK OFFICIAL", "Death sentence for 100+ state secrets", "REPORTED"),
    ("Southeast Asia", "MALAYSIA SUES GOOGLE $150M", "Over YouTube content, regulator says", "CONFIRMED"),
    ("Europe", "FRAGRANCE GIANTS FINED $630M", "EU, UK antitrust ruling on price fixing", "OFFICIAL"),
    ("Europe", "EASYJET PROFIT SLUMPS", "Ahead of Apollo takeover, fuel costs bite", "CONFIRMED"),
    ("Europe", "NESTLE EYES WEARABLE TECH", "To match consumers with nutrition", "REPORTED"),
    ("North America", "LAKERS BEAT JAZZ", "Doncic 28 points, 8 assists in payback win", "CONFIRMED"),
    ("Europe", "MOSCOW'S BIGGEST ARMS BUDGET", "Largest military spend since Soviet era", "REPORTED"),
    ("Europe", "ZELENSKYY TO APPEAL TO CONGRESS", "If no Ukraine peace deal by year-end", "REPORTED"),
    ("Europe", "EU TEAM JOINS PEACE TALKS", "'Strong European team' in next round", "REPORTED"),
    ("Africa", "EGYPT BUS CRASH KILLS 10", "Bus-truck collision in the south", "REPORTED"),
]
assert len(INDEX) == 37, len(INDEX)
assert len(LEADS) + len(TILES) + len(INDEX) == 50

# ---------- flat-illustration scenes (each draws inside box x,y,w,h) ----------
def sun(d, x, y, r, col=(255, 214, 64)):
    d.ellipse([x - r, y - r, x + r, y + r], fill=col)
    for a in range(0, 360, 45):
        import math
        x2, y2 = x + int((r + 7) * math.cos(math.radians(a))), y + int((r + 7) * math.sin(math.radians(a)))
        x3, y3 = x + int((r + 13) * math.cos(math.radians(a))), y + int((r + 13) * math.sin(math.radians(a)))
        d.line([x2, y2, x3, y3], fill=col, width=3)

def flame(d, cx, base, w, h, cols=((255, 122, 26), (255, 190, 0), (255, 240, 120))):
    d.polygon([(cx - w, base), (cx - w * 0.55, base - h * 0.55), (cx - w * 0.2, base - h),
               (cx + w * 0.25, base - h * 0.6), (cx + w, base)], fill=cols[0])
    d.polygon([(cx - w * 0.55, base), (cx - w * 0.25, base - h * 0.45), (cx + w * 0.1, base - h * 0.6),
               (cx + w * 0.5, base)], fill=cols[1])
    d.polygon([(cx - w * 0.25, base), (cx, base - h * 0.35), (cx + w * 0.25, base)], fill=cols[2])

def chart_down(d, x, y, w, h, col=RED, lw=4):
    pts = [(x, y + h * 0.15), (x + w * 0.25, y + h * 0.3), (x + w * 0.45, y + h * 0.25),
           (x + w * 0.65, y + h * 0.6), (x + w * 0.85, y + h * 0.8), (x + w, y + h * 0.95)]
    d.line(pts, fill=col, width=lw, joint="curve")
    d.polygon([(x + w - 14, y + h * 0.95 - 2), (x + w, y + h * 0.95), (x + w - 2, y + h * 0.95 - 14)], fill=col)

def scene_tariffs(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(30, 58, 95))
    d.rectangle([x, y + h - 26, x + w, y + h], fill=(20, 40, 66))
    cols = [(179, 38, 30), (46, 125, 50), (255, 190, 0), (37, 99, 235), (194, 65, 12)]
    cw, ch = 52, 34
    for i, c in enumerate(cols):
        cx = x + 12 + i * 56
        d.rectangle([cx, y + h - 26 - ch, cx + cw, y + h - 26], fill=c, outline=(255, 255, 255), width=2)
        for k in range(3):
            d.line([cx + 8, y + h - 26 - ch + 10 + k * 9, cx + cw - 8, y + h - 26 - ch + 10 + k * 9], fill=(255, 255, 255), width=1)
    d.line([x + 8, y + 12, x + 8, y + h - 60], fill=(255, 214, 64), width=4)
    d.line([x + 8, y + 12, x + 60, y + 12], fill=(255, 214, 64), width=4)
    d.line([x + 60, y + 12, x + 60, y + 26], fill=(255, 214, 64), width=3)
    d.rectangle([x + 52, y + 26, x + 68, y + 40], outline=(255, 214, 64), width=2)
    d.ellipse([x + w - 52, y + 8, x + w - 8, y + 52], outline=(255, 255, 255), width=2)
    d.text((x + w - 44, y + 20), "%", font=SANS_B(22), fill=(255, 255, 255))

def scene_chips(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(24, 24, 32))
    for i, (cx, top, bot, col) in enumerate([
            (x + 30, 0.25, 0.55, (220, 60, 50)), (x + 70, 0.2, 0.5, (220, 60, 50)),
            (x + 110, 0.35, 0.6, (220, 60, 50)), (x + 150, 0.3, 0.65, (220, 60, 50)),
            (x + 190, 0.45, 0.75, (220, 60, 50)), (x + 230, 0.4, 0.7, (220, 60, 50))]):
        d.line([cx, y + h * top - 6, cx, y + h * bot + 6], fill=col, width=2)
        d.rectangle([cx - 9, y + h * top, cx + 9, y + h * bot], fill=col)
    chart_down(d, x + 10, y + 6, w - 20, h - 16, col=(255, 190, 0), lw=3)
    d.rectangle([x + w - 78, y + h - 34, x + w - 30, y + h - 10], fill=(60, 60, 80), outline=(255, 214, 64), width=2)
    for k in range(3):
        d.line([x + w - 78, y + h - 30 + k * 8, x + w - 86, y + h - 30 + k * 8], fill=(255, 214, 64), width=2)
        d.line([x + w - 30, y + h - 30 + k * 8, x + w - 22, y + h - 30 + k * 8], fill=(255, 214, 64), width=2)

def scene_tanker(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(64, 28, 16))
    d.ellipse([x + w - 34, y + 6, x + w - 14, y + 26], fill=(255, 190, 0))
    d.rectangle([x, y + h - 30, x + w, y + h], fill=(40, 40, 40))
    for i in range(7):
        d.line([x + 10 + i * 42, y + h - 15, x + 30 + i * 42, y + h - 15], fill=(255, 214, 64), width=3)
    d.rounded_rectangle([x + 30, y + 58, x + 210, y + 88], radius=14, fill=(200, 200, 200), outline=(120, 120, 120), width=2)
    d.rectangle([x + 214, y + 62, x + 252, y + 88], fill=(179, 38, 30))
    d.ellipse([x + 62, y + 88, x + 84, y + 104], fill=(20, 20, 20))
    d.ellipse([x + 216, y + 88, x + 238, y + 104], fill=(20, 20, 20))
    flame(d, x + 120, y + 62, 34, 46)
    flame(d, x + 190, y + 60, 26, 36)
    for (sx, sy, sr) in [(x + 90, y + 22, 10), (x + 130, y + 12, 13), (x + 170, y + 20, 9)]:
        d.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(120, 120, 120))

def scene_rocket(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(16, 42, 67))
    for (sx, sy) in [(x + 14, y + 8), (x + 60, y + 16), (x + 150, y + 6), (x + 178, y + 20), (x + 100, y + 12)]:
        d.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=(255, 255, 255))
    d.polygon([(x + 78, y + 6), (x + 94, y + 6), (x + 86, y - 6)], fill=(255, 255, 255))
    d.rectangle([x + 78, y + 6, x + 94, y + 34], fill=(240, 240, 240))
    d.polygon([(x + 78, y + 34), (x + 70, y + 44), (x + 78, y + 40)], fill=(179, 38, 30))
    d.polygon([(x + 94, y + 34), (x + 102, y + 44), (x + 94, y + 40)], fill=(179, 38, 30))
    d.ellipse([x + 81, y + 14, x + 91, y + 24], fill=(3, 105, 161), outline=(255, 255, 255), width=1)
    flame(d, x + 86, y + 44, 8, 12)
    d.ellipse([x - 40, y + h - 14, x + w + 40, y + h + 30], fill=(46, 125, 50))
    d.ellipse([x + 130, y + 18, x + 170, y + 44], outline=(255, 214, 64), width=2)
    d.rectangle([x + 138, y + 28, x + 162, y + 34], fill=(255, 214, 64))

def scene_hormuz(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(12, 74, 110))
    for i in range(4):
        d.arc([x + 6 + i * 48, y + h - 16, x + 46 + i * 48, y + h + 8], 180, 360, fill=(255, 255, 255), width=2)
    d.rounded_rectangle([x + 18, y + 22, x + 120, y + 38], radius=6, fill=(40, 40, 40))
    d.rectangle([x + 52, y + 12, x + 62, y + 22], fill=(40, 40, 40))
    d.ellipse([x + 140, y + 18, x + 158, y + 36], fill=(20, 20, 20))
    for a in range(0, 360, 45):
        import math
        d.line([x + 149 + int(9 * math.cos(math.radians(a))), y + 27 + int(9 * math.sin(math.radians(a))),
                x + 149 + int(14 * math.cos(math.radians(a))), y + 27 + int(14 * math.sin(math.radians(a)))], fill=(20, 20, 20), width=2)
    flame(d, x + 90, y + 24, 16, 22)
    flame(d, x + 150, y + 20, 12, 16)

def scene_dow(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(240, 238, 228))
    for i in range(5):
        d.line([x + 8, y + 8 + i * 9, x + w - 8, y + 8 + i * 9], fill=(220, 216, 200), width=1)
    pts = [(x + 8, y + 14), (x + 50, y + 26), (x + 90, y + 20), (x + 130, y + 38), (x + 160, y + 44), (x + 182, y + 12)]
    d.line(pts, fill=(46, 125, 50), width=4, joint="curve")
    d.polygon([(x + 182 - 12, y + 12 - 2), (x + 182, y + 12), (x + 182 - 2, y + 12 + 12)], fill=(46, 125, 50))
    d.text((x + 10, y + h - 16), "50,182.95", font=SANS_B(11), fill=(46, 125, 50))

def scene_spacex(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(10, 20, 40))
    for (sx, sy) in [(x + 16, y + 8), (x + 60, y + 14), (x + 110, y + 6), (x + 160, y + 12), (x + 40, y + 26), (x + 130, y + 24)]:
        d.ellipse([sx - 1, sy - 1, sx + 1, sy + 1], fill=(255, 255, 255))
    for (sx, sy) in [(x + 30, y + 34), (x + 80, y + 30), (x + 130, y + 36), (x + 170, y + 30)]:
        d.rectangle([sx - 5, sy - 2, sx + 5, sy + 2], fill=(255, 214, 64))
        d.rectangle([sx - 2, sy - 5, sx + 2, sy + 5], fill=(255, 214, 64))
    d.ellipse([x - 50, y + h - 12, x + w + 50, y + h + 44], fill=(30, 90, 160))
    d.arc([x - 50, y + h - 12, x + w + 50, y + h + 44], 180, 360, fill=(120, 200, 255), width=2)

def scene_court(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(232, 228, 214))
    d.polygon([(x + 20, y + 8), (x + w - 20, y + 8), (x + w // 2, y + 22)], fill=(30, 58, 95))
    for i in range(4):
        cx = x + 32 + i * 44
        d.rectangle([cx, y + 24, cx + 12, y + 44], fill=(255, 255, 255), outline=(30, 58, 95), width=1)
    d.rectangle([x + 16, y + 44, x + w - 16, y + 48], fill=(30, 58, 95))
    d.rectangle([x + 70, y + 16, x + 120, y + 22], fill=(120, 72, 20))
    d.rectangle([x + 92, y + 8, x + 98, y + 18], fill=(120, 72, 20))

def scene_garment(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(146, 64, 14))
    d.rectangle([x + 14, y + 18, x + 96, y + 44], fill=(255, 251, 235))
    d.polygon([(x + 14, y + 18), (x + 30, y + 8), (x + 96, y + 8), (x + 96, y + 18)], fill=(179, 38, 30))
    for i in range(3):
        d.rectangle([x + 24 + i * 22, y + 26, x + 34 + i * 22, y + 38], fill=(3, 105, 161))
    d.rectangle([x + 116, y + 14, x + 172, y + 40], fill=(37, 99, 235))
    d.rectangle([x + 116, y + 14, x + 130, y + 40], fill=(255, 255, 255))
    d.line([x + 130, y + 27, x + 172, y + 27], fill=(255, 255, 255), width=2)
    d.ellipse([x + 150, y + 42, x + 158, y + 48], fill=(255, 214, 64))

def scene_island(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(14, 116, 144))
    for i in range(3):
        d.arc([x + 8 + i * 60, y + h - 14, x + 48 + i * 60, y + h + 10], 180, 360, fill=(255, 255, 255), width=2)
    d.ellipse([x + 30, y + 26, x + 160, y + 52], fill=(232, 205, 140))
    d.line([x + 52, y + 30, x + 52, y + 12], fill=(120, 72, 20), width=3)
    d.line([x + 52, y + 30, x + 40, y + 20], fill=(120, 72, 20), width=2)
    d.line([x + 52, y + 30, x + 64, y + 20], fill=(120, 72, 20), width=2)
    d.polygon([(x + 110, y + 12), (x + 110, y + 30), (x + 150, y + 21)], fill=(0, 122, 51))
    d.polygon([(x + 110, y + 12), (x + 110, y + 21), (x + 150, y + 21)], fill=(255, 214, 64))
    d.polygon([(x + 110, y + 21), (x + 110, y + 30), (x + 150, y + 21)], fill=(30, 58, 95))
    d.ellipse([x + 118, y + 16, x + 124, y + 22], fill=(255, 255, 255))

def scene_drone(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(120, 53, 15))
    for i in range(3):
        hx = x + 16 + i * 56
        d.rectangle([hx, y + 26, hx + 40, y + 46], fill=(232, 205, 140))
        d.polygon([(hx, y + 26), (hx + 8, y + 18), (hx + 32, y + 18), (hx + 40, y + 26)], fill=(179, 38, 30))
    cx, cy = x + 150, y + 14
    d.rectangle([cx - 12, cy - 4, cx + 12, cy + 4], fill=(40, 40, 40))
    for (ox, oy) in [(-16, -8), (16, -8), (-16, 8), (16, 8)]:
        d.line([cx, cy, cx + ox, cy + oy], fill=(40, 40, 40), width=2)
        d.ellipse([cx + ox - 5, cy + oy - 2, cx + ox + 5, cy + oy + 2], fill=(200, 200, 200))
    d.ellipse([x + 130, y + 30, x + 146, y + 42], fill=(120, 120, 120))

def scene_mine(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(68, 64, 60))
    d.ellipse([x + 30, y + 8, x + 130, y + 46], fill=(40, 30, 20))
    d.ellipse([x + 44, y + 14, x + 116, y + 40], fill=(10, 10, 10))
    d.rectangle([x + 140, y + 18, x + 176, y + 34], fill=(255, 214, 64))
    d.rectangle([x + 140, y + 34, x + 176, y + 38], fill=(179, 38, 30))
    for i in range(3):
        d.arc([x + 10 + i * 56, y + h - 12, x + 50 + i * 56, y + h + 8], 180, 360, fill=(3, 105, 161), width=3)
    d.line([x + 60, y + 6, x + 60, y + 14], fill=(255, 255, 255), width=2)

def scene_train(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(30, 58, 95))
    d.ellipse([x + 10, y + 8, x + 180, y + 48], fill=(60, 60, 70))
    d.rounded_rectangle([x + 56, y + 12, x + 134, y + 46], radius=10, fill=(255, 214, 64))
    d.rectangle([x + 66, y + 18, x + 86, y + 30], fill=(20, 40, 66))
    d.rectangle([x + 104, y + 18, x + 124, y + 30], fill=(20, 40, 66))
    d.ellipse([x + 90, y + 34, x + 100, y + 40], fill=(179, 38, 30))
    d.polygon([(x + 162, y + 12), (x + 178, y + 40), (x + 146, y + 40)], fill=(255, 214, 64), outline=(179, 38, 30))
    d.text((x + 159, y + 26), "!", font=SANS_B(12), fill=(179, 38, 30), anchor="mm")

SCENES = {
    "tariffs": scene_tariffs, "chips": scene_chips, "tanker": scene_tanker,
    "rocket": scene_rocket, "hormuz": scene_hormuz, "dow": scene_dow,
    "spacex": scene_spacex, "court": scene_court, "garment": scene_garment,
    "island": scene_island, "drone": scene_drone, "mine": scene_mine,
    "train": scene_train,
}

# ---------- layout ----------
def build(path):
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    MX = 24

    def draw_scene(fn, x, y, w, h):
        """Draw a scene clipped to its own box (no overflow into text)."""
        tmp = Image.new("RGB", (w, h), PAPER)
        td = ImageDraw.Draw(tmp)
        fn(td, 0, 0, w, h)
        img.paste(tmp, (x, y))

    # top rules
    d.rectangle([0, 0, W, 5], fill=RED)
    d.rectangle([0, 8, W, 10], fill=INK)

    # masthead
    f_date = SERIF_B(34)
    d.text((W // 2, 16), "WEDNESDAY 25 NOVEMBER 2026", font=f_date, fill=INK, anchor="ma")
    d.text((W // 2, 56), "O N E   D A Y   O F   W O R L D   N E W S ,   O N E   P I C T U R E",
           font=SANS_B(12), fill=RED, anchor="ma")
    d.text((W // 2, 76), "50 STORIES  ·  10 REGIONS  ·  21 FIELDS  ·  EVERY ONE FROM THIS WEDNESDAY",
           font=SANS_B(12), fill=INK, anchor="ma")
    d.line([MX, 96, W - MX, 96], fill=INK, width=2)

    # UTC strip
    d.text((MX, 104), "THE DAY IN UTC", font=SANS_B(11), fill=RED)
    d.text((W - MX, 104), "ALL TIMES UTC", font=SANS(10), fill=MUTED, anchor="ra")
    cw = (W - 2 * MX - 6 * 8) / 7
    for i, (t, ev) in enumerate(UTC):
        x0 = MX + i * (cw + 8)
        d.text((x0, 120), t, font=SANS_B(13), fill=RED)
        for j, ln in enumerate(wrap(d, ev, SANS(10), cw)):
            d.text((x0, 136 + j * 12), ln, font=SANS(10), fill=INK)
    d.line([MX, 166, W - MX, 166], fill=LINE, width=1)

    # numbers strip
    d.text((MX, 172), "THE DAY IN NUMBERS", font=SANS_B(11), fill=RED)
    nw = (W - 2 * MX - 5 * 10) / 6
    for i, (num, lab) in enumerate(NUMBERS):
        x0 = MX + i * (nw + 10)
        d.text((x0, 188), num, font=SANS_B(20), fill=NAVY)
        for j, ln in enumerate(wrap(d, lab, SANS_B(8), nw)):
            d.text((x0, 212 + j * 10), ln, font=SANS_B(8), fill=MUTED)
    d.line([MX, 236, W - MX, 236], fill=INK, width=2)

    # leads
    lw = 304
    for i, L in enumerate(LEADS):
        x0 = MX + i * (lw + 32)
        y0 = 246
        d.rectangle([x0, y0, x0 + lw, y0 + 26], fill=L["bcol"])
        d.text((x0 + 10, y0 + 3), L["banner"], font=SANS_B(17), fill=(255, 255, 255))
        d.text((x0 + lw - 8, y0 + 7), "LEAD " + str(i + 1), font=SANS_B(9), fill=(255, 255, 255), anchor="ra")
        draw_scene(SCENES[L["scene"]], x0, y0 + 26, lw, 108)
        d.rectangle([x0, y0 + 26, x0 + lw, y0 + 134], outline=LINE, width=1)
        ty = y0 + 140
        for j, ln in enumerate(wrap(d, L["title"], SERIF_B(15), lw - 4)):
            d.text((x0 + 2, ty + j * 18), ln, font=SERIF_B(15), fill=INK)
        by = ty + 18 * len(wrap(d, L["title"], SERIF_B(15), lw - 4)) + 2
        for j, ln in enumerate(wrap(d, L["body"], SANS(11), lw - 4)):
            d.text((x0 + 2, by + j * 13), ln, font=SANS(11), fill=(60, 58, 48))
        badge(d, x0 + 2, y0 + 234, L["badge"])

    # tiles
    tw, th = 190, 106
    for r in range(2):
        for c in range(5):
            T = TILES[r * 5 + c]
            x0 = MX + c * (tw + 8)
            y0 = 500 + r * (th + 8)
            draw_scene(SCENES[T["scene"]], x0, y0, tw, 50)
            d.rectangle([x0, y0, x0 + tw, y0 + 50], outline=LINE, width=1)
            ty = y0 + 54
            for j, ln in enumerate(wrap(d, T["title"], SANS_B(10), tw - 2)):
                d.text((x0 + 1, ty + j * 12), ln, font=SANS_B(10), fill=INK)
            fy = ty + 12 * len(wrap(d, T["title"], SANS_B(10), tw - 2)) + 1
            d.text((x0 + 1, fy), trunc(d, T["fact"], SANS(9), tw - 2), font=SANS(9), fill=MUTED)
            badge(d, x0 + 1, y0 + th - 15, T["badge"])

    # bottom band
    yb = 726
    d.line([MX, yb - 6, W - MX, yb - 6], fill=INK, width=2)
    # --- world map (left column) ---
    map_x, map_w = MX, 306
    d.text((map_x, yb), "WHERE IT HAPPENED", font=SANS_B(11), fill=RED)
    mx0, my0, mw, mh = map_x, yb + 18, map_w, 148
    d.rectangle([mx0, my0, mx0 + mw, my0 + mh], fill=(238, 232, 214), outline=LINE, width=1)
    for gx in range(0, mw, 12):
        for gy in range(0, mh, 12):
            d.ellipse([mx0 + gx + 4, my0 + gy + 4, mx0 + gx + 7, my0 + gy + 7], fill=(210, 202, 178))
    # rough continent blobs
    d.polygon([(mx0 + 18, my0 + 30), (mx0 + 60, my0 + 18), (mx0 + 96, my0 + 26), (mx0 + 88, my0 + 52),
               (mx0 + 60, my0 + 62), (mx0 + 30, my0 + 52)], fill=(200, 190, 150))
    d.polygon([(mx0 + 96, my0 + 78), (mx0 + 118, my0 + 72), (mx0 + 130, my0 + 96), (mx0 + 112, my0 + 122),
               (mx0 + 98, my0 + 100)], fill=(200, 190, 150))
    d.polygon([(mx0 + 150, my0 + 34), (mx0 + 178, my0 + 26), (mx0 + 196, my0 + 40), (mx0 + 182, my0 + 58),
               (mx0 + 158, my0 + 52)], fill=(200, 190, 150))
    d.polygon([(mx0 + 150, my0 + 62), (mx0 + 190, my0 + 56), (mx0 + 208, my0 + 78), (mx0 + 196, my0 + 108),
               (mx0 + 168, my0 + 112), (mx0 + 152, my0 + 88)], fill=(200, 190, 150))
    d.polygon([(mx0 + 210, my0 + 30), (mx0 + 260, my0 + 22), (mx0 + 292, my0 + 40), (mx0 + 280, my0 + 66),
               (mx0 + 240, my0 + 62), (mx0 + 214, my0 + 48)], fill=(200, 190, 150))
    d.polygon([(mx0 + 252, my0 + 108), (mx0 + 282, my0 + 104), (mx0 + 292, my0 + 120), (mx0 + 268, my0 + 130),
               (mx0 + 250, my0 + 122)], fill=(200, 190, 150))
    pins = [("Washington", -77, 39, 0, 0), ("Tokyo", 139, 35, 6, -4), ("Seoul", 127, 37, -4, 8),
            ("Cairo", 31, 30, -8, -5), ("Jiuquan", 98, 40, 4, -3), ("Ras Tanura", 50, 26, 8, -2),
            ("Hodeidah", 43, 15, -4, 6), ("Canberra", 149, -35, 0, 0)]
    for i, (name, lon, lat, dx, dy) in enumerate(pins, 1):
        px = mx0 + int((lon + 180) / 360 * mw) + dx
        py = my0 + int((90 - lat) / 180 * mh) + dy
        d.ellipse([px - 8, py - 8, px + 8, py + 8], fill=RED, outline=(255, 255, 255), width=1)
        d.text((px, py - 2), str(i), font=SANS_B(9), fill=(255, 255, 255), anchor="mm")
    d.text((mx0, my0 + mh + 4), "1 Washington  2 Tokyo  3 Seoul  4 Cairo", font=SANS(8), fill=MUTED)
    d.text((mx0, my0 + mh + 14), "5 Jiuquan  6 Ras Tanura  7 Hodeidah  8 Canberra", font=SANS(8), fill=MUTED)
    # --- DATE CHECK box (under map) ---
    dc_y = my0 + mh + 30
    d.rectangle([mx0, dc_y, mx0 + mw, 1008], outline=INK, width=1)
    d.text((mx0 + 6, dc_y + 4), "DATE CHECK", font=SANS_B(10), fill=RED)
    dc = [
        "EXCLUDED (earlier news):",
        "COP31 collapse 22 Nov · Dow first tops",
        "50,000 on 24 Nov · Nvidia +31.5% 24 Nov",
        "Sinner surgery 24 Nov · Riyadh strike 24 Nov",
        "NOT YET: Thanksgiving 27 Nov · US",
        "markets closed Thu · USTR hearing 25 Jan",
        "Starmind satellite 2033 · Dhaka wage 1 Dec",
    ]
    for j, ln in enumerate(dc):
        fnt = SANS_B(8) if j in (0, 6) else SANS(8)
        d.text((mx0 + 6, dc_y + 18 + j * 10), ln, font=fnt, fill=INK)

    # --- index (right) ---
    ix0 = MX + map_w + 14
    iw = W - MX - ix0
    d.text((ix0, yb), "ALSO ON WEDNESDAY — THE FULL DAY IN 37 MORE STORIES",
           font=SANS_B(11), fill=RED)
    colw = (iw - 2 * 10) / 3
    for col in range(3):
        cx = ix0 + col * (colw + 10)
        for r in range(13):
            k = col * 13 + r
            if k >= len(INDEX):
                break
            reg, head, fact, bd = INDEX[k]
            ry = yb + 18 + r * 21
            d.ellipse([cx, ry + 3, cx + 7, ry + 10], fill=REGION_COLOR[reg])
            d.text((cx + 11, ry), trunc(d, head, SANS_B(8), colw - 30), font=SANS_B(8), fill=INK)
            d.text((cx + 11, ry + 10), trunc(d, fact, SANS(8), colw - 30), font=SANS(8), fill=MUTED)
    # footer
    d.line([MX, 1012, W - MX, 1012], fill=LINE, width=1)
    d.text((MX, 1014), "All 50 stories happened or were first reported on Wednesday 25 November 2026 · Badges: OFFICIAL = primary source · CONFIRMED = 2+ outlets · REPORTED = single source / claim",
           font=SANS(7), fill=MUTED)

    # deterministic sparse paper grain (adds density; keeps output byte-stable)
    rng = random.Random(20261125)
    for _ in range(30000):
        gx, gy = rng.randrange(W), rng.randrange(H)
        v = rng.randint(-9, 9)
        r, g, b = img.getpixel((gx, gy))
        img.putpixel((gx, gy), (max(0, min(255, r + v)), max(0, min(255, g + v)), max(0, min(255, b + v))))
    img.save(path, optimize=True)
    return img

if __name__ == "__main__":
    build(os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png"))
    print("built entry.png")
