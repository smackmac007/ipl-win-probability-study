"""
Regenerate every table in results/ from the main pipeline's saved predictions.

Needs the private pipeline checkout (default ../ipl_json, override with IPL_JSON=path).
Reads only walk-forward predictions (each made before the match / state it scores);
no model is refit here.

Usage:
    python3 scripts/build_tables.py
"""

import os
import sys
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parents[1]
PIPELINE = Path(os.environ.get('IPL_JSON', HERE.parent / 'ipl_json')).resolve()
sys.path.insert(0, str(PIPELINE))
os.chdir(PIPELINE)

from src.evaluation import bankroll_sim as bs  # noqa: E402

OUT = HERE / 'results'
SEASONS = [2024, 2025, 2026]
CHECKPOINTS = [
    ('prematch', 'Before the toss'),
    ('start', 'After the toss, 0 balls'),
    ('pp6', '1st innings, 6 overs'),
    ('pp10', '1st innings, 10 overs'),
    ('pp15', '1st innings, 15 overs'),
    ('break', 'Innings break'),
    ('chase6', 'Chase, 6 overs'),
    ('chase10', 'Chase, 10 overs'),
    ('chase15', 'Chase, 15 overs'),
    ('chase18', 'Chase, 18 overs'),
]
BANDS = [(0.5, 0.6), (0.6, 0.7), (0.7, 0.8), (0.8, 0.9), (0.9, 1.01)]
START, STAKE = 10_000.0, 1_000.0


def wilson(k: int, n: int, z: float = 1.96):
    if n == 0:
        return (np.nan, np.nan)
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * np.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (c - h, c + h)


def picks(df: pd.DataFrame) -> pd.DataFrame:
    conf = np.maximum(df['p_home'], 1 - df['p_home'])
    won = np.where(df['p_home'] >= 0.5, df['home_won'] == 1, df['home_won'] == 0)
    return df.assign(conf=conf, won=won)


def reliability(d: pd.DataFrame, cp: str, label: str):
    rows = []
    for lo, hi in BANDS:
        s = d[(d['conf'] >= lo) & (d['conf'] < hi)]
        k, n = int(s['won'].sum()), len(s)
        a, b = wilson(k, n)
        rows.append({'checkpoint': cp, 'situation': label, 'band': f'{lo:.0%}-{min(hi, 1):.0%}',
                     'matches': n, 'avg_confidence': s['conf'].mean() if n else np.nan,
                     'picked_side_won': k, 'win_rate': k / n if n else np.nan,
                     'ci_low': a, 'ci_high': b})
    cum = []
    for t in (0.5, 0.6, 0.7, 0.8, 0.9):
        s = d[d['conf'] >= t]
        k, n = int(s['won'].sum()), len(s)
        a, b = wilson(k, n)
        cum.append({'checkpoint': cp, 'situation': label, 'threshold': f'>={t:.0%}',
                    'matches': n, 'share_of_matches': n / len(d),
                    'avg_confidence': s['conf'].mean() if n else np.nan,
                    'picked_side_won': k, 'win_rate': k / n if n else np.nan,
                    'ci_low': a, 'ci_high': b})
    return rows, cum


def bankroll(df: pd.DataFrame, cp: str, label: str, **kw):
    g = bs.grid(df, START, STAKE, thresholds=(0.5, 0.6, 0.7, 0.8, 0.9), **kw)
    lows = []
    for t in (0.5, 0.6, 0.7, 0.8, 0.9):
        bets = bs.simulate(df, t, START, STAKE, **{k: v for k, v in kw.items() if k != 'n_boot'})
        lows.append(min([START] + [b.bankroll_after for b in bets]))
    return g.assign(checkpoint=cp, situation=label, lowest_bankroll=lows)


def main():
    OUT.mkdir(exist_ok=True)
    rel, cum, fair = [], [], []
    for cp, label in CHECKPOINTS:
        df = bs.load_checkpoint(cp, SEASONS)
        d = picks(df)
        r, c = reliability(d, cp, label)
        rel += r
        cum += c
        fair.append(bankroll(df, cp, label))
        print(f'{cp:9} {len(df)} matches')
    pd.DataFrame(rel).to_csv(OUT / 'reliability_by_band.csv', index=False, float_format='%.4f')
    pd.DataFrame(cum).to_csv(OUT / 'accuracy_by_threshold.csv', index=False, float_format='%.4f')
    pd.concat(fair).to_csv(OUT / 'bankroll_fair_odds.csv', index=False, float_format='%.4f')

    pm = bs.load_polymarket(SEASONS)
    mk = bankroll(pm, 'prematch', 'Before the toss, vs Polymarket price', n_boot=5000)
    mk.to_csv(OUT / 'bankroll_polymarket.csv', index=False, float_format='%.4f')
    print(f'polymarket {len(pm)} matches')


if __name__ == '__main__':
    main()
