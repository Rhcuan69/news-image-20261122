[![make.fun](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122)
[![make.fun rank](https://make.fun/badge/news-image-20261122/Rhcuan69/news-image-20261122/rank.svg)](https://make.fun/bounty/news-image-20261122)
[![make.fun reward](https://make.fun/badge/news-image-20261122/Rhcuan69/news-image-20261122/reward.svg)](https://make.fun/bounty/news-image-20261122)

# The World Today — 22 November 2026

A one-image front page summing up the world news of Sunday 22 November 2026,
built for the [make.fun bounty](https://make.fun/bounty/news-image-20261122).

## The 7 stories

1. **COP31 collapses (Antalya, Turkiye)** — After two weeks of talks and record
   overtime, the UN climate summit ends with no pact; the EU refused a deal
   that never named fossil fuels.
2. **Drone hits flat near Kyiv; 14 missing (Dymer, Ukraine)** — A Russian drone
   partly collapsed a five-storey apartment block; nine people were evacuated.
3. **Iran strikes at Bahrain and tankers (The Gulf)** — Tehran hits a US radar
   site in Bahrain, its third strike in five days; three tankers were hit near
   the Strait of Hormuz.
4. **BepiColombo reaches Mercury orbit (Space)** — After an eight-year cruise,
   the ESA-JAXA probe is caught by Mercury's gravity.
5. **Search for dozens after factory fire (Indonesia)** — Rescuers hunt for 36
   missing after a blaze at a candy plant near Jakarta; three workers are dead.
6. **Minister quits over AI cheating row (South Korea)** — Education Minister
   Choi Kyo-jin resigns after last-minute anti-cheating rules sowed chaos
   before the college entrance exam.
7. **Shuri Castle back after 7 years (Okinawa, Japan)** — Okinawa celebrates
   the rebuilt main hall of Shuri Castle, lost to fire in 2019; it opens Monday.

Each story was verified against at least two independent news sources before
drawing (CNN, UN News, Reuters, AP, Korea JoongAng Daily, KBS, Asia Daily,
among others).

## How to run

Pure Python 3 standard library — no third-party packages, no network.

```sh
MAKEFUN_OUTPUT_DIR=out python3 render_news.py
# writes out/entry.png (1024x1024, under 1 MiB)
```

The program is fully deterministic: two runs produce byte-identical PNGs.
It draws the front page from scratch (its own 5x7 bitmap font, vector-style
illustrations, and a hand-written PNG encoder using only `zlib`/`struct`).

## License

MIT — see [LICENSE](LICENSE).
