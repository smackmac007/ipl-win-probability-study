# Betting simulation

> **Hypothetical only.** No money was bet. This is a way to test whether the model's confidence can be trusted. It is not a strategy. Read [DISCLAIMER.md](DISCLAIMER.md).

## Setup

- **Bankroll:** start with ₹10,000.
- **Walk:** go through IPL 2024-26 in date order.
- **When to bet:** whenever the model's confidence at a given point in the match is at least the threshold.
- **Stake:** a flat ₹1,000 on the side it favours.
- **Bets per match:** one per match per simulation. Each row is a separate strategy, not additive.
- **No stop at zero:** the simulation does not stop when the bankroll hits zero. A negative "lowest" means the strategy would have gone bust.

Two payout assumptions:

1. **Fair odds.** You are paid at exactly the model's own probability; at 80% confidence a win pays ₹250 on ₹1,000. This is the most generous assumption possible, because no bookmaker margin applies. A perfectly calibrated model should break even here, so profit or loss mostly measures calibration error plus luck.
2. **Real market prices.** Payout is at the Polymarket price about 5 minutes before the start. This is available for 73 IPL 2026 matches, pre-match only. A bet is placed only when the model's probability is above the market's.

## Fair odds: final bankroll from ₹10,000

| Situation | ≥50% | ≥60% | ≥70% | ≥80% | ≥90% |
|---|---|---|---|---|---|
| Before the toss | **-₹13,219** (215 bets) | **-₹6,389** (37) | no bets | no bets | no bets |
| After the toss | **-₹16,564** (215) | ₹1,319 (29) | ₹7,313 (4) | no bets | no bets |
| 1st innings, 6 overs | ₹4,296 (215) | -₹1,244 (115) | ₹6,819 (43) | ₹9,183 (9) | ₹10,210 (2) |
| 1st innings, 10 overs | -₹8,674 (215) | -₹1,479 (137) | ₹3,881 (59) | ₹8,800 (19) | no bets |
| 1st innings, 15 overs | ₹8,310 (213) | ₹4,597 (148) | ₹6,021 (93) | ₹6,383 (47) | ₹9,459 (6) |
| Innings break | ₹3,570 (215) | ₹6,700 (162) | ₹10,301 (107) | ₹2,932 (58) | ₹6,014 (21) |
| Chase, 6 overs | **₹12,642** (215) | ₹10,133 (183) | **₹13,976** (143) | ₹10,475 (100) | ₹7,994 (59) |
| Chase, 10 overs | **₹11,969** (213) | ₹6,874 (187) | **₹14,506** (158) | ₹10,957 (115) | ₹9,557 (69) |
| Chase, 15 overs | **₹14,745** (202) | ₹12,626 (182) | ₹9,676 (162) | ₹9,987 (139) | ₹11,382 (100) |
| Chase, 18 overs | ₹9,796 (171) | ₹11,234 (157) | ₹11,863 (147) | ₹10,209 (138) | ₹10,948 (120) |

Negative figures mean the strategy lost more than the starting ₹10,000.

**What this shows:**

- **Before the match, every strategy lost money, and betting on everything went bust.** That fits the model having no pre-match skill.
- **Later in the match, results scatter around ₹10,000.** The best cell, ₹14,506 at chase 10 overs ≥70%, is +₹4,506 on ₹158,000 staked, about +3% return on money bet. That is within the range luck produces over 150-200 bets. Neighbouring thresholds at the same checkpoint lost money.
- **High confidence does not mean high profit.** At 90%+ a win pays only about 5-10% of the stake, so a single loss wipes out 10-20 wins.

## Real market prices (Polymarket, IPL 2026, before the toss)

| Strategy | Bets | Won | Final bankroll | Return on money bet | 95% CI on return |
|---|---|---|---|---|---|
| Model above market, confidence ≥50% | 43 | 19 | ₹7,323 | -6% | -37% to +27% |
| Model above market, confidence ≥60% | 8 | 2 | ₹5,771 | -53% | -100% to +3% |
| ≥70% and above | 0 | - | ₹10,000 | - | - |

Model vs market over the same matches, by Brier score (lower is better): model 0.264, market 0.253, coin flip 0.250. The market was no better than a coin flip either, and the model was slightly worse than the market. With 73 matches, neither difference is statistically significant.

## Bottom line

**There is no evidence this model can make money from betting.**

- **Pre-match:** it has no skill.
- **In-play at fair odds:** it roughly breaks even, which is the best a calibrated model can do at fair odds.
- **Real prices:** a real bookmaker or exchange adds a margin (typically 2-10%) and moves prices faster than an over-by-over model. Any break-even strategy at fair odds becomes a losing one.
- **Real pre-match prices:** the model lost against them.
