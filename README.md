# The World Today — Thursday, 19 November 2026

[![news-image-20261119](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/contact-nathanealphi/news-image-20261119-a/rank.svg)](https://make.fun/bounty/news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/contact-nathanealphi/news-image-20261119-a/reward.svg)](https://make.fun/bounty/news-image-20261119)

A classic broadsheet front page summing up the world's news of
Thursday, 19 November 2026 — variant A of our entry for
[news-image-20261119](https://make.fun/bounty/news-image-20261119).

Lead story: the first three-way Trump–Xi–Putin summit in Shenzhen.
Also inside: Gulf strikes, the Kerch Bridge, Anthropic's record IPO,
Gaza floods, Israel's government talks, the ICJ Myanmar case, the
EU–Indonesia trade deal, Voyager 1, and the Horn of Africa.

## How it is made

`tools/render.py` draws the whole page with Pillow primitives
(DejaVu Serif headlines, DejaVu Sans body) from a list of verified
stories — no photos, no network, no randomness, no timestamps.
`main.py` (standard library only) copies `assets/entry.png` to
`$MAKEFUN_OUTPUT_DIR/entry.png`, so repeated runs are byte-identical.

Rebuild the image:

```sh
python3 tools/render.py
```
