#!/usr/bin/env python3
"""Draw the 17 November 2026 world-news summary image.

Flat editorial front-page illustration, 1024x1024, drawn with Pillow.
Every shape and label is original work written for this entry; the five
stories below were verified against the day's reporting (17 Nov 2026):

  1. Ukraine strikes the Kerch Bridge to Crimea a second day running;
     a road span collapses, as Russia hits bridges in Kyiv.
  2. Two oil tankers strike mines and catch fire near the Strait of Hormuz.
  3. Trump arrives in Manila for ASEAN; a Xi-Trump-Putin meeting is
     confirmed for Thursday in Shenzhen on the APEC sidelines.
  4. Japan scrambles fighter jets after suspected Russian aircraft
     enter its airspace; Tokyo protests.
  5. The UK, Australia, Canada and Italy call on Israel to open Gaza
     crossings, citing flooding and a catastrophic aid situation.

Also today: MS Dhoni retires from the IPL; Gerard Depardieu admits a
sexual-assault charge in a Paris court.
"""
import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024

PAPER = (246, 241, 231)
INK = (26, 26, 26)
RED = (179, 39, 30)
GREY = (110, 104, 92)
RULE = (60, 56, 48)
SKY = (176, 205, 224)
SEA = (46, 96, 128)
SEA_DARK = (32, 74, 102)
SAND = (214, 196, 160)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, x, y, text, fnt, fill, max_w, leading):
    """Draw wrapped text; returns y after the last line."""
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def kicker(draw, x, y, s, size=19):
    f = font(SANS_B, size)
    draw.text((x, y), s, font=f, fill=RED)
    return y + size + 6


def rule(draw, x0, y, x1, width=2, fill=RULE):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


# ---------------------------------------------------------------- scenes

def scene_bridge(draw, x0, y0, w, h):
    """Kerch Bridge over the strait, one span collapsed, smoke rising."""
    x1, y1 = x0 + w, y0 + h
    draw.rectangle([x0, y0, x1, y1], fill=SKY)
    # low sun
    draw.ellipse([x1 - 92, y0 + 18, x1 - 32, y0 + 78], fill=(240, 196, 110))
    # sea
    sea_y = y0 + int(h * 0.62)
    draw.rectangle([x0, sea_y, x1, y1], fill=SEA)
    for i, wy in enumerate((sea_y + 22, sea_y + 52, sea_y + 82)):
        draw.line([(x0 + 14, wy), (x1 - 14, wy)], fill=SEA_DARK, width=3)
    # far shore
    draw.rectangle([x0, sea_y - 14, x1, sea_y], fill=(120, 138, 112))
    # bridge deck: left part intact, middle collapsed, right part intact
    deck_y = y0 + int(h * 0.42)
    gap0, gap1 = x0 + int(w * 0.44), x0 + int(w * 0.60)
    draw.rectangle([x0, deck_y, gap0, deck_y + 12], fill=(70, 66, 60))
    draw.rectangle([gap1, deck_y, x1, deck_y + 12], fill=(70, 66, 60))
    # collapsed span, tilted down into the water
    draw.polygon(
        [(gap0, deck_y + 12), (gap1, deck_y + 12),
         (gap1 - 8, deck_y + 66), (gap0 + 14, deck_y + 58)],
        fill=(52, 49, 44))
    # towers
    for tx in (x0 + int(w * 0.20), x0 + int(w * 0.80)):
        draw.rectangle([tx - 6, deck_y - 78, tx + 6, deck_y], fill=(88, 84, 76))
        draw.line([(tx, deck_y - 78), (tx - 70, deck_y)], fill=(120, 116, 108), width=2)
        draw.line([(tx, deck_y - 78), (tx + 70, deck_y)], fill=(120, 116, 108), width=2)
    # burst + smoke over the gap
    cx, cy = (gap0 + gap1) // 2, deck_y - 2
    for r, col in ((24, (240, 140, 40)), (15, (250, 190, 60)), (8, (255, 230, 120))):
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=col)
    ov = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    od = ImageDraw.Draw(ov)
    for (sx, sy, r, a) in ((cx - 22, cy - 52, 24, 150), (cx + 4, cy - 74, 28, 130),
                           (cx + 28, cy - 48, 20, 150), (cx - 2, cy - 96, 20, 110)):
        od.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(120, 118, 112, a))
    draw._image.paste(ov, (x0, y0), ov)
    # splash where the span went down
    draw.line([(gap0 + 8, deck_y + 72), (gap1 - 6, deck_y + 72)],
              fill=(220, 235, 245), width=3)


