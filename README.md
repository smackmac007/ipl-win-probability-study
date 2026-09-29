# How much does an IPL win-probability model actually know?

A study of an IPL match-winner model on the **IPL 2026 tournament**, at ten points in a match, from before the toss to the 18th over of the chase. For each point it answers two questions:

1. **When the model says X% confident, how often is it right?** (calibration, by confidence band)
2. **What would a ₹10,000 bankroll have done betting on it through IPL 2026?** (a simulation only - see [DISCLAIMER.md](DISCLAIMER.md))

**Test set: IPL 2026 only** (73 decided matches; one no-result excluded).
- The models were trained on matches played before each prediction: other T20 leagues and internationals, plus earlier IPL seasons.
- The in-play model was trained on seasons up to 2025.
- No 2026 result was used to predict itself.

> **This is a research project, not betting advice.** Betting is illegal in many places, including most of India. Read [DISCLAIMER.md](DISCLAIMER.md) before anything else.

## Headline findings (IPL 2026)

- **Before the match, the model was no better than a coin flip.**
  - Every model tried scored a log loss of 0.69-0.74, against 0.693 for a 50/50 guess. That covers player ratings, team Elo, gradient boosting and logistic regression.
  - The favoured side won 35 of 73 matches (48%).
  - The model never reached 70% confidence before the toss. Its 60%+ picks won only 2 of 9.
- **The model became informative as the match unfolded.** Accuracy climbed from 48% before the toss to 62% at the innings break, 83% at 10 overs into the chase and 93% at 18 overs.
- **High-confidence calls in the chase held up.** Every pick at 90%+ confidence from 6 overs into the chase onward was right:
  - 16/16 at 6 overs;
  - 20/20 at 10 overs;
  - 35/35 at 15 overs;
  - 36/36 at 18 overs.
- **The innings break was overconfident.** Picks at 80%+ won only 12/18 (67%).
- **No real betting edge was found.**
  - Against real prediction-market prices before the toss (Polymarket), the model lost money.
  - In the ₹10,000 simulation, betting before the match or at the innings break lost money.
  - Chase-stage bets ended in profit only at "fair" odds, which assume someone prices exactly at the model's own number. That is not a real-world edge.

## Accuracy by situation and confidence (IPL 2026)

How often the side the model favoured went on to win, counting every match where its confidence was at least the threshold.

| Situation | ≥50% (all) | ≥60% | ≥70% | ≥80% | ≥90% |
|---|---|---|---|---|---|
| Before the toss | 35/73 (48%) | 2/9 (22%) | none | none | none |
| After the toss | 35/73 (48%) | none | none | none | none |
| 1st innings, 6 overs | 41/73 (56%) | 23/42 (55%) | 12/20 (60%) | 1/1 | 1/1 |
| 1st innings, 10 overs | 43/73 (59%) | 29/51 (57%) | 9/14 (64%) | 3/3 | none |
| 1st innings, 15 overs | 44/72 (61%) | 33/49 (67%) | 24/33 (73%) | 10/14 (71%) | 1/1 |
| Innings break | 45/73 (62%) | 38/56 (68%) | 28/38 (74%) | 12/18 (67%) | 2/3 |
| Chase, 6 overs | 59/73 (81%) | 53/65 (82%) | 46/50 (92%) | 32/33 (97%) | 16/16 (100%) |
| Chase, 10 overs | 60/72 (83%) | 52/62 (84%) | 48/52 (92%) | 37/38 (97%) | 20/20 (100%) |
| Chase, 15 overs | 62/69 (90%) | 59/64 (92%) | 53/57 (93%) | 46/47 (98%) | 35/35 (100%) |
| Chase, 18 overs | 54/58 (93%) | 52/53 (98%) | 49/50 (98%) | 46/47 (98%) | 36/36 (100%) |

- Percentages are omitted for cells with fewer than 5 matches.
- Fewer matches reach the later chase checkpoints because many chases finish early.
- [RESULTS.md](RESULTS.md) has band-by-band results with 95% intervals, pooled over IPL 2024-26 for a larger sample.

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

