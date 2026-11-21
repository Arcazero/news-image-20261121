#!/usr/bin/env python3
"""Compose the 21 November 2026 front page for news-image-20261121.

The sheet is 1024 by 1024: a masthead, a weather bar built from real
Open-Meteo forecast figures for five cities, six illustrated story cards
in a two-by-three grid, and a source line along the bottom edge.

The six stories, each checked against reporting dated 20-21 Nov 2026:
  - Cyclone Akvan's rains linger over Odisha (the weather story)
  - a magnitude 6.8 tremor in Junin, Peru
  - Russia's heaviest air raid on Ukraine this year
  - New York's plan to shut Rikers Island by 2032 (the US local story)
  - COP31 running past its deadline in Antalya
  - a tanker hit and ablaze near Khasab in the Strait of Hormuz

Pictures live under assets/ and carry no lettering; every word on the
page is drawn here with DejaVu. Running `python3 draw.py` writes
entry.png (PNG while it fits in 1 MiB, otherwise JPEG).
"""
from pathlib import Path

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from PIL import ImageOps

PAGE_W = 1024
PAGE_H = 1024
RESULT = "entry.png"
PICTURES = Path("assets")

PALETTE = {
    "navy": (15, 42, 67),
    "gold": (184, 124, 22),
    "paper": (247, 245, 240),
    "ink": (26, 26, 26),
    "grey": (92, 92, 92),
    "body": (60, 60, 60),
    "white": (255, 255, 255),
    "line": (208, 203, 193),
    "sky": (228, 237, 243),
}

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
FONTS = {
    "mast": (f"{FONT_DIR}/DejaVuSerif-Bold.ttf", 50),
    "date": (f"{FONT_DIR}/DejaVuSans-Bold.ttf", 17),
    "label": (f"{FONT_DIR}/DejaVuSans-Bold.ttf", 13),
    "city": (f"{FONT_DIR}/DejaVuSans-Bold.ttf", 13),
    "value": (f"{FONT_DIR}/DejaVuSans.ttf", 12),
    "tag": (f"{FONT_DIR}/DejaVuSans-Bold.ttf", 12),
    "head": (f"{FONT_DIR}/DejaVuSans-Bold.ttf", 19),
    "text": (f"{FONT_DIR}/DejaVuSans.ttf", 14),
    "foot": (f"{FONT_DIR}/DejaVuSans.ttf", 12),
}


def load_fonts():
    """Resolve every named font to a truetype object."""
    loaded = {}
    for key, (path, size) in FONTS.items():
        loaded[key] = ImageFont.truetype(path, size)
    return loaded


def measure_wrap(canvas, wording, face, limit):
    """Split wording into lines no wider than limit pixels."""
    parts = wording.split(" ")
    wrapped = []
    current = ""
    for piece in parts:
        candidate = (current + " " + piece).strip()
        if canvas.textlength(candidate, font=face) <= limit:
            current = candidate
        else:
            if current:
                wrapped.append(current)
            current = piece
    if current:
        wrapped.append(current)
    return wrapped


def clamp_to_lines(canvas, wording, face, limit, most):
    """Wrap wording, keeping at most `most` lines with an ellipsis."""
    wrapped = measure_wrap(canvas, wording, face, limit)
    if len(wrapped) <= most:
        return wrapped
    kept = wrapped[:most]
    while kept and canvas.textlength(kept[-1] + " ...", font=face) > limit:
        head = kept[-1].rsplit(" ", 1)
        kept[-1] = head[0] if len(head) > 1 else ""
    kept[-1] = (kept[-1] + " ...").strip()
    return kept


def thumb(name, width, height):
    """Crop an illustration to the card's picture box and shrink its palette."""
    picture = Image.open(PICTURES / name).convert("RGB")
    fitted = ImageOps.fit(picture, (width, height), Image.LANCZOS)
    return fitted.convert("P", palette=Image.ADAPTIVE, colors=256).convert("RGB")


