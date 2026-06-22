cd ~/fomo-index && cat > README.md << 'ENDOFFILE'
# FOMO Index — North American Behavioral Finance Dashboard

A real-time behavioral finance dashboard that measures how much of a stock market reaction to major North American events is driven by human psychology rather than fundamentals.

## What It Does

- Tracks 21 major market events from 2004–2026
- Calculates a FOMO Score (0–100) using Cumulative Abnormal Return (CAR) methodology
- Classifies the behavioral bias driving each market reaction (FOMO, Loss Aversion, Herd Behaviour, Anchoring, Availability Bias, Overconfidence, Recency Bias)
- Shows historical pattern matching — similar past events and what happened next
- Displays live stock prices for Canadian and US markets
- Calculates a live daily FOMO reading based on S&P 500 momentum and VIX volatility

## Methodology

The FOMO Score is calculated using Event Study Methodology (MacKinlay, 1997):

1. **Baseline** — Average closing price over 20 trading days before the event
2. **CAR** — (Actual Price − Baseline) / Baseline × 100
3. **Peak CAR** — Maximum absolute CAR in 20 trading days post-event
4. **FOMO Score** — min(|Peak CAR| × 3, 100)

### Academic Foundation
- Kahneman & Tversky (1979) — Prospect Theory (Nobel Prize 2002)
- MacKinlay (1997) — Event Studies in Economics and Finance
- Bikhchandani, Hirshleifer & Welch (1992) — Information Cascades
- Bonaparte (2025) — Global FOMO Index

## Events Covered

| Year | Event | FOMO Score | Bias |
|------|-------|------------|------|
| 2008 | Lehman Brothers Collapse | 96/100 | Loss Aversion |
| 2020 | COVID Black Monday | 98/100 | Loss Aversion |
| 2020 | TSX COVID Bottom | 97/100 | Loss Aversion |
| 2021 | GameStop Short Squeeze | 100/100 | FOMO |
| 2022 | Russia Invades Ukraine | 76/100 | Loss Aversion |
| 2023 | Silicon Valley Bank | 78/100 | Herd Behaviour |
| 2024 | Yen Carry Trade Unwind | 85/100 | Herd Behaviour |
| 2025 | Trump Liberation Day Tariffs | 88/100 | Loss Aversion |
| 2025 | Black Monday 2025 | 91/100 | Herd Behaviour |
| 2026 | AI Monetization Reality Check | 69/100 | Recency Bias |

## Tech Stack

- Python
- Streamlit
- Plotly
- yfinance
- pandas

## How to Run

```bash
pip install streamlit plotly pandas yfinance
streamlit run fomo_v4.py
```

## Disclaimer

Educational research tool only. Not financial advice. Always consult a licensed financial advisor before making investment decisions.

## Built By

**Gurasis Kaur**  
Financial Economics & Business, University of Waterloo (Class of 2029)  
FOMO Index
