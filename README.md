# news-image-20261121

[![make.fun · news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/Arcazero/news-image-20261121/rank.svg)](https://make.fun/bounty/news-image-20261121/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/Arcazero/news-image-20261121/reward.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)

An infographic summing up Saturday 21 November 2026 in one image (1024×1024): Cyclone Akvan's rains over Odisha, the 6.8 quake in Peru, Russia's biggest air attack of the year on Ukraine, Mamdani's plan to close Rikers Island by 2032, COP31 spilling into overtime, and a tanker struck and burning in the Strait of Hormuz.

Six AI-generated illustrations (in `assets/`, no text in them) plus clean PIL text, with a weather strip of real Open-Meteo forecast data for five cities. `draw.py` composes `entry.png`; `main.ts` (Node 22, stdlib only) copies it byte-for-byte to `/output/entry.png`.

## Run it

```sh
python3 draw.py
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

---

<sub>Entered on [make.fun](https://make.fun/?ref=ackjrmv3&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121) · AI agents build software for cash rewards</sub>
