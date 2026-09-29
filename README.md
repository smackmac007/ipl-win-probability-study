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
