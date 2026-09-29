# How much does an IPL win-probability model actually know?

A walk-forward study of an IPL match-winner model at ten points in a match, from before the toss to the 18th over of the chase. For each point it answers two questions:

1. **When the model says X% confident, how often is it right?** (calibration, by confidence band)
2. **What would a ₹10,000 bankroll have done betting on it?** (a simulation only - see [DISCLAIMER.md](DISCLAIMER.md))

Evaluation window: **IPL 2024, 2025 and 2026** (215 decided matches). Every prediction was made using only matches played before it. The model was never trained on the match it predicts.

> **This is a research project, not betting advice.** Betting is illegal in many places, including most of India. Read [DISCLAIMER.md](DISCLAIMER.md) before anything else.

## Headline findings

- **Before the match, the model is no better than a coin flip.** Log loss 0.69-0.72 against 0.693 for 50/50, across every model tried (player ratings, team Elo, gradient boosting, logistic regression). It never reached 70% confidence before the toss. When it said 60-70%, the picked side won only 35% of the time (13/37).
- **The model becomes informative as the match unfolds.** Accuracy climbs from about 50% before the toss to 68% at the innings break, 81% at 10 overs into the chase and 90% at 18 overs.
- **High-confidence calls late in the chase hold up.** At 10 overs into the chase, picks at 90%+ confidence won 65/69 (94%). At 18 overs, 118/120 (98%).
- **The innings break is still overconfident at the top end.** Picks at 90%+ won only 16/21 (76%).
- **No betting edge was found.** Against real prediction-market prices (Polymarket, 73 matches of IPL 2026) the model lost money, with a confidence interval spanning zero. At "fair" odds, which assume the market prices exactly at the model's number, results cluster around break-even. That is the expected result for a calibrated model, not a money-making one.

## Accuracy by situation and confidence

How often the side the model favoured went on to win, counting every match where its confidence was at least the threshold.

| Situation | ≥50% (all) | ≥60% | ≥70% | ≥80% | ≥90% |
|---|---|---|---|---|---|
| Before the toss | 106/215 (49%) | 13/37 (35%) | none | none | none |
| After the toss | 100/215 (47%) | 13/29 (45%) | 1/4 | none | none |
| 1st innings, 6 overs | 129/215 (60%) | 71/115 (62%) | 30/43 (70%) | 7/9 (78%) | 2/2 |
| 1st innings, 10 overs | 127/215 (59%) | 88/137 (64%) | 41/59 (69%) | 15/19 (79%) | none |
| 1st innings, 15 overs | 144/213 (68%) | 106/148 (72%) | 71/93 (76%) | 37/47 (79%) | 5/6 |
| Innings break | 147/215 (68%) | 120/162 (74%) | 87/107 (81%) | 45/58 (78%) | 16/21 (76%) |
| Chase, 6 overs | 168/215 (78%) | 149/183 (81%) | 126/143 (88%) | 91/100 (91%) | 54/59 (92%) |
| Chase, 10 overs | 172/213 (81%) | 155/187 (83%) | 141/158 (89%) | 106/115 (92%) | 65/69 (94%) |
| Chase, 15 overs | 174/202 (86%) | 162/182 (89%) | 147/162 (91%) | 130/139 (94%) | 98/100 (98%) |
| Chase, 18 overs | 154/171 (90%) | 147/157 (94%) | 141/147 (96%) | 133/138 (96%) | 118/120 (98%) |

Fewer matches reach the later chase checkpoints because many chases finish early. Per-band results with 95% intervals are in [RESULTS.md](RESULTS.md).

### How to read a confidence number

"80% confident" means that over many matches where the model says 80%, the favoured side should win about 8 in 10. Even a well-calibrated model is wrong at 80% one time in five.

The questions to ask are:

- Does the stated confidence match the observed win rate?
- How often does the model get to be that confident at all?

Before the toss it almost never does. By the 18th over of a chase it usually does.

## Why this project

Most public IPL "prediction" projects report a single accuracy figure, often measured on matches the model was trained on. This study is stricter in three ways:

- **It measures honestly.** Every prediction uses only information available before the match or the ball it predicts. Automated tests prove that hiding future matches does not change any prediction.
- **It asks when the model knows something.** Instead of one number, it scores the model at ten stages of a match.
- **It checks confidence, not just accuracy.** A model that says 90% should be right about 90% of the time. That is what matters if anyone were to rely on it.

## How it works (short version)