## Betting simulation: IPL 2026 tournament

Hypothetical only (see [DISCLAIMER.md](DISCLAIMER.md)).

**Setup:**
- The bankroll starts at ₹10,000 at the first match. Matches are taken in date order, with at most one bet per match.
- A flat ₹2,000 goes on the model's pick whenever its confidence is at least the threshold.
- Payout is at the model's own probability, with winnings cut by 5% to mimic a bookmaker margin.
- Betting stops if the bankroll hits zero.

Final bankroll after the tournament:

| When the bet is placed | ≥50% | ≥60% | ≥70% | ≥80% | ≥90% |
|---|---|---|---|---|---|
| Before the toss | bust | bust | no bets | no bets | no bets |
| Innings break | bust | bust | ₹3,634 | ₹1,397 | ₹8,279 |
| Chase, 10 overs | ₹16,667 | ₹8,407 | ₹16,488 | ₹15,660 | ₹12,413 |
| Chase, 18 overs | ₹14,738 | ₹17,441 | ₹14,532 | ₹12,529 | ₹11,695 |

- **Before the match and at the innings break:** betting lost money, and several strategies went bust.
- **Chase-stage strategies ended in profit in 2026, but that is not an edge.** The payout assumes someone prices exactly at the model's number. The profit comes from the model being too cautious late in chases (for example 37 of 38 wins at about 87% average confidence), not from beating a real market. It is one season, not repeatable evidence.
- **Against real Polymarket prices before the toss:** the model lost money, with a -6% return on 43 bets (₹10,000 down to ₹4,647).

All checkpoints, the 2,000-run luck analysis and the real-price comparison are in [BETTING_SIMULATION.md](BETTING_SIMULATION.md).

## What was tried and did not help

- **Predicted-score features** (expected first-innings runs): made the in-play model worse, because it overfit.
- **An "Impact Player era" adjustment:** scoring rose by about 22 runs from 2023, but the model's accuracy did not change, and no adjustment helped.
- **A ball-by-ball Monte Carlo simulator,** alone or blended with the main model: an early gain disappeared once data errors were fixed. The simulator underestimates modern IPL scoring.
- **Claims of beating Elo before the match:** a model trained on shuffled results beat Elo by the same margin. Elo is simply overconfident; no model beat it on skill.
- **Multiple-testing check:** many variants were compared during development. After correcting for that, none of the apparent "significant" improvements held up.

Negative results are reported deliberately. They are as informative as the positive ones.

## Limitations

- **Small sample.** One tournament is 73 matches. Many confidence bands hold fewer than 20, so single cells can swing a lot by chance.
- **Over boundaries only.** In-play predictions are made at over boundaries, not ball by ball.
- **Impact players.** From 2023, these substitutes can't be told apart from the starting XI in the source data.
- **Limited market comparison.** Pre-match prices only; no real in-play prices were tested.
- **One season.** Design choices were made after seeing results that included 2026, so this is close to, but not exactly, an untouched test. IPL 2027 predictions logged in advance would be the cleanest check.

## Contents

| File | What it holds |
|---|---|
| [METHODOLOGY.md](METHODOLOGY.md) | Data, features, models, walk-forward evaluation, leakage checks, what was tried and rejected |
| [RESULTS.md](RESULTS.md) | Calibration by confidence band at every checkpoint, with confidence intervals |
| [BETTING_SIMULATION.md](BETTING_SIMULATION.md) | The ₹10,000 bankroll simulation for IPL 2026: per-checkpoint results, 2,000-run luck analysis, real market prices |
| [DISCLAIMER.md](DISCLAIMER.md) | Legal and financial disclaimer |
| `scripts/build_tables.py` | Regenerates the summary tables locally from the private pipeline (outputs are not committed) |

## Data credit

Ball-by-ball data: [Cricsheet](https://cricsheet.org), released under the Open Data Commons Attribution License. Market prices: Polymarket public API. This repository contains no raw data - only the aggregated summary tables shown in these documents.
