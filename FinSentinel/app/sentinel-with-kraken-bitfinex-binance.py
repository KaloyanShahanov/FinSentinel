import threading
import time
import requests
from app.alerts import send_slack_alert

running = False
monitor_thread = None

def fetch_price_binance():
    url = "https://api.binance.com/api/v3/ticker/price?symbol=BTCEUR"
    data = requests.get(url).json()
    return float(data["price"])

def fetch_price_bitfinex():
    url = "https://api-pub.bitfinex.com/v2/ticker/tBTCEUR"
    data = requests.get(url).json()
    return float(data[6])  # Last price

def fetch_price_kraken():
    url = "https://api.kraken.com/0/public/Ticker"
    params = {"pair": "XBTEUR"}
    response = requests.get(url, params=params)
    data = response.json()
    
    result = data["result"]
    key = list(result.keys())[0]  # e.g., "XXBTZEUR"
    last_price = result[key]["c"][0]  # "c" is the "last trade closed" array
    return float(last_price)

    
def monitor_loop():
    global running
    while running:
        try:
           price_binance = fetch_price_binance()
           price_bitfinex = fetch_price_bitfinex()

           avg = (price_binance + price_bitfinex) / 2
           diff = abs(price_binance - price_bitfinex)
           percent_diff = (diff / avg) * 100

           print(f"Binance: {price_binance:.6f}, Bitfinex: {price_bitfinex:.6f}, Diff: {percent_diff:.8f}%")

           if percent_diff >= 0.00002:
               send_slack_alert("Bitcoin","Binance vs Bitfinex", price_binance, price_bitfinex, percent_diff)
             
        except Exception as e:
            print("Error in monitor loop:", e)
            if not running:
                break
            time.sleep(5)

        try:
            price_binance = fetch_price_binance()
            price_kraken = fetch_price_kraken()

            avg = (price_binance + price_kraken) / 2
            diff = abs(price_binance - price_kraken)
            percent_diff = (diff / avg) * 100

            print(f"Binance: {price_binance:.6f}, Kraken: {price_kraken:.6f}, Diff: {percent_diff:.8f}%")

            if percent_diff >= 0.00002:
                send_slack_alert("Bitcoin","Binance vs Kraken", price_binance, price_kraken, percent_diff)
             
        except Exception as e:
            print("Error in monitor loop:", e)
            if not running:
                break
            time.sleep(5)

def start_crypto_monitor():
    global running, monitor_thread
    if not running:
        running = True
        monitor_thread = threading.Thread(target=monitor_loop, daemon=True)
        monitor_thread.start()

def stop_crypto_monitor():
    global running
    running = False