def scene_tanker(draw, x0, y0, w, h):
    """Oil tanker at sea with a mine and flames."""
    x1, y1 = x0 + w, y0 + h
    draw.rectangle([x0, y0, x1, y1], fill=(232, 214, 178))
    draw.rectangle([x0, y0 + int(h * 0.60), x1, y1], fill=SEA)
    for wy in (y0 + int(h * 0.72), y0 + int(h * 0.86)):
        draw.line([(x0 + 10, wy), (x1 - 10, wy)], fill=SEA_DARK, width=3)
    # tanker hull + deck
    hy = y0 + int(h * 0.52)
    draw.polygon([(x0 + 18, hy), (x1 - 26, hy), (x1 - 52, hy + 34),
                  (x0 + 34, hy + 34)], fill=(150, 52, 38))
    draw.rectangle([x0 + 40, hy - 26, x1 - 90, hy], fill=(210, 205, 190))
    draw.rectangle([x0 + 96, hy - 52, x0 + 128, hy - 26], fill=(230, 226, 214))
    draw.rectangle([x0 + 108, hy - 66, x0 + 116, hy - 52], fill=(90, 86, 78))
    # flames from the bow: teardrop tongues
    fx, fy = x1 - 58, hy - 6
    draw.polygon([(fx - 18, fy), (fx - 4, fy - 34), (fx + 10, fy - 8), (fx + 4, fy)],
                 fill=(240, 120, 30))
    draw.polygon([(fx - 8, fy), (fx + 2, fy - 24), (fx + 14, fy - 6), (fx + 8, fy)],
                 fill=(250, 190, 60))
    draw.polygon([(fx - 2, fy), (fx + 4, fy - 14), (fx + 10, fy - 2), (fx + 4, fy)],
                 fill=(255, 230, 120))
    # mine: spiked ball floating ahead
    mx, my = x0 + 34, y0 + int(h * 0.78)
    for ang in range(0, 360, 45):
        import math
        ex = mx + int(22 * math.cos(math.radians(ang)))
        ey = my + int(22 * math.sin(math.radians(ang)))
        draw.line([(mx, my), (ex, ey)], fill=(40, 40, 40), width=3)
    draw.ellipse([mx - 14, my - 14, mx + 14, my + 14], fill=(40, 40, 40))


def scene_summit(draw, x0, y0, w, h):
    """Three flags over a summit table: US, China, Russia."""
    x1, y1 = x0 + w, y0 + h
    draw.rectangle([x0, y0, x1, y1], fill=(226, 232, 238))
    # table
    draw.rectangle([x0 + 16, y0 + int(h * 0.66), x1 - 16, y0 + int(h * 0.74)],
                   fill=(122, 84, 52))
    draw.rectangle([x0 + 24, y0 + int(h * 0.74), x0 + 34, y1 - 8], fill=(96, 64, 40))
    draw.rectangle([x1 - 34, y0 + int(h * 0.74), x1 - 24, y1 - 8], fill=(96, 64, 40))
    # three chairs
    for cx in (x0 + int(w * 0.22), x0 + int(w * 0.50), x0 + int(w * 0.78)):
        draw.rectangle([cx - 26, y0 + int(h * 0.52), cx + 26, y0 + int(h * 0.66)],
                       fill=(70, 76, 88))
    flags = [
        ("US", [(178, 34, 52), (255, 255, 255), (178, 34, 52), (255, 255, 255),
                (178, 34, 52), (255, 255, 255), (178, 34, 52)]),
        ("CN", [(222, 41, 16)]),
        ("RU", [(255, 255, 255), (0, 57, 166), (213, 0, 50)]),
    ]
    for i, (code, stripes) in enumerate(flags):
        fx = x0 + int(w * (0.14 + 0.30 * i))
        fy = y0 + 12
        fw, fh = 56, 38
        draw.line([(fx + fw // 2, fy), (fx + fw // 2, y0 + int(h * 0.52))],
                  fill=(60, 56, 48), width=3)
        sh = fh // len(stripes)
        for j, col in enumerate(stripes):
            draw.rectangle([fx, fy + j * sh, fx + fw, fy + (j + 1) * sh], fill=col)
        draw.rectangle([fx, fy, fx + fw, fy + fh], outline=(60, 56, 48), width=2)
        if code == "US":
            draw.rectangle([fx, fy, fx + 24, fy + 16], fill=(40, 48, 96))
            for sx in (fx + 7, fx + 16):
                for sy in (fy + 5, fy + 11):
                    draw.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=(255, 255, 255))
        if code == "CN":
            for (sx, sy) in ((fx + 10, fy + 10), (fx + 21, fy + 7), (fx + 24, fy + 13),
                             (fx + 19, fy + 18), (fx + 10, fy + 16)):
                draw.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=(255, 222, 0))


