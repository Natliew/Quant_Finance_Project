import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# 1. Define the Ticker and Fetch Data
# We are asking for Tesla (TSLA) data for the last 3 months
print("Fetching market data... 🚀")
ticker = "TSLA"
tesla = yf.Ticker(ticker)

# Get historical data
data = tesla.history(period = "1y")

data["Daily Return"] = data["Close"].pct_change()
data["SMA_20"] = data["Close"].rolling(window=20).mean()
data["SMA_50"] = data["Close"].rolling(window=50).mean()
# fig is the canvas, (ax1, ax2) are the two charts

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)

if data.empty:
    print(f"❌ Error: No data found for {ticker}. Check your internet or the ticker spelling.")
else:
    print("\n--- Raw Data Preview ---")
    print(data.head())

    # We plot the 'Close' column to see the final price of each trading day
    ax1.plot(data.index, data['Close'], label = f"Price", color = "red")
    ax1.plot(data.index, data['SMA_20'], label='20-Day SMA', color='cyan', linewidth=2)
    ax1.plot(data.index, data['SMA_50'], label='50-Day SMA', color='orange')

    #chart1
    ax1.set_title(f"{ticker} Stock Price - Last 3 months")
    ax1.grid(True)
    ax1.set_xlabel("Date")
    ax1.set_ylabel("Price (USD)")

    #chart2
    ax2.plot(data.index, data["Daily Return"], label="Daily Return", color="red", linestyle = '--')
    ax2.set_title("Daily Volatile (The Heartbeat)")
    ax2.set_ylabel('% Change')
    ax2.grid(True)

    # Add a horizontal line at 0 (to show positive vs negative days)
    ax2.axhline(0, color='black', linewidth=1)

    plt.tight_layout() # Prevents labels from overlapping
    plt.show()
  