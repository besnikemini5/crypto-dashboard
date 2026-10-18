import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set(style="darkgrid")

# Load the data
df = pd.read_csv("eth_data.csv")

# Rename columns for clarity (optional but cleaner)
df.rename(columns={
    'snapped_at': 'Date',
    'price': 'Close'
}, inplace=True)

# Convert to datetime and sort
df['Date'] = pd.to_datetime(df['Date'])
df = df.sort_values('Date')

# Drop missing values in Close
df.dropna(subset=['Close'], inplace=True)

# Add moving averages
df['MA7'] = df['Close'].rolling(window=7).mean()     # 7-day moving average
df['MA30'] = df['Close'].rolling(window=30).mean()   # 30-day moving average

plt.figure(figsize=(12, 6))
plt.plot(df['Date'], df['Close'], label='ETH Close Price', color='purple')
plt.plot(df['Date'], df['MA7'], label='7-Day MA', color='orange')
plt.plot(df['Date'], df['MA30'], label='30-Day MA', color='green')
plt.title("Ethereum Price Trend with Moving Averages")
plt.xlabel("Date")
plt.ylabel("Price (USD)")
plt.legend()
plt.tight_layout()
plt.show()

