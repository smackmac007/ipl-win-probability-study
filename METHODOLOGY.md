# Methodology

## 1. Data

- **Source:** Cricsheet ball-by-ball JSON for every men's T20 and T20I match it publishes. That is 10,763 matches and about 2.47 million deliveries, of which about 1,240 matches are IPL.
- **Why other leagues are included:** they help rate players, since most IPL players also play T20Is, the PSL, BBL, CPL, SA20 and so on. Non-IPL matches are down-weighted when models are trained.
- **Excluded:**
  - 100-ball formats (The Hundred), because overs have 5 balls.
  - No-results.
  - Ties decided by a Super Over, for the in-play model only.
- **Rain-reduced matches** are kept, using Cricsheet's recorded revised (DLS) target and overs.

### Data corrections made during the study

An audit found several problems, which were fixed before the final numbers were produced.

| Problem | Fix |
|---|---|
| At neutral venues the "home" team defaulted to the first-listed team, which is usually the side that batted first. That leaked toss information into the labels. | Neutral-venue teams are ordered alphabetically. Elo home advantage applies only when a team is genuinely at home. |
| Rain-reduced chases used target = first-innings runs + 1 over 20 overs. | The real revised target and overs are used. |
| "Retired hurt" and "retired not out" were counted as wickets. | Excluded. |
| Players were keyed by name spelling, so one player could have two ratings and two different players could share one. | Players are keyed on Cricsheet's registry id. |
| Player-rating baselines for a league's first seasons used an all-season average, which peeks at the future. | Those balls contribute no rating signal. |

## 2. Features

All features are **point-in-time**: a feature for a match uses only information available before that match (or, for in-play states, before that ball).

- **Player ratings.** For every delivery, the runs and wicket outcome is compared with the average for that league, innings and phase over the previous three seasons.
  - A player's rating is the exponentially decayed sum of those residuals (one-year half-life), shrunk towards zero for small samples.
  - Separate ratings exist for batting and bowling, in the powerplay, middle overs and death overs.
- **Team strength** comes from the playing XI's ratings: top-order and finishing batting, bowling runs saved, wicket-taking, the number of all-rounders and the number of unknown players.
- **Team Elo** uses season-to-season regression to the mean and a margin-of-victory adjustment.
- **Context:** recent form, net run rate, head-to-head, rest days, and venue scoring and chase-success history.
- **Match state (in-play):** runs, wickets, balls left, target, runs needed, current and required run rate.

## 3. Models

- **Pre-match:** gradient boosting (LightGBM) and logistic regression. Each is refit every 10 matches on all earlier matches, with "probable XI" (each team's last known XI) and no toss information. Temperature-scaled calibration is fitted on earlier seasons only.
- **In-play:** one LightGBM model over match states, with monotone constraints:
  - more runs needed must never raise the chasing side's win probability;
  - more wickets in hand must never lower it.
  - It is retrained each season on all earlier seasons.
  - Each checkpoint is calibrated with a temperature fitted on earlier seasons at the same checkpoint.
- **Checkpoints reported:**
  - before the toss;
  - after the toss;
  - end of overs 6, 10 and 15 of the first innings;
  - innings break;
  - end of overs 6, 10, 15 and 18 of the chase.

## 4. Evaluation

- **Walk-forward, predict-then-learn.** Matches are processed in date order. Each match is predicted first and only then added to the training history. The models never see the match they predict or anything after it.
- **Window:** IPL 2024, 2025 and 2026.
- **Metrics:**
  - log loss (0.693 = coin flip; lower is better);
  - accuracy;
  - calibration by confidence band.
- **Uncertainty:**
  - 95% intervals come from bootstrapping over matches, or Wilson intervals for win rates.
  - Model comparisons use paired bootstrap differences.
  - A change was accepted only if its interval excluded zero.

### Leakage tests

Each feature path has a "future-blind" test. The same prediction is computed twice: once with the full history, once with every later match deleted. The two must be identical. These tests cover:

- player ratings and ball-level ratings;
- team context and venue curves;
- the pre-match prior;
- the runs-distribution model;
- per-season calibration;
- the ball-outcome model;
- the conformal split.

All pass. A monotonicity probe confirms that the in-play model's constraints hold.

### Multiple testing

Many variants were compared on the same three seasons, which inflates the chance of a false "significant" result. A family-wise correction (Holm and max-T bootstrap, clustered by match) was applied. **None of the earlier individually significant improvements survived the correction**, so the results above are reported as descriptive, not as proven improvements between variants.

## 5. Tried and rejected

| Idea | Result |
|---|---|
| Runs-distribution features (predicted first-innings score quantiles) | Made the in-play model significantly worse, because it overfit to match identity. Removed. |
| All-league pre-match prior as an in-play feature | Neutral. |
| Impact Player era flag or re-weighting (2023+) | Scoring jumped about 22 runs from 2023, but model accuracy and calibration were unchanged, and no era adjustment helped. |
| Ball-by-ball Monte Carlo simulator, alone or blended with the in-play model | An early positive result did not survive the data corrections. The simulator underestimates modern IPL scoring. |
| Beating Elo pre-match | A model trained on shuffled labels "beat" Elo by the same margin, so it wasn't a real win. Elo is simply overconfident. |

## 6. Limitations

- **Sample size:** 215 matches is small, and single confidence bands often hold 20-60 matches.
- **Cutoff:** in-play states are taken at over boundaries only.
- **Impact players:** these substitutes (2023+) can't be separated from the starting XI in the source data.
- **Real XI in-play:** in-play predictions use the actual XI, which is known once the match starts.
- **Probable XI pre-match:** pre-match predictions use the probable XI.
- **Market comparison:** it covers one season (73 matches) and pre-match prices only.
