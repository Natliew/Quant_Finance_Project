import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures

# --- CHECKPOINT 1 ---
print("1. Fetching data from Yahoo... ⏳")
data = yf.download("NVDA", period="1y", progress=False)

# Clean Data
if isinstance(data.columns, pd.MultiIndex):
    data = data.xs('Close', level=0, axis=1)

if 'Close' in data.columns:
    y = data['Close']
else:
    y = data.iloc[:,0]

# --- CHECKPOINT 2 ---
print("2. Training AI Models... 🧠")
data = data.copy()
data["Day_Num"] = np.arange(len(data))
X = data[["Day_Num"]]

# Train Linear
linear_model = LinearRegression()
linear_model.fit(X, y)

# Train Polynomial
poly = PolynomialFeatures(degree=2)
X_poly = poly.fit_transform(X)
poly_model = LinearRegression()
poly_model.fit(X_poly, y)
data["Poly_Trend"] = poly_model.predict(X_poly)

# --- CHECKPOINT 3 ---
print("3. Simulating Trades... 💸")

# Generate Signal
data["signal"] = np.where(data['Poly_Trend'] > y, 1, 0)

# FIX: Define the cost!
transaction_cost = 0.001  # 0.1% fee

# Calculate Trades (0 or 1)
data["Trades"] = data['signal'].diff().abs()

# Calculate Returns
data["Market_Return"] = y.pct_change()
data["Strategy_Return"] = data['signal'].shift(1) * data["Market_Return"]

# FIX: Multiply Trades by the cost (1 * 0.001), NOT just (1)
data['Strategy_Return_Net'] = data['Strategy_Return'] - (data["Trades"] * transaction_cost)

# Cumulative Math
data["Market_Cumulative"] = (1 + data["Market_Return"]).cumprod()
data["Strategy_Cumulative"] = (1 + data["Strategy_Return"]).cumprod()
data['Strategy_Cumulative_Net'] = (1 + data['Strategy_Return_Net']).cumprod()


# --- CHECKPOINT 4: THE UNIFIED DASHBOARD ---
print("4. Plotting Dashboard... 📊")

# Create 2 plots stacked on top of each other
# sharex=True means if you zoom in on one, the other zooms too!
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10), sharex=True)

# === TOP CHART: Price & Signals ===
# 1. Plot Price
ax1.plot(data.index, y, label="NVDA Price", color="black", alpha=0.3)
ax1.plot(data.index, data['Poly_Trend'], label="AI Trend", color="blue", linestyle="--", alpha=0.5)

# 2. Add Buy/Sell Markers
buy_signals = data[data['signal'].diff() == 1].index
sell_signals = data[data['signal'].diff() == -1].index

ax1.scatter(buy_signals, y.loc[buy_signals], marker='^', color='green', s=150, label='Buy', zorder=5)
ax1.scatter(sell_signals, y.loc[sell_signals], marker='v', color='red', s=150, label='Sell', zorder=5)

ax1.set_title("AI Decision Making (Price vs Trend)")
ax1.legend()
ax1.grid(True, alpha=0.3)

# === BOTTOM CHART: The Bank Account ===
# 3. Plot Cumulative Returns
ax2.plot(data.index, data['Market_Cumulative'], label="Buy & Hold (Market)", color="grey", alpha=0.6)
ax2.plot(data.index, data['Strategy_Cumulative_Net'], label="AI Strategy (Net)", color="green", linewidth=2)

# 4. Fill the area under the curve to make it look "Pro"
ax2.fill_between(data.index, data['Strategy_Cumulative_Net'], 1, color='green', alpha=0.1)

ax2.set_title("Portfolio Growth ($1 Investment)")
ax2.legend()
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

# --- SCOREBOARD ---
print("\n" + "="*30)
print("      🏆 FINAL RESULTS")
print("="*30)
# ... (Keep your existing print logic below this) ...
if not data.empty:
    market_return = data['Market_Cumulative'].iloc[-1] - 1
    strategy_return = data['Strategy_Cumulative_Net'].iloc[-1] - 1
    
    print(f"Market Return:    {market_return*100:.2f}%")
    print(f"AI Model Return:  {strategy_return*100:.2f}%")
    print("-" * 30)
    if strategy_return > market_return:
        print("✅ SUCCESS: The AI beat the market!")
    else:
        print("❌ FAILURE: The AI lost to simple holding.")
else:
    print("❌ Error: No data to analyze.")
print("="*30)