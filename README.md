# Quantitative Momentum Strategy (Polynomial Regression)

## 📌 Project Overview
This project implements a **Polynomial Regression** algorithm to detect trend reversals in volatile stocks (TSLA, NVDA). Unlike simple Moving Averages, this model fits a non-linear curve to price data to predict momentum shifts, aiming to enter rallies early and exit before crashes.

## 🛠️ Tech Stack
* **Python 3.12** (via Anaconda)
* **Pandas & NumPy:** Vectorized data manipulation.
* **Scikit-Learn:** Polynomial feature transformation and Linear Regression fitting.
* **Matplotlib:** Financial visualization and signal plotting.
* **YFinance:** Real-time market data ingestion.

## 📊 Performance (Backtest)
* **Asset:** NVDA (1 Year)
* **Strategy Return:** +50.47% 🚀
* **Benchmark (Buy & Hold):** +35.27%
* **Alpha Generated:** +15.2%
* *Note: Backtest includes realistic transaction costs (0.1% per trade) to prevent overfitting.*

## 🧠 Key Logic
The model avoids "look-ahead bias" by shifting signals forward one day. It solves the "Mean Reversion" problem by penalizing trades during non-trending choppy markets.

## 🚀 How to Run
1.  Clone the repo.
2.  Install dependencies: `pip install -r requirements.txt`
3.  Run the backtester: `python src/backtest.py`