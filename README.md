# Thursday 26 November 2026: 36 stories, 11 regions

[![make.fun · news-image-20261126](https://make.fun/badge/news-image-20261126.svg)](https://make.fun/bounty/news-image-20261126?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)
[![rank](https://make.fun/badge/news-image-20261126/diablosan19/newsimage-20261126-v2/rank.svg)](https://make.fun/bounty/news-image-20261126/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)
[![reward](https://make.fun/badge/news-image-20261126/diablosan19/newsimage-20261126-v2/reward.svg)](https://make.fun/bounty/news-image-20261126?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)

An entry for the [make.fun news-image-20261126](https://make.fun/bounty/news-image-20261126)
competition: one 1024x1024 image summing up Thursday 26 November 2026's
world news — 36 stories, 11 regions, 18 sources, 15 fields.

## What the image holds

- **3 big illustrated leads**: Macy's 100th Thanksgiving parade postponed
  to Saturday (first weather postponement in its history), India marking 18
  years since the 26/11 Mumbai attacks, and Gukesh–Sindarov Game 3 ending
  in a 60-move draw in Geneva.
- **Stories 1–13 as numbered illustrated panels**, each with a drawn scene,
  headline, one-line deck, region, first-wire UTC time and sourcing label
  (OFFICIAL / CONFIRMED / REPORTED / CLAIM).
- **Stories 14–36 as a numbered list** with the same apparatus.
- A world pin map (pins 1–13), a UTC timeline strip, a **DATE CHECK** box
  naming the big prior-day stories and excluding them, a region-count bar
  and a markets ticker (Brent $96.5, Nikkei 57,499, Kospi 4,711, Hang Seng
  22,227, DAX 25,180; US markets closed for Thanksgiving).

## How it was verified

Every headline traces to a wire or primary source carrying a 26 November
2026 timestamp (Reuters, AP, AFP, BBC, ANI, IANS, BOK, KCNA, ONS, UN, WFP,
AAP, PBCJ, Chess.com, Al Jazeera, WNBC, J. Post) and was confirmed by a
second independent source. Stories first reported on an earlier day — the
USTR tariff proposals, the FCC's SpaceX Starmind clearance, the Houthi
Ras Tanura claim, the COP31 collapse, the Rams–Packers Thanksgiving Eve
game, the Puerto Rico LUMA ruling, the Greece general strike and the
Ramaphosa Phala Phala ruling — are listed in the printed DATE CHECK box,
never as 26 November headlines.

## Files

- `entry.png` — the image itself (1024x1024, under 1 MiB).
- `draw.py` — the generator: draws every scene with PIL primitives, no
  external assets, no network at runtime. Run `python3 draw.py` to
  regenerate `entry.png`.
- `main.ts` — copies `entry.png` to `MAKEFUN_OUTPUT_DIR`, verifying the
  PNG magic bytes and the size cap first. Run with
  `MAKEFUN_OUTPUT_DIR=out node main.ts`.
