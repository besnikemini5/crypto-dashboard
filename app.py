from flask import Flask, render_template
import pandas as pd
import os
import requests
import plotly.graph_objects as go

app = Flask(__name__)

# === File mappings ===
COIN_FILES = {
    'ETH': 'eth_data.csv',
    'BTC': 'btc_data.csv',
    'SOL': 'sol_data.csv',
    'XRP': 'xrp_data.csv'
}


def load_coin(coin):
    """Load and clean the price history for one coin."""
    df = pd.read_csv(COIN_FILES[coin])
    df.rename(columns={'snapped_at': 'Date', 'price': 'Close'}, inplace=True)
    df['Date'] = pd.to_datetime(df['Date']).dt.tz_localize(None)
    df['Close'] = pd.to_numeric(df['Close'], errors='coerce')
    return df.dropna(subset=['Close']).sort_values('Date')


# === Home Page (menu) ===
@app.route("/")
def index():
    return render_template("index.html")


# === Dashboard Page ===
@app.route("/dashboard")
def dashboard():
    changes = {}
    latest = None
    for coin in COIN_FILES:
        df = load_coin(coin)
        last30 = df.tail(30)
        changes[coin] = (last30['Close'].iloc[-1] / last30['Close'].iloc[0] - 1) * 100
        newest = df['Date'].max()
        latest = newest if latest is None else max(latest, newest)

    stats = {
        "total_coins": len(COIN_FILES),
        "latest_price_update": latest.strftime("%Y-%m-%d %H:%M"),
        "top_gainer": max(changes, key=changes.get),
        "top_loser": min(changes, key=changes.get),
    }
    return render_template("dashboard.html", stats=stats)


# === Live Prices Page ===
@app.route('/live')
def live_prices():
    coins = ['bitcoin', 'ethereum', 'solana', 'ripple']
    url = "https://api.coingecko.com/api/v3/simple/price"
    try:
        response = requests.get(url, params={
            'ids': ','.join(coins),
            'vs_currencies': 'usd'
        }, timeout=10)
        response.raise_for_status()
        data = response.json()
        prices = [
            {'name': 'Bitcoin', 'price': data['bitcoin']['usd']},
            {'name': 'Ethereum', 'price': data['ethereum']['usd']},
            {'name': 'Solana', 'price': data['solana']['usd']},
            {'name': 'XRP', 'price': data['ripple']['usd']}
        ]
    except (requests.RequestException, KeyError, ValueError) as e:
        print("Live price error:", e)
        prices = []
    return render_template('live.html', prices=prices)


# === Candlestick Chart Page ===
@app.route('/candles')
def candles():
    df = load_coin('ETH')

    # Real weekly OHLC built from the daily prices
    ohlc = df.set_index('Date')['Close'].resample('W').ohlc().dropna().tail(52)

    fig = go.Figure(data=[go.Candlestick(
        x=ohlc.index,
        open=ohlc['open'],
        high=ohlc['high'],
        low=ohlc['low'],
        close=ohlc['close'],
        increasing_line_color='lime',
        decreasing_line_color='red'
    )])

    fig.update_layout(
        title='Ethereum Weekly Candlestick Chart (last 52 weeks, built from daily prices)',
        xaxis_title='Date',
        yaxis_title='Price (USD)',
        template='plotly_dark'
    )

    chart_html = fig.to_html(full_html=False)
    return render_template("candles.html", chart_html=chart_html)


# === News Page ===
@app.route('/news')
def news():
    api_key = os.environ.get("NEWSDATA_API_KEY")
    if not api_key:
        return render_template("news.html", articles=[])

    try:
        response = requests.get(
            "https://newsdata.io/api/1/news",
            params={"apikey": api_key, "q": "crypto", "language": "en", "category": "business"},
            timeout=10,
        )
        response.raise_for_status()
        data = response.json()

        articles = [
            {
                'title': article['title'],
                'url': article['link'],
                'pubDate': article['pubDate'],
                'source': article.get('source_id', 'Unknown')
            }
            for article in data.get('results', [])
        ]
    except (requests.RequestException, KeyError, ValueError) as e:
        print("News Fetch Error:", e)
        articles = []

    return render_template("news.html", articles=articles)


# === Run App ===
if __name__ == "__main__":
    app.run(debug=os.environ.get("FLASK_DEBUG") == "1")