def scene_jet(draw, x0, y0, w, h):
    """Fighter jet climbing past a red sun disc."""
    x1, y1 = x0 + w, y0 + h
    draw.rectangle([x0, y0, x1, y1], fill=(196, 216, 232))
    draw.ellipse([x0 + int(w * 0.62), y0 + 14, x0 + int(w * 0.62) + 74,
                  y0 + 88], fill=(196, 52, 44))
    for (cx, cy, r) in ((x0 + 30, y0 + 30, 16), (x0 + 64, y0 + 18, 12),
                        (x0 + 96, y0 + 34, 14)):
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 255, 255))
    # jet: fuselage, wings, tail, canopy
    jx, jy = x0 + int(w * 0.55), y0 + int(h * 0.58)
    draw.polygon([(jx - 62, jy + 6), (jx + 50, jy - 22), (jx + 62, jy - 18),
                  (jx + 32, jy + 2), (jx - 16, jy + 14)], fill=(52, 58, 66))
    draw.polygon([(jx - 4, jy - 8), (jx + 20, jy - 42), (jx + 34, jy - 40),
                  (jx + 18, jy - 6)], fill=(66, 72, 82))
    draw.polygon([(jx - 46, jy + 2), (jx - 24, jy + 28), (jx - 10, jy + 24),
                  (jx - 28, jy + 4)], fill=(66, 72, 82))
    draw.polygon([(jx + 28, jy - 18), (jx + 46, jy - 28), (jx + 52, jy - 22),
                  (jx + 36, jy - 12)], fill=(66, 72, 82))
    draw.polygon([(jx + 28, jy - 20), (jx + 44, jy - 24), (jx + 34, jy - 12)],
                 fill=(150, 200, 230))
    # contrail
    draw.line([(jx - 66, jy + 8), (x0 + 4, jy + 30)], fill=(255, 255, 255), width=5)


def scene_aid(draw, x0, y0, w, h):
    """Aid trucks at a crossing, rain falling."""
    x1, y1 = x0 + w, y0 + h
    draw.rectangle([x0, y0, x1, y1], fill=(222, 214, 196))
    draw.rectangle([x0, y0 + int(h * 0.66), x1, y1], fill=(150, 142, 122))
    # rain
    for (rx, ry) in ((x0 + 20, y0 + 16), (x0 + 60, y0 + 40), (x0 + 110, y0 + 12),
                     (x0 + 150, y0 + 44), (x0 + 190, y0 + 20), (x0 + 40, y0 + 64),
                     (x0 + 130, y0 + 66), (x0 + 175, y0 + 62)):
        draw.line([(rx, ry), (rx - 5, ry + 14)], fill=(120, 130, 150), width=2)
    # barrier arm
    draw.line([(x0 + 12, y0 + int(h * 0.52)), (x1 - 30, y0 + int(h * 0.40))],
              fill=(200, 60, 40), width=6)
    # two trucks
    for tx in (x0 + 10, x0 + 94):
        ty = y0 + int(h * 0.56)
        draw.rectangle([tx, ty, tx + 62, ty + 34], fill=(240, 238, 228))
        draw.rectangle([tx + 62, ty + 8, tx + 88, ty + 34], fill=(196, 52, 44))
        draw.rectangle([tx + 66, ty + 12, tx + 84, ty + 22], fill=(180, 215, 235))
        draw.ellipse([tx + 10, ty + 30, tx + 26, ty + 46], fill=(30, 30, 30))
        draw.ellipse([tx + 38, ty + 30, tx + 54, ty + 46], fill=(30, 30, 30))
        draw.ellipse([tx + 68, ty + 30, tx + 84, ty + 46], fill=(30, 30, 30))
    # aid box on the ground
    draw.rectangle([x1 - 46, y0 + int(h * 0.72), x1 - 14, y0 + int(h * 0.88)],
                   fill=(196, 160, 90))
    draw.text((x1 - 42, y0 + int(h * 0.76)), "+", font=font(SANS_B, 20), fill=(255, 255, 255))


# ---------------------------------------------------------------- page

