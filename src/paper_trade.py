from alpaca_trade_api.rest import REST
import time

# --- CONFIGURATION ---
API_KEY = "PKQYLGCLIS6T4ZXMFGGS5D3MWZ"       # <--- PASTE YOUR KEY
SECRET_KEY = "AbpzB1hECKRQgMy6EoJz315fvnU4E1Nrir3zPKV2Vbw3" # <--- PASTE YOUR SECRET
BASE_URL = "https://paper-api.alpaca.markets"

# --- CONNECT ---
print("Connecting to Alpaca Paper Trading...")
api = REST(API_KEY, SECRET_KEY, BASE_URL)

# 1. Check Bank Account
account = api.get_account()
print(f"💰 Cash Available: ${account.cash}")

# 2. FORCE THE TRADE (Ignore Market Hours)
print("\n🚀 Attempting to buy BTC (Crypto trades 24/7)...")

try:
    # Submit Order for Bitcoin
    order = api.submit_order(
        symbol='BTC/USD', 
        qty=0.01,          
        side='buy',
        type='market',
        time_in_force='gtc'
    )
    print("✅ ORDER SENT SUCCESS!")
    print(f"Order ID: {order.id}")
    print("Go check your Alpaca Dashboard -> Positions tab!")
    
except Exception as e:
    print(f"❌ Order Failed: {e}")