def draw_banner(canvas, fonts):
    """Masthead: title, gold rule, and the Saturday date line."""
    navy = PALETTE["navy"]
    canvas.text((PAGE_W // 2, 6), "THE WORLD TODAY",
                font=fonts["mast"], fill=navy, anchor="mt")
    canvas.line([(14, 58), (PAGE_W - 14, 58)], fill=PALETTE["gold"], width=3)
    canvas.text((PAGE_W // 2, 74), "Saturday, 21 November 2026",
                font=fonts["date"], fill=PALETTE["ink"], anchor="ma")


def draw_weather_bar(canvas, fonts):
    """Five-city weather bar from Open-Meteo forecast data for 21 Nov."""
    top = 112
    tall = 58
    canvas.rectangle([14, top, PAGE_W - 14, top + tall],
                     fill=PALETTE["sky"], outline=PALETTE["line"], width=1)
    canvas.text((26, top + 8), "WEATHER", font=fonts["label"],
                fill=PALETTE["navy"])
    canvas.text((26, top + 28), "21 NOV 2026", font=fonts["label"],
                fill=PALETTE["navy"])
    canvas.text((26, top + 43), "OPEN-METEO", font=fonts["value"],
                fill=PALETTE["grey"])
    readings = [
        ("Gopalpur", "28\u00b0 / 24\u00b0", "5.8 mm rain", "17 km/h"),
        ("Lima", "27\u00b0 / 24\u00b0", "0.3 mm rain", "19 km/h"),
        ("Antalya", "20\u00b0 / 18\u00b0", "6.9 mm rain", "11 km/h"),
        ("New York", "18\u00b0 / 6\u00b0", "dry", "12 km/h"),
        ("Kyiv", "7\u00b0 / 0\u00b0", "2.5 mm rain", "14 km/h"),
    ]
    start_x = 190
    slot = (PAGE_W - 14 - start_x) // len(readings)
    for pos, (city, temps, rain, wind) in enumerate(readings):
        left = start_x + pos * slot
        if pos:
            canvas.line([(left, top + 8), (left, top + tall - 8)],
                        fill=PALETTE["line"], width=1)
        canvas.text((left + 10, top + 6), city, font=fonts["city"],
                    fill=PALETTE["ink"])
        canvas.text((left + 10, top + 24), temps, font=fonts["value"],
                    fill=PALETTE["ink"])
        canvas.text((left + 10, top + 40), f"{rain} \u00b7 {wind}",
                    font=fonts["value"], fill=PALETTE["grey"])
    return top + tall + 12


def draw_story_grid(sheet, canvas, fonts, grid_top):
    """Six cards, two across and three down, each with a picture on top."""
    margin = 14
    gap = 12
    card_w = (PAGE_W - 2 * margin - gap) // 2
    card_h = (PAGE_H - grid_top - 34) // 3 - 10
    pic_h = 140
    entries = [
        ("WEATHER", "cyclone.webp",
         "Cyclone Akvan's rains keep falling on Odisha",
         "After landfall near Gopalpur, the storm's remnants bring heavy "
         "rain. Mayurbhanj and Balasore are under red alert and 4.4 lakh "
         "people were shifted to safety."),
        ("PERU", "peru.webp",
         "6.8 quake shakes Peru, Lima rushes outside",
         "A magnitude 6.8 earthquake struck the Junin region on Friday "
         "evening, felt 320 km away in the capital. No casualties or "
         "major damage were reported."),
        ("UKRAINE", "ukraine.webp",
         "Russia's biggest air attack of the year hits Ukraine",
         "More than 400 drones and 110 missiles rained down overnight. "
         "At least nine people were killed, Kyiv's bridges were damaged "
         "and Polish airspace was violated."),
        ("USA", "rikers.webp",
         "Mamdani sets 2032 to close Rikers Island",
         "New York's mayor unveiled the city's first comprehensive plan "
         "to shut the notorious jail complex, with four borough jails "
         "and $146m for mental health."),
        ("COP31", "cop31.webp",
         "COP31 spills into overtime, fossil fuels cut",
         "Climate talks in Antalya ran past their deadline with no deal. "
         "The draft agreement drops all mention of fossil fuels; a new "
         "text is due on Saturday."),
        ("HORMUZ", "hormuz.webp",
         "Tanker struck and burning off Khasab",
         "An outbound tanker was hit on its port bow and caught fire in "
         "the Strait of Hormuz. Iran claims a naval mine; shipping "
         "traffic is down about 15%."),
    ]
    for idx, (tag, pic_name, headline, blurb) in enumerate(entries):
        col = idx % 2
        row = idx // 2
        x = margin + col * (card_w + gap)
        y = grid_top + row * (card_h + 10)
        canvas.rectangle([x, y, x + card_w, y + card_h],
                         fill=PALETTE["white"], outline=PALETTE["line"],
                         width=1)
        sheet.paste(thumb(pic_name, card_w - 2, pic_h), (x + 1, y + 1))
        chip_w = canvas.textlength(tag, font=fonts["tag"]) + 16
        chip_y = y + 1 + pic_h - 24
        canvas.rectangle([x + 1, chip_y, x + 1 + chip_w, chip_y + 23],
                         fill=PALETTE["navy"])
        canvas.text((x + 9, chip_y + 4), tag, font=fonts["tag"],
                    fill=PALETTE["white"])
        text_x = x + 12
        text_w = card_w - 24
        head_y = y + pic_h + 12
        head_lines = clamp_to_lines(canvas, headline, fonts["head"],
                                    text_w, 2)
        for n, line in enumerate(head_lines):
            canvas.text((text_x, head_y + n * 22), line,
                        font=fonts["head"], fill=PALETTE["ink"])
        body_y = head_y + len(head_lines) * 22 + 4
        body_lines = clamp_to_lines(canvas, blurb, fonts["text"],
                                    text_w, 3)
        for n, line in enumerate(body_lines):
            canvas.text((text_x, body_y + n * 17), line,
                        font=fonts["text"], fill=PALETTE["body"])
        lowest = body_y + len(body_lines) * 17
        assert lowest <= y + card_h - 6, f"card {tag} overflows"


def draw_source_line(canvas, fonts):
    """Rule plus the list of sources, centred near the bottom edge."""
    base = PAGE_H - 26
    canvas.line([(14, base - 8), (PAGE_W - 14, base - 8)],
                fill=PALETTE["line"], width=1)
    note = ("Sources: Reuters \u00b7 IMD \u00b7 CNN \u00b7 AP \u00b7 "
            "UKMTO \u00b7 Open-Meteo \u2014 "
            "six stories verified 21 November 2026")
    canvas.text((PAGE_W // 2, base), note, font=fonts["foot"],
                fill=PALETTE["grey"], anchor="ma")


def build_front_page():
    """Render every layer and save the finished page."""
    sheet = Image.new("RGB", (PAGE_W, PAGE_H), PALETTE["paper"])
    canvas = ImageDraw.Draw(sheet)
    fonts = load_fonts()
    draw_banner(canvas, fonts)
    grid_top = draw_weather_bar(canvas, fonts)
    draw_story_grid(sheet, canvas, fonts, grid_top)
    draw_source_line(canvas, fonts)
    sheet.save(RESULT, "PNG", optimize=True)
    size = Path(RESULT).stat().st_size
    print(f"saved {RESULT}: {sheet.size}, {size} bytes")
    if size > 1048576:
        sheet.save(RESULT, "JPEG", quality=88)
        print(f"over 1 MiB, saved as JPEG: "
              f"{Path(RESULT).stat().st_size} bytes")


if __name__ == "__main__":
    build_front_page()
