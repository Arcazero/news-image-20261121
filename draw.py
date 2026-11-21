#!/usr/bin/env python3
"""Draw the news-image-20261121 entry: a 1024x1024 newspaper front page
summing up Saturday 21 November 2026.

Six verified stories (all happened or first reported on 20-21 Nov 2026):
  1. WEATHER  - Cyclone Akvan's rains keep falling on Odisha; red alerts
                in Mayurbhanj/Balasore, 4.4 lakh people shifted (IMD)
  2. PERU     - Magnitude 6.8 quake strikes Junin, felt in Lima (Reuters)
  3. UKRAINE  - Russia's biggest air attack of the year: 400+ drones,
                110+ missiles, at least 9 killed (CNN/Reuters)
  4. USA      - Mamdani unveils plan to close Rikers Island by 2032
                (Reuters/AP)
  5. COP31    - Climate talks spill into overtime; fossil fuels dropped
                from the draft deal (Reuters/AP)
  6. HORMUZ   - Tanker struck and burning off Khasab; Iran claims a
                naval mine, traffic down ~15% (UKMTO/Reuters)

Six AI-generated illustrations (assets/, no text in them) + clean PIL text
(DejaVu Sans/Serif). Weather strip uses REAL 21 Nov 2026 forecast data
from the Open-Meteo forecast API for five story cities.
Output entry.png; PNG first, JPEG q85 fallback if over 1 MiB.
Layout asserts nothing overflows its card.
"""
import os
from PIL import Image, ImageDraw, ImageFont, ImageOps

W, H = 1024, 1024
OUT = "entry.png"
ASSETS = "assets"

NAVY = (15, 42, 67)
GOLD = (184, 124, 22)
PAPER = (247, 245, 240)
INK = (26, 26, 26)
MUTED = (92, 92, 92)
WHITE = (255, 255, 255)
BORDER = (208, 203, 193)
SKY = (228, 237, 243)
TAG_BG = (15, 42, 67)

SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Wrap text to fit max_w pixels; returns list of lines."""
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


def fit_lines(draw, text, fnt, max_w, max_lines):
    """Wrap and cap to max_lines, adding an ellipsis if truncated."""
    lines = wrap(draw, text, fnt, max_w)
    if len(lines) > max_lines:
        lines = lines[:max_lines]
        # trim last line until the ellipsis fits
        while lines and draw.textlength(lines[-1] + " ...", font=fnt) > max_w:
            lines[-1] = lines[-1].rsplit(" ", 1)[0] if " " in lines[-1] else ""
        lines[-1] = (lines[-1] + " ...").strip()
    return lines


def load_pic(name, tw, th):
    """Load an illustration, centre-crop to the target aspect, resize,
    and quantize to a 256-colour palette so the final PNG stays small."""
    path = os.path.join(ASSETS, name)
    im = Image.open(path).convert("RGB")
    im = ImageOps.fit(im, (tw, th), Image.LANCZOS)
    return im.convert("P", palette=Image.ADAPTIVE, colors=256).convert("RGB")


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    f_mast = font(SERIF_B, 50)
    f_date = font(SANS_B, 17)
    f_wlab = font(SANS_B, 13)
    f_wcity = font(SANS_B, 13)
    f_wval = font(SANS, 12)
    f_tag = font(SANS_B, 12)
    f_head = font(SANS_B, 19)
    f_body = font(SANS, 14)
    f_foot = font(SANS, 12)

    # ---- Masthead ----
    d.text((W // 2, 6), "THE WORLD TODAY", font=f_mast, fill=NAVY,
           anchor="mt")
    d.line([(14, 58), (W - 14, 58)], fill=GOLD, width=3)
    d.text((W // 2, 74), "Saturday, 21 November 2026", font=f_date,
           fill=INK, anchor="ma")

    # ---- Weather strip (REAL 21 Nov 2026 data, Open-Meteo forecast API) ----
    wy, wh = 112, 58
    d.rectangle([14, wy, W - 14, wy + wh], fill=SKY,
                outline=BORDER, width=1)
    d.text((26, wy + 8), "WEATHER", font=f_wlab, fill=NAVY)
    d.text((26, wy + 28), "21 NOV 2026", font=f_wlab, fill=NAVY)
    d.text((26, wy + 43), "OPEN-METEO", font=f_wval, fill=MUTED)
    cities = [
        ("Gopalpur", "28\u00b0 / 24\u00b0", "5.8 mm rain", "17 km/h"),
        ("Lima", "27\u00b0 / 24\u00b0", "0.3 mm rain", "19 km/h"),
        ("Antalya", "20\u00b0 / 18\u00b0", "6.9 mm rain", "11 km/h"),
        ("New York", "18\u00b0 / 6\u00b0", "dry", "12 km/h"),
        ("Kyiv", "7\u00b0 / 0\u00b0", "2.5 mm rain", "14 km/h"),
    ]
    x0 = 190
    cw = (W - 14 - x0) // len(cities)
    for i, (city, temp, rain, wind) in enumerate(cities):
        cx = x0 + i * cw
        if i:
            d.line([(cx, wy + 8), (cx, wy + wh - 8)], fill=BORDER, width=1)
        d.text((cx + 10, wy + 6), city, font=f_wcity, fill=INK)
        d.text((cx + 10, wy + 24), temp, font=f_wval, fill=INK)
        d.text((cx + 10, wy + 40), f"{rain} \u00b7 {wind}", font=f_wval,
               fill=MUTED)

    # ---- Story cards: 2 columns x 3 rows ----
    stories = [
        dict(tag="WEATHER", pic="cyclone.webp",
             head="Cyclone Akvan's rains keep falling on Odisha",
             body="After landfall near Gopalpur, the storm's remnants "
                  "bring heavy rain. Mayurbhanj and Balasore are under "
                  "red alert and 4.4 lakh people were shifted to safety."),
        dict(tag="PERU", pic="peru.webp",
             head="6.8 quake shakes Peru, Lima rushes outside",
             body="A magnitude 6.8 earthquake struck the Junin region "
                  "on Friday evening, felt 320 km away in the capital. "
                  "No casualties or major damage were reported."),
        dict(tag="UKRAINE", pic="ukraine.webp",
             head="Russia's biggest air attack of the year hits Ukraine",
             body="More than 400 drones and 110 missiles rained down "
                  "overnight. At least nine people were killed, Kyiv's "
                  "bridges were damaged and Polish airspace was violated."),
        dict(tag="USA", pic="rikers.webp",
             head="Mamdani sets 2032 to close Rikers Island",
             body="New York's mayor unveiled the city's first "
                  "comprehensive plan to shut the notorious jail complex, "
                  "with four borough jails and $146m for mental health."),
        dict(tag="COP31", pic="cop31.webp",
             head="COP31 spills into overtime, fossil fuels cut",
             body="Climate talks in Antalya ran past their deadline with "
                  "no deal. The draft agreement drops all mention of "
                  "fossil fuels; a new text is due on Saturday."),
        dict(tag="HORMUZ", pic="hormuz.webp",
             head="Tanker struck and burning off Khasab",
             body="An outbound tanker was hit on its port bow and caught "
                  "fire in the Strait of Hormuz. Iran claims a naval "
                  "mine; shipping traffic is down about 15%."),
    ]

    mx, gutter = 14, 12
    cw_card = (W - 2 * mx - gutter) // 2
    top = wy + wh + 12
    rows = 3
    ch_card = (H - top - 34) // rows - 10
    pic_h = 140

    for idx, s in enumerate(stories):
        col, row = idx % 2, idx // 2
        x = mx + col * (cw_card + gutter)
        y = top + row * (ch_card + 10)
        d.rectangle([x, y, x + cw_card, y + ch_card], fill=WHITE,
                    outline=BORDER, width=1)
        pic = load_pic(s["pic"], cw_card - 2, pic_h)
        img.paste(pic, (x + 1, y + 1))
        # tag chip over the picture's bottom-left
        tag = s["tag"]
        tw = d.textlength(tag, font=f_tag) + 16
        ty = y + 1 + pic_h - 24
        d.rectangle([x + 1, ty, x + 1 + tw, ty + 23], fill=TAG_BG)
        d.text((x + 9, ty + 4), tag, font=f_tag, fill=WHITE)
        tx = x + 12
        tw_text = cw_card - 24
        hy = y + pic_h + 12
        head_lines = fit_lines(d, s["head"], f_head, tw_text, 2)
        for i, ln in enumerate(head_lines):
            d.text((tx, hy + i * 22), ln, font=f_head, fill=INK)
        by = hy + len(head_lines) * 22 + 4
        body_lines = fit_lines(d, s["body"], f_body, tw_text, 3)
        for i, ln in enumerate(body_lines):
            d.text((tx, by + i * 17), ln, font=f_body, fill=(60, 60, 60))
        # overflow assert: last body line must end inside the card
        assert by + len(body_lines) * 17 <= y + ch_card - 6, \
            f"card {s['tag']} overflows"

    # ---- Footer ----
    fy = H - 26
    d.line([(14, fy - 8), (W - 14, fy - 8)], fill=BORDER, width=1)
    foot = ("Sources: Reuters \u00b7 IMD \u00b7 CNN \u00b7 AP \u00b7 "
            "UKMTO \u00b7 Open-Meteo \u2014 "
            "six stories verified 21 November 2026")
    d.text((W // 2, fy), foot, font=f_foot, fill=MUTED, anchor="ma")

    img.save(OUT, "PNG", optimize=True)
    size = os.path.getsize(OUT)
    print(f"saved {OUT}: {img.size}, {size} bytes")
    if size > 1048576:
        img.save(OUT, "JPEG", quality=88)
        print(f"over 1 MiB, saved as JPEG: {os.path.getsize(OUT)} bytes")


if __name__ == "__main__":
    main()
