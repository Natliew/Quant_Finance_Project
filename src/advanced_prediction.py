import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
import datetime as dt

print("Fetching data .... 🚀")
tesla = yf.download("TSLA", period="6mo", progress=False)

if isinstance(tesla.columns, pd.MultiIndex):
    print(tesla)
    tesla = tesla.xs('Close', level=0, axis=1)

if 'Close' in tesla.columns:
    y = tesla['Close']
else:
    y = tesla.iloc[:,0]

tesla = tesla.copy()
tesla["Day_Num"] = np.arange(len(tesla))
X = tesla[["Day_Num"]]

poly = PolynomialFeatures(degree=2)
X_poly = poly.fit_transform(X)

model = LinearRegression()
model.fit(X_poly, y)

tesla['Poly_Trend'] = model.predict(X_poly)

plt.figure(figsize=(12,6))
plt.scatter(tesla.index, y, color='blue', s=5, label='Actual Price')
plt.plot(tesla.index, tesla['Poly_Trend'], color='green', linewidth=2, label='Polynomial Trend (Curve)')

plt.title("Tesla (TSLA): Polynomial Regression")
plt.xlabel('Date')
plt.ylabel('Price (USD)')
plt.legend()
plt.grid(True)
plt.show()

print("\n--- 🔮 FORECAST ---")
last_day = tesla['Day_Num'].iloc[-1]
next_day_num = np.array([[last_day + 1]])

next_day_poly = poly.transform(next_day_num)
next_price = model.predict(next_day_poly)[0]

print(f"Predicted Price for Next Trading Day: ${next_price:.2f}")

# Check Acceleration (The x^2 coefficient)
acceleration = model.coef_[2] 
print(f"Acceleration Factor: {acceleration:.5f}")

if acceleration > 0:
    print("Market Momentum: Accelerating UP 🚀")
else:
    print("Market Momentum: Decelerating (Slowing Down) 🐢")