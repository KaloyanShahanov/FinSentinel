import requests
import time
import threading
from app.alerts import send_email_alert, send_slack_alert

last_prices = {}

# API functions for multi-coin 

def fetch_price_coingecko(coin_id):
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies=usd"
    data = requests.get(url).json()
    return data[coin_id]["usd"]

def fetch_price_coincap(symbol):
    url = f"https://api.coincap.io/v2/assets/{symbol.lower()}"
    data = requests.get(url).json()
    return float(data["data"]["priceUsd"])

def fetch_price_binance(symbol):
    url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}USDT"
    data = requests.get(url).json()
    return float(data["price"])

# multi-API for a single coin

def average_price(coin):
    prices = []
    try: prices.append(fetch_price_coingecko(coin["coingecko_id"]))
    except: print(f"Error: CoinGecko for {coin['name']}")
    try: prices.append(fetch_price_coincap(coin["coincap_id"]))
    except: print(f"Error: CoinCap for {coin['name']}")
    try: prices.append(fetch_price_binance(coin["binance_symbol"]))
    except: print(f"Error: Binance for {coin['name']}")

    if prices:
        return sum(prices) / len(prices)
    else:
        raise Exception(f"No prices fetched for {coin['name']}")

# def send_test_email():
#    test_name = "TestCoin"
#    test_price = 1234.56
#    print("Sending test email alert...")
#    send_email_alert(test_name, test_price)
#    send_slack_alert(test_name, test_price)
#    print("Test alerts sent.")

# main monitor loop

coins = [
    {"name": "Bitcoin", "coingecko_id": "bitcoin", "coincap_id": "bitcoin", "binance_symbol": "BTC"},
    {"name": "Ethereum", "coingecko_id": "ethereum", "coincap_id": "ethereum", "binance_symbol": "ETH"},
    {"name": "Dogecoin", "coingecko_id": "dogecoin", "coincap_id": "dogecoin", "binance_symbol": "DOGE"},
]

def monitor_crypto():
    global last_prices
    while True:
        try:
            for coin in coins:
                price = average_price(coin)
                name = coin["name"]
                print(f"{name} Price: ${round(price, 4)}")

                if name in last_prices:
                    last_price = last_prices[name]
                    drop_percent = (last_price - price) / last_price
                    rise_percent = (price - last_price) / last_price

                    if drop_percent >= 0.05:
                        alert_message = f"{name} price dropped by {drop_percent*100:.2f}%! Now: ${round(price, 4)}"
                        send_email_alert(name, round(price, 4))
                        send_slack_alert(name, round(price, 4))

                    elif rise_percent >= 0.05:
                        alert_message = f"{name} price rose by {rise_percent*100:.2f}%! Now: ${round(price, 4)}"
                        send_email_alert(name, round(price, 4))
                        send_slack_alert(name, round(price, 4))

                last_prices[name] = price

        except Exception as e:
            print("Error in crypto monitor:", e)

        time.sleep(60)

def start_crypto_monitor():
    thread = threading.Thread(target=monitor_crypto, daemon=True)
    thread.start()
