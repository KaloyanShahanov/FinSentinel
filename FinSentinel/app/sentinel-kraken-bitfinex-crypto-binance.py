import threading
import time
import requests

from app.logger import logger
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
    try:
        response = requests.get(url, params=params, timeout=5)
        data = response.json()

        logger.info("Kraken API response: %s", data)

        if "error" in data and data["error"]:
            raise ValueError(f"Kraken API returned error: {data['error']}")

        if "result" not in data:
            raise KeyError("'result' key missing in Kraken response")

        result = data["result"]
        key = next(iter(result))
        last_price = result[key]["c"][0]
        return float(last_price)

    except Exception:
        logger.exception("Error fetching Kraken price")
        return None

def fetch_price_crypto_exchange():
    url = "https://api.crypto.com/v2/public/get-ticker"
    params = {"instrument_name": "BTC_EUR"}
    try:
        response = requests.get(url, params=params, timeout=5)
        data = response.json()

        logger.info(f"Crypto.com API response: {data}")

        tickers = data.get("result", {}).get("data", [])
        if not tickers:
            raise KeyError("No ticker data in Crypto.com response")

        btc_data = tickers[0]  # First item in the list for BTC_EUR

        bid = float(btc_data["b"])  # Best bid
        ask = float(btc_data["k"])  # Best ask

        # Average price
        last_price = (bid + ask) / 2
        return last_price

    except Exception as e:
        logger.exception("Error fetching Crypto.com price")
        return None


def monitor_loop():
    global running
    while running:
        try:
            price_binance = fetch_price_binance()
            price_bitfinex = fetch_price_bitfinex()

            avg = (price_binance + price_bitfinex) / 2
            diff = abs(price_binance - price_bitfinex)
            percent_diff = (diff / avg) * 100

            logger.info(f"Binance: {price_binance:.6f}, Bitfinex: {price_bitfinex:.6f}, Diff: {percent_diff:.8f}%")

            if percent_diff >= 0.00002:
                send_slack_alert("Bitcoin", "Binance vs Bitfinex", price_binance, price_bitfinex, percent_diff)

        except Exception:
            logger.exception("Error comparing Binance vs Bitfinex")
            if not running:
                break
            time.sleep(5)

        try:
            price_binance = fetch_price_binance()
            price_kraken = fetch_price_kraken()

            if price_binance is None or price_kraken is None:
                logger.info("Skipping Kraken comparison due to failed price fetch.")
                continue

            avg = (price_binance + price_kraken) / 2
            diff = abs(price_binance - price_kraken)
            percent_diff = (diff / avg) * 100

            logger.info(f"Binance: {price_binance:.6f}, Kraken: {price_kraken:.6f}, Diff: {percent_diff:.8f}%")

            if percent_diff >= 0.00002:
                send_slack_alert("Bitcoin", "Binance vs Kraken", price_binance, price_kraken, percent_diff)

        except Exception:
            logger.exception("Error comparing Binance vs Kraken")
            if not running:
                break
            time.sleep(5)

        try:
            price_binance = fetch_price_binance()
            price_crypto_exchange = fetch_price_crypto_exchange()

            if price_crypto_exchange is None:
                logger.info("Skipping Crypto.com comparison due to failed price fetch.")
                continue

            avg = (price_binance + price_crypto_exchange) / 2
            diff = abs(price_binance - price_crypto_exchange)
            percent_diff = (diff / avg) * 100

            logger.info(f"Binance: {price_binance:.6f}, Crypto Exchange: {price_crypto_exchange:.6f}, Diff: {percent_diff:.8f}%")

            if percent_diff >= 0.00002:
                send_slack_alert("Bitcoin", "Binance vs Crypto", price_binance, price_crypto_exchange, percent_diff)

        except Exception:
            logger.exception("Error comparing Binance vs Crypto.com")
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
