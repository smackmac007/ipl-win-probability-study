# Results: calibration by confidence band

- **Scope:** IPL 2024-26, walk-forward. "Confidence" is the model's probability for the side it favoured, and "won" means that side won.
- **Reading a row:** a well-calibrated model's win rate should be close to its average confidence.
- **Intervals:** 95% Wilson intervals. Bands with few matches are shown but carry wide intervals.

## Before the match

| Situation | Band | Matches | Avg confidence | Won | Win rate | 95% CI |
|---|---|---|---|---|---|---|
| Before the toss | 50-60% | 178 | 54% | 93 | 52% | 45-59% |
| | 60-70% | 37 | 63% | 13 | **35%** | 22-51% |
| After the toss | 50-60% | 186 | 52% | 87 | 47% | 40-54% |
| | 60-70% | 25 | 64% | 12 | 48% | 30-66% |
| | 70-80% | 4 | 73% | 1 | 25% | 5-70% |

Before a ball is bowled the model has no measurable skill. Its rarer 60-70% calls did worse than a coin flip. IPL parity (auction, salary cap) leaves very little signal before the match.

## First innings

| Situation | Band | Matches | Avg confidence | Won | Win rate | 95% CI |
|---|---|---|---|---|---|---|
| 6 overs | 50-60% | 100 | 55% | 58 | 58% | 48-67% |
| | 60-70% | 72 | 64% | 41 | 57% | 45-68% |
| | 70-80% | 34 | 73% | 23 | 68% | 51-81% |
| | 80-90% | 7 | 83% | 5 | 71% | 36-92% |
| | 90-100% | 2 | 90% | 2 | 100% | 34-100% |
| 10 overs | 50-60% | 78 | 55% | 39 | 50% | 39-61% |
| | 60-70% | 78 | 65% | 47 | 60% | 49-70% |
| | 70-80% | 40 | 74% | 26 | 65% | 50-78% |
| | 80-90% | 19 | 84% | 15 | 79% | 57-91% |
| 15 overs | 50-60% | 65 | 56% | 38 | 58% | 46-70% |
| | 60-70% | 55 | 65% | 35 | 64% | 50-75% |
| | 70-80% | 46 | 75% | 34 | 74% | 60-84% |
| | 80-90% | 41 | 84% | 32 | 78% | 63-88% |
| | 90-100% | 6 | 92% | 5 | 83% | 44-97% |

## Innings break

| Band | Matches | Avg confidence | Won | Win rate | 95% CI |
|---|---|---|---|---|---|
| 50-60% | 53 | 55% | 27 | 51% | 38-64% |
| 60-70% | 55 | 64% | 33 | 60% | 47-72% |
| 70-80% | 49 | 75% | 42 | 86% | 73-93% |
| 80-90% | 37 | 85% | 29 | 78% | 63-89% |
| 90-100% | 21 | 94% | 16 | **76%** | 55-89% |

The top band is overconfident: it claimed 94% and delivered 76%. The model knows the first-innings total but not how the pitch will play for the chase.

## Chase

| Situation | Band | Matches | Avg confidence | Won | Win rate | 95% CI |
|---|---|---|---|---|---|---|
| 6 overs | 50-60% | 32 | 55% | 19 | 59% | 42-74% |
| | 60-70% | 40 | 64% | 23 | 57% | 42-71% |
| | 70-80% | 43 | 75% | 35 | 81% | 67-90% |
| | 80-90% | 41 | 85% | 37 | 90% | 77-96% |
| | 90-100% | 59 | 95% | 54 | 92% | 82-96% |
| 10 overs | 50-60% | 26 | 55% | 17 | 65% | 46-81% |
| | 60-70% | 29 | 65% | 14 | 48% | 31-66% |
| | 70-80% | 43 | 75% | 35 | 81% | 67-90% |
| | 80-90% | 46 | 87% | 41 | 89% | 77-95% |
| | 90-100% | 69 | 95% | 65 | 94% | 86-98% |
| 15 overs | 50-60% | 20 | 54% | 12 | 60% | 39-78% |
| | 60-70% | 20 | 65% | 15 | 75% | 53-89% |
| | 70-80% | 23 | 75% | 17 | 74% | 54-87% |
| | 80-90% | 39 | 85% | 32 | 82% | 67-91% |
| | 90-100% | 100 | 97% | 98 | 98% | 93-99% |
| 18 overs | 50-60% | 14 | 55% | 7 | 50% | 27-73% |
| | 60-70% | 10 | 66% | 6 | 60% | 31-83% |
| | 70-80% | 9 | 75% | 8 | 89% | 56-98% |
| | 80-90% | 18 | 86% | 15 | 83% | 61-94% |
| | 90-100% | 120 | 98% | 118 | 98% | 94-100% |

From 6 overs into the chase onward, high-confidence calls are close to calibrated.

## Summary

| Situation | Accuracy (all matches) | Where it is reliable |
|---|---|---|
| Before / after the toss | 47-49% | Nowhere; indistinguishable from a coin flip |
| 1st innings, 6-15 overs | 59-68% | Weakly; bands track confidence loosely |
| Innings break | 68% | Up to about 80%; top band overconfident |
| Chase, 6-10 overs | 78-81% | 70%+ bands roughly calibrated |
| Chase, 15-18 overs | 86-90% | 90%+ band wins about 98% |
