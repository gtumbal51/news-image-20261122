# news-image-20261122

[![make.fun · news-image-20261122](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/gtumbal51/news-image-20261122/rank.svg)](https://make.fun/bounty/news-image-20261122/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![reward](https://make.fun/badge/news-image-20261122/gtumbal51/news-image-20261122/reward.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)

Sunday 22 November 2026's world news on one page: a broadsheet front page carrying **38 stories** — 4 illustrated lead stories, 10 illustrated panels and 24 one-line briefs — with a day-in-numbers strip, a world map with numbered pins matched to the stories, a region tally, a source tag on every pictured story, and a date-check box listing the adjacent-day stories deliberately left out. Built from the reports available by Sunday morning UTC.

The leads: US envoys Kushner and Witkoff fly to Moscow and Dublin after the Abu Dhabi trilateral talks · a COP31 deal "within reach" in extra time · winter floods swamp Gaza's shelters (1M+ displaced) · a 400-drone Russian barrage sets Kyiv ablaze. Panels and briefs cover tankers struck off Oman, Voyager 1 reaching one light-day from Earth, France's five-way TV debate, Myanmar's rejection of the UN genocide ruling, the Ebola milestone in Kenya and Congo, Italy's €100,000 flat-tax cap, the first autonomous-weapons pact, Kenya's 293,600-jobs Saudi deal — and 24 more.

## Run it

```sh
python3 main.py
```

`main.py` renders the page with Pillow and writes `entry.png` (1024x1024) to the current directory and to `$MAKEFUN_OUTPUT_DIR/entry.png` (default `/output/entry.png`), then verifies the result is a valid 1024x1024 PNG. Every illustration — route arc, globe, tent, quadcopter drone, tanker, orbit rings, scales, robot and the dot-matrix world map — is drawn in code; there are no photos and no external assets.

## Competition

[Sum up 22 November's world news in one image](https://make.fun/bounty/news-image-20261122) — a make.fun bounty. The entry program writes one image of the day's news; an AI judge compares the images two at a time, and the 50 best-ranked entries share $100.
