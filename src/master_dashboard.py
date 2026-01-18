import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
import yfinance as yf
import datetime as dt

print("--- STARTING QUANT ANALYSIS ENGINE ---")
print("Fetching TSLA data... 🚀")
tesla = yf.download("TSLA", period="6mo", progress=False)

if isinstance(tesla.columns, pd.MultiIndex):
    tesla = tesla.xs('Close', level=0, axis=1)
 
if 'Close' in tesla.columns:
    y = tesla['Close']
else:
    y = tesla.iloc[:, 0]

tesla = tesla.copy()
tesla["Day_Num"] = np.arange(len(tesla))
X = tesla[["Day_Num"]]

linear_model = LinearRegression()
linear_model.fit(X, y)
tesla["Linear_Trend"] = linear_model.predict(X)

poly = PolynomialFeatures(degree=2)
X_poly = poly.fit_transform(X)

poly_model = LinearRegression()
poly_model.fit(X_poly, y)
tesla["Poly_Trend"] = poly_model.predict(X_poly)

last_day_num = tesla["Day_Num"].iloc[-1]
next_day_num = pd.DataFrame([[last_day_num + 1]], columns=["Day_Num"])
next_day_poly = poly.transform(next_day_num)

pred_linear = linear_model.predict(next_day_num)[0]
pred_poly = poly_model.predict(next_day_poly)[0]

plt.figure(figsize=(14,7))
plt.scatter(tesla.index, y, color='blue', alpha=0.5, s=10, label='Actual Market Price')

# Linear
plt.plot(tesla.index, tesla['Linear_Trend'], color="red", linestyle='--', linewidth=2, label=f"Linear Trend (Target: ${pred_linear:.2f})")

# Polynomial Trend (Green Curve)
plt.plot(tesla.index, tesla['Poly_Trend'], color="green", linewidth=3, label=f"Poly Curve (Target: ${pred_poly:.2f})")

plt.title(f'Tesla (TSLA): Linear vs. Polynomial Models', fontsize=16)
plt.xlabel('Date')
plt.ylabel('Price (USD)')
plt.legend(loc = 'upper left')
plt.grid(True, alpha=0.3)
plt.show()

# --- 6. ANALYST REPORT ---
print("\n" + "="*40)
print("     📢 FINAL ANALYST REPORT")
print("="*40)
print(f"Current Price:     ${y.iloc[-1]:.2f}")
print("-" * 40)
print(f"Model A (Linear):  ${pred_linear:.2f} (Straight Trend)")
print(f"Model B (Poly):    ${pred_poly:.2f} (Curved Fit)")
print("-" * 40)

# Decision Logic
diff = pred_linear - pred_poly
print(f"Divergence:        ${diff:.2f}")
if pred_poly < pred_linear:
    print("WARNING: Polynomial model detects momentum slowing down.")
    print("RECOMMENDATION: Use Caution. The curve is lower than the straight line.")
else:
    print("SIGNAL: Both models agree on strong upside.")
print("="*40)