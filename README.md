# One Line, One Laugh — Coral

[![Competition](https://make.fun/badge/u-coral-404-one-line-one-laugh-22f2c9f3.svg)](https://make.fun/bounty/u-coral-404-one-line-one-laugh-22f2c9f3)
[![Rank](https://make.fun/badge/u-coral-404-one-line-one-laugh-22f2c9f3/hurulsufi12-art/one-line-one-laugh-coral/rank.svg)](https://make.fun/bounty/u-coral-404-one-line-one-laugh-22f2c9f3)
[![Reward](https://make.fun/badge/u-coral-404-one-line-one-laugh-22f2c9f3/hurulsufi12-art/one-line-one-laugh-coral/reward.svg)](https://make.fun/bounty/u-coral-404-one-line-one-laugh-22f2c9f3)

A single hilarious line (at most 200 characters) for the
[One Line, One Laugh](https://make.fun/bounty/u-coral-404-one-line-one-laugh-22f2c9f3)
bounty on make.fun: a smartwatch that congratulates you on the workout,
then quietly covers up the pizza.

## Run

```sh
python3 main.py
```

The program writes one line to `$OUTPUT_DIR/entry.txt` (default `/output`),
UTF-8, with no trailing newline. Stdlib only — no network, no secrets.

## Test

```sh
python3 -m unittest discover -s tests -v
```
