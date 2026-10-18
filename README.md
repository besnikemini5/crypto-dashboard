# Crypto Dashboard

A Flask web app for exploring cryptocurrency prices. It has a summary dashboard, live prices from the CoinGecko API, a candlestick chart, and the latest crypto news, all behind a simple menu page with a light/dark theme toggle.

Supported coins: Bitcoin (BTC), Ethereum (ETH), Solana (SOL) and XRP.

<!-- Add a screenshot here: ![Dashboard screenshot](docs/screenshot.png) -->

## Features

- **Dashboard:** number of coins tracked, latest data timestamp, and the top gainer and loser over the last 30 data points
- **Live prices:** current USD prices from the CoinGecko API
- **Candlestick chart:** weekly OHLC candles for Ethereum, built from the daily price history
- **News:** latest crypto business headlines from the newsdata.io API

## Tech Stack

- Python, Flask
- pandas for data cleaning and analysis
- Plotly for charts
- Requests for external API calls
- HTML / CSS / Bootstrap (Jinja2 templates)

## Getting Started

### Prerequisites

- Python 3.10 or newer

### Setup

```powershell
git clone https://github.com/besnikemini5/crypto-dashboard.git
cd crypto-dashboard

python -m venv venv
venv\Scripts\activate

pip install -r requirements.txt
```

### Optional: enable the news page

The news page needs a free API key from [newsdata.io](https://newsdata.io). Set it as an environment variable before starting the app:

```powershell
$env:NEWSDATA_API_KEY="your_key_here"
```

Without a key, the news page simply shows no articles and everything else still works.

### Run

```powershell
python app.py
```

Then open <http://127.0.0.1:5000> in your browser.

## Project Structure

```
app.py              # Flask app and routes
templates/          # HTML templates
static/             # CSS
*_data.csv          # Historical daily price data per coin
```

## Notes

- Historical prices come from static CSV files, so they are a snapshot and not updated automatically. Only the Live Prices page uses real-time data.
- Candlestick candles are aggregated from daily closing prices, not from exchange tick data.