def build(out_path):
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 24  # margin
    # frame
    d.rectangle([8, 8, W - 9, H - 9], outline=INK, width=3)

    # masthead
    y = 26
    title = "THE WORLD IN ONE DAY"
    tf = font(SERIF_B, 62)
    d.text(((W - d.textlength(title, font=tf)) / 2, y), title, font=tf, fill=INK)
    y += 78
    rule(d, M, y, W - M, 3)
    y += 10
    date = "TUESDAY  ·  17 NOVEMBER 2026"
    df = font(SANS_B, 30)
    d.text(((W - d.textlength(date, font=df)) / 2, y), date, font=df, fill=RED)
    y += 46
    rule(d, M, y, W - M, 2)
    rule(d, M, y + 5, W - M, 1)

    # ---- lead story: Kerch Bridge
    lead_y0, lead_y1 = y + 14, 508
    img_w, img_h = 520, lead_y1 - lead_y0
    scene_bridge(d, M, lead_y0, img_w, img_h)
    d.rectangle([M, lead_y0, M + img_w, lead_y1], outline=INK, width=2)
    tx = M + img_w + 22
    tw = W - M - tx
    ty = lead_y0 + 6
    ty = kicker(d, tx, ty, "UKRAINE  ·  WAR")
    ty = text_block(d, tx, ty, "BRIDGE TO CRIMEA HIT AGAIN",
                    font(SANS_B, 44), INK, tw, 52)
    ty += 8
    ty = text_block(
        d, tx, ty,
        "Ukraine strikes the Kerch crossing for a second day; a road span "
        "collapses as Russia hits bridges in Kyiv.",
        font(SANS, 22), (52, 48, 42), tw, 30)
    rule(d, M, lead_y1 + 12, W - M, 2)

    # ---- 2x2 grid of secondary stories
    stories = [
        (scene_tanker, "MIDDLE EAST  ·  SHIPPING",
         "TANKERS HIT BY MINES OFF HORMUZ",
         "Two oil tankers catch fire near the Strait; a third U.S. carrier arrives."),
        (scene_summit, "ASIA  ·  DIPLOMACY",
         "TRUMP IN MANILA; XI–TRUMP–PUTIN MEET SET",
         "Three-way meeting confirmed for Thursday in Shenzhen at APEC."),
        (scene_jet, "ASIA-PACIFIC  ·  SECURITY",
         "JAPAN SCRAMBLES JETS",
         "Tokyo protests after suspected Russian aircraft enter its airspace."),
        (scene_aid, "MIDDLE EAST  ·  AID",
         "WEST URGES: OPEN GAZA CROSSINGS",
         "UK, Australia, Canada and Italy cite flooding and a “catastrophic” aid crisis."),
    ]
    grid_y0 = lead_y1 + 26
    cell_w = (W - 2 * M - 16) // 2
    cell_h = 186
    for i, (scene, kick, head, sub) in enumerate(stories):
        cx = M + (i % 2) * (cell_w + 16)
        cy = grid_y0 + (i // 2) * (cell_h + 14)
        iw = 190
        scene(d, cx, cy, iw, cell_h)
        d.rectangle([cx, cy, cx + iw, cy + cell_h], outline=INK, width=2)
        tx2 = cx + iw + 14
        tw2 = cell_w - iw - 14
        ty2 = cy + 4
        ty2 = kicker(d, tx2, ty2, kick, size=16)
        ty2 = text_block(d, tx2, ty2, head, font(SANS_B, 25), INK, tw2, 30)
        ty2 += 4
        text_block(d, tx2, ty2, sub, font(SANS, 18), (52, 48, 42), tw2, 24)
        if i % 2 == 0:
            d.line([(cx + cell_w + 8, cy), (cx + cell_w + 8, cy + cell_h)],
                   fill=GREY, width=1)

    # ---- ticker (shrink font until it fits the band)
    tick_y = grid_y0 + 2 * cell_h + 14 + 12
    d.rectangle([M, tick_y, W - M, tick_y + 44], fill=INK)
    tick = "ALSO TODAY   •   Dhoni retires from the IPL   •   Depardieu admits assault charge in Paris"
    tsize = 19
    while tsize > 13 and d.textlength(tick, font=font(SANS_B, tsize)) > W - 2 * M - 28:
        tsize -= 1
    d.text((M + 14, tick_y + (44 - tsize) // 2 - 1), tick, font=font(SANS_B, tsize),
           fill=(246, 241, 231))

    # ---- footer
    foot = "Events reported on Tuesday 17 November 2026"
    ff = font(SANS, 17)
    d.text(((W - d.textlength(foot, font=ff)) / 2, tick_y + 56), foot,
           font=ff, fill=GREY)

    img.save(out_path, "PNG", optimize=True)
    return out_path


if __name__ == "__main__":
    out = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    os.makedirs(out, exist_ok=True)
    p = build(os.path.join(out, "entry.png"))
    print("wrote", p, os.path.getsize(p), "bytes")