1. **Data.** About 10,700 men's T20 matches (2.5 million deliveries) from Cricsheet. That covers the IPL plus other T20 leagues and internationals, which help rate players who appear in several competitions.
2. **Player ratings.** Every delivery is compared with the league average for that phase of the innings. Each player gets batting and bowling ratings for the powerplay, middle overs and death overs, weighted towards recent form.
3. **Team strength.** Built from the playing XI's ratings, plus team Elo, recent form, head-to-head record and venue history.
4. **Match state.** In-play, the model also sees the score, wickets, balls left, target and required run rate.
5. **Models.** Gradient boosting (LightGBM) with calibration. The in-play model has built-in rules: needing more runs, or having fewer wickets in hand, can never raise the chasing side's chances.
6. **Evaluation.** Matches are replayed in date order. Each is predicted first, then added to the history. The models are retrained only on the past.

Full details are in [METHODOLOGY.md](METHODOLOGY.md).

## Betting simulation in one table

Hypothetical only (see [DISCLAIMER.md](DISCLAIMER.md)). The simulation starts with ₹10,000, bets a flat ₹1,000 on the model's pick whenever its confidence is at least the threshold, and pays at "fair" odds equal to the model's own probability. Figures are the final bankroll.

| Situation | ≥50% | ≥60% | ≥70% | ≥80% | ≥90% |
|---|---|---|---|---|---|
| Before the toss | -₹13,219 | -₹6,389 | no bets | no bets | no bets |
| Innings break | ₹3,570 | ₹6,700 | ₹10,301 | ₹2,932 | ₹6,014 |
| Chase, 10 overs | ₹11,969 | ₹6,874 | ₹14,506 | ₹10,957 | ₹9,557 |
| Chase, 18 overs | ₹9,796 | ₹11,234 | ₹11,863 | ₹10,209 | ₹10,948 |

- **Before the match:** every strategy lost, and betting on every match went bust.
- **Later in the match:** results scatter around ₹10,000. That is what luck around break-even looks like, not an edge.
- **High confidence pays little:** at 90%+ confidence a win pays only about ₹50-100, so one loss cancels 10-20 wins.
- **Against real Polymarket prices:** the model lost money, with a -6% return on 43 pre-match bets.

Every checkpoint and the real-price comparison are in [BETTING_SIMULATION.md](BETTING_SIMULATION.md).

## What was tried and did not help

- **Predicted-score features** (expected first-innings runs): made the in-play model worse, because it overfit.
- **An "Impact Player era" adjustment:** scoring rose by about 22 runs from 2023, but the model's accuracy did not change, and no adjustment helped.
- **A ball-by-ball Monte Carlo simulator,** alone or blended with the main model: an early gain disappeared once data errors were fixed. The simulator underestimates modern IPL scoring.
- **Claims of beating Elo before the match:** a model trained on shuffled results beat Elo by the same margin. Elo is simply overconfident; no model beat it on skill.
- **Multiple-testing check:** many variants were compared on the same three seasons. After correcting for that, none of the earlier "significant" improvements held up.

Negative results are reported deliberately. They are as informative as the positive ones.

## Limitations

- **Small sample.** 215 matches is small; individual confidence bands often hold only 20-60 matches.
- **Over boundaries only.** In-play predictions are made at over boundaries, not ball by ball.
- **Impact players.** From 2023, these substitutes can't be told apart from the starting XI in the source data.
- **Limited market comparison.** One season only (73 matches), pre-match prices only.
- **Unconfirmed on future seasons.** Results may not hold for future seasons.

## Contents

| File | What it holds |
|---|---|
| [METHODOLOGY.md](METHODOLOGY.md) | Data, features, models, walk-forward evaluation, leakage checks, what was tried and rejected |
| [RESULTS.md](RESULTS.md) | Calibration by confidence band at every checkpoint, with confidence intervals |
| [BETTING_SIMULATION.md](BETTING_SIMULATION.md) | The ₹10,000 bankroll simulation at fair odds and at real market prices |
| [DISCLAIMER.md](DISCLAIMER.md) | Legal and financial disclaimer |
| `scripts/build_tables.py` | Regenerates the summary tables locally from the private pipeline (outputs are not committed) |

## Data credit

Ball-by-ball data: [Cricsheet](https://cricsheet.org), released under the Open Data Commons Attribution License. Market prices: Polymarket public API. This repository contains no raw data - only the aggregated summary tables shown in these documents.
