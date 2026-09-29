# Betting simulation: IPL 2026 only

> **Hypothetical only.** No money was bet. This simulation tests whether the model's confidence can be trusted; it is not a strategy. Read [DISCLAIMER.md](DISCLAIMER.md).

## Why only 2026

IPL 2026 is the cleanest test available. Every 2026 prediction came from models trained only on matches played before it:

- the in-play model was trained on seasons up to 2025;
- the pre-match model was refit every 10 matches on earlier results only;
- no 2026 result was used to predict itself.

**One caveat.** Design choices, such as which features to keep, were made after looking at results that included 2026. The test is therefore close to, but not exactly, a fully untouched hold-out. A truly untouched test needs predictions logged before IPL 2027.

## Method

- **Tournament:** 73 decided matches of IPL 2026 (one no-result excluded), in date order.
- **Bankroll:** start with ₹10,000 at the first match.
- **Bet rule:** at a chosen point in the match, bet on the side the model favours if its confidence is at least the threshold.
  - At most one bet per match.
  - Each row below is a separate strategy, so rows don't add up.
- **Stake:** flat ₹2,000 per bet (20% of the starting bankroll).
- **Stop rule:** betting stops if the bankroll reaches ₹0 (bust).
- **Payout:** three assumptions.
  1. **Fair odds.** Paid at the model's own probability; at 80% confidence, a win pays ₹500 on ₹2,000. There is no bookmaker margin, so this is the most generous case.
  2. **5% margin.** Fair odds with winnings cut by 5%, closer to a real bookmaker.
  3. **Real market price.** The Polymarket price about 5 minutes before the start. This is available before the toss only.
- **Repeat simulations:** 2,000 re-runs per strategy. Each re-run redraws the season's qualifying bets at random, with repeats allowed. This shows how much luck moves the final bankroll.

## Result 1: final bankroll at the end of IPL 2026 (flat ₹2,000, 5% margin)

| When the bet is placed | ≥50% | ≥60% | ≥70% | ≥80% | ≥90% |
|---|---|---|---|---|---|
| Before the toss | **bust** (73 bets) | **bust** (9) | no bets | no bets | no bets |
| After the toss | **bust** (73) | no bets | no bets | no bets | no bets |
| 1st innings, 6 overs | **bust** (73) | **bust** (42) | ₹446 (20) | ₹10,206 (1) | ₹10,206 (1) |
| 1st innings, 10 overs | **bust** (73) | **bust** (51) | ₹4,913 (14) | ₹11,149 (3) | no bets |
| 1st innings, 15 overs | **bust** (72) | **bust** (49) | ₹4,745 (33) | ₹5,266 (14) | ₹10,105 (1) |
| Innings break | **bust** (73) | **bust** (56) | ₹3,634 (38) | ₹1,397 (18) | ₹8,279 (3) |
| Chase, 6 overs | ₹15,503 (73) | ₹10,169 (65) | **₹18,184** (50) | ₹15,104 (33) | ₹11,850 (16) |
| Chase, 10 overs | ₹16,667 (72) | ₹8,407 (62) | ₹16,488 (52) | ₹15,660 (38) | ₹12,413 (20) |
| Chase, 15 overs | ₹16,636 (69) | ₹15,674 (64) | ₹11,782 (57) | ₹13,382 (47) | ₹12,238 (35) |
| Chase, 18 overs | ₹14,738 (58) | **₹17,441** (53) | ₹14,532 (50) | ₹12,529 (47) | ₹11,695 (36) |

- Numbers in brackets are the bets placed.
- At fair odds (no margin), results are slightly better; for example, chase 10 overs at ≥80% ends at ₹16,063.
- A ₹2,000 stake is 20% of the starting bankroll. That doubles both gains and losses compared with ₹1,000, so many more strategies go bust.

## Result 2: how much of it is luck (2,000 re-runs, flat ₹2,000, 5% margin)

| Strategy | Actual 2026 result | Chance of ending in profit | 90% range of outcomes | Chance of going bust |
|---|---|---|---|---|
| Before the toss, ≥50% | bust | 8% | ₹0 to ₹14,666 | 88% |
| Innings break, ≥70% | ₹3,634 | 17% | ₹0 to ₹14,650 | 41% |
| Chase 6 overs, ≥70% | ₹18,184 | 95% | ₹10,100 to ₹25,321 | 0% |
| Chase 10 overs, ≥70% | ₹16,488 | 91% | ₹8,462 to ₹23,409 | 0% |
| Chase 10 overs, ≥80% | ₹15,660 | 99% | ₹11,612 to ₹18,650 | 0% |
| Chase 15 overs, ≥80% | ₹13,382 | 93% | ₹9,291 to ₹16,260 | 0% |

## Result 3: against real market prices (Polymarket, before the toss)

A bet is placed only when the model's probability is higher than the market's. Payout is at the market price.

| Strategy | Bets | Won | Final bankroll | Return on money bet | 95% range of return |
|---|---|---|---|---|---|
| Model above market, confidence ≥50% | 43 | 19 | ₹4,647 | -6% | -37% to +27% |
| Model above market, confidence ≥60% | 8 | 2 | ₹1,543 | -53% | -100% to +3% |

Brier score (lower is better): model 0.264, market 0.253, coin flip 0.250.

## What this means

- **Before the match and in the first innings, betting lost money in 2026,** and several strategies went bust. The model has no useful pre-match skill.
- **From the innings break, confidence and profit diverge.** The model's picks win often (about 74% at ≥70%), yet the bankroll still falls. That checkpoint is overconfident.
- **Chase-stage strategies made money in 2026 at fair odds,** roughly +₹2,000 to +₹8,000 on ₹10,000. This does not prove an edge:
  - **It reflects underconfidence, not an edge.** "Fair odds" means a counterparty prices exactly at the model's own number. The profit comes from the model being underconfident in the 2026 chases, for example 37 of 38 wins at an average of about 87% confidence. That shows the model is too cautious late in a chase, not that it beats the market.
  - **No real in-play prices were tested.** Real in-play prices already reflect the live score, so a bettor would not be offered the model's price. No free source of ball-by-ball timestamps was available to line up the model with real in-play prices, so this was not tested.
  - **2026 is out of line with other years.** In 2024 and 2025 the same chase strategies ended both above and below ₹10,000, so a profit in one season is not repeatable evidence.
- **Against a real market price before the toss, the model lost money.**

**Bottom line: nothing here shows a way to make money betting on IPL matches.**
