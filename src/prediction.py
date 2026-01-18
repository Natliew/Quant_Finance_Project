import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import datetime as dt


# 1. Fetch Data
print("Fetching TSLA data... 🚀")
tesla = yf.Ticker("TSLA")
data = tesla.history(period="6mo")

# 2. Prepare Data for AI
# Fixed the typo: it is 'arange' (one r), not 'arrange'
data["Day_Num"] = np.arange(len(data))

# Reshape for Sklearn
X = data[['Day_Num']]
y = data['Close']

# 3. Train the Model
model = LinearRegression()
model.fit(X, y)

# 4. Predict
data["Trend_Line"] = model.predict(X)
print("Plotting ......")
# 5. Visualize
plt.figure(figsize=(10, 6))
plt.scatter(data.index, data["Close"], color="blue", s=5, label="Actual Price")
plt.plot(data.index, data["Trend_Line"], color="red", linewidth=2, label="AI Trend Line")

plt.title('Tesla (TSLA) Trend Prediction')
plt.xlabel("Date")
plt.ylabel("Price (USD)")
plt.legend()
plt.grid(True)
plt.show()


# 6. Conclusion
slope = model.coef_[0]
print(f"Model Slope: {slope:.4f}")
if slope > 0:
    print("Conclusion: The general trend is UP 📈")
else:
    print("Conclusion: The general trend is DOWN 📉")

# === NEW: PREDICT THE FUTURE ===
print("\n--- 🔮 FORECAST ---")

last_day_num = data["Day_Num"].iloc[-1]
next_day_num = np.array([[last_day_num + 1]])

next_price = model.predict(next_day_num)[0]

last_date = data.index[-1]
next_date = last_date + dt.timedelta(days=1)

print(f"Last Closing Price: ${data['Close'].iloc[-1]:.2f}")
print(f"Predicted Price for Next Trading Day ({next_date.date()}): ${next_price:.2f}")

# 4. The Advice
if next_price > data['Close'].iloc[-1]:
    diff = next_price - data['Close'].iloc[-1]
    print(f"Model suggests: BUY (Expected increase of ${diff:.2f})")
else:
    diff = data['Close'].iloc[-1] - next_price
    print(f"Model suggests: SELL (Expected drop of ${diff:.2f})")



