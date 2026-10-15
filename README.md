# APEX Crypto Bot

APEX is a self-improving crypto trading bot written in Python. It uses a
5-layer signal architecture (Momentum + Arbitrage + ML + Sentiment +
OrderFlow + Meta-Learner) to make automated trading decisions on Coinbase.

## Files

- **`bot.py`** — the main trading engine.
- **`log_shipper.py`** — tails the bot's log file and ships new lines to the dashboard.
- **`requirements.txt`** — Python dependencies.

## Setup

```bash
pip install -r requirements.txt
```

The bot reads Coinbase credentials from `cdp_api_key.json` or from
environment variables (`COINBASE_API_KEY`, `COINBASE_API_SECRET`). These
secrets are **never** committed to this repo (see `.gitignore`).

## Running

```bash
python bot.py
```

## Branches

- **`main`** — stable code. Do not push directly.
- **`test`** — all automated fixes land here first for review before merging.
