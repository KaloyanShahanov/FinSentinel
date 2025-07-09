import threading
import time
import requests

from app.shared_queue import price_diff_queue
from app.logger import logger
from app.alerts import send_slack_alert, send_exchange_rate_alert

running = False
exchange_rate_alert_sent = False

# fetch usd to eur exchange rate
def fetch_usd_to_eur_rate():
    #url = "https://api.exchangerate.host/latest?base=USD&symbols=EUR" - requires API key
    url = "https://api.fxratesapi.com/latest?base=USD&currencies=EUR&resolution=1m&amount=1&places=6&format=json" # Free for now
    try:
        response = requests.get(url, timeout=5)
        data = response.json()
        rate = data["rates"]["EUR"]
        return float(rate)
    except Exception:
        logger.exception("Failed to fetch USD to EUR exchange rate")
        return None

# fetch Bitcoin price from Binance
def fetch_price_binance_bitcoin():
    url = "https://api.binance.com/api/v3/ticker/price?symbol=BTCEUR"
    data = requests.get(url).json()
    return float(data["price"])

# fetch Bitcoin price from Bitfinex
def fetch_price_bitfinex_bitcoin():
    url = "https://api-pub.bitfinex.com/v2/ticker/tBTCEUR"
    data = requests.get(url).json()
    return float(data[6])  # Last price

# fetch Bitcoin price from Kraken
def fetch_price_kraken_bitcoin():
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
        logger.exception("Error fetching Bitcoin Kraken price")
        return None

# fetch Bitcoin price from Crypto.com
def fetch_price_crypto_exchange_bitcoin():
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
        logger.exception("Error fetching Bitcoin Crypto.com price")
        return None

# fetch Bitcoin price from Bitget
def fetch_price_bitget_bitcoin():
    url = "https://api.bitget.com/api/v2/mix/market/tickers?productType=COIN-FUTURES"
    try:
        response = requests.get(url, timeout=5)
        data = response.json()

        logger.info("Bitget API response: %s", data)

        if data.get("code") != "00000":
            raise ValueError(f"Bitget API returned error code: {data.get('code')}")

        tickers = data.get("data", [])
        if not tickers:
            raise KeyError("'data' key missing or empty in Bitget response")

        btc_ticker = next((item for item in tickers if "btc" in item.get("symbol", "").lower()), None)
        if btc_ticker is None:
            raise KeyError("BTC ticker not found in Bitget response")

        last_price_str = btc_ticker.get("lastPr")
        if last_price_str is None:
            raise KeyError("'lastPr' price missing for BTC ticker in Bitget response")

        last_price_usd = float(last_price_str)

        usd_to_eur = fetch_usd_to_eur_rate()
        if usd_to_eur is None:
            # Return None to indicate failure — no price to compare
            return None

        last_price_eur = last_price_usd * usd_to_eur
        return last_price_eur

    except Exception:
        logger.exception("Error fetching Bitcoin Bitget price")
        return None

def monitor_loop():
    global running, exchange_rate_alert_sent
    while running:
        # Bitcoin,Binance vs bitfinex
        try:
            price_binance = fetch_price_binance_bitcoin()
            price_bitfinex = fetch_price_bitfinex_bitcoin()

            avg = (price_binance + price_bitfinex) / 2
            diff = abs(price_binance - price_bitfinex)
            percent_diff = (diff / avg) * 100

            logger.info(f"Binance: {price_binance:.6f}, Bitfinex: {price_bitfinex:.6f}, Diff: {percent_diff:.8f}%")
            price_diff_queue.put(("Binance vs Bitfinex", percent_diff, 0))

            if percent_diff >= 0.00002:
                send_slack_alert("Bitcoin", "Binance vs Bitfinex", price_binance, price_bitfinex, percent_diff)

        except Exception:
            logger.exception("Error comparing Bitcoin,Binance vs Bitfinex")
            if not running:
                break
            time.sleep(5)

        # Bitcoin,Binance vs Kraken
        try:
            price_binance = fetch_price_binance_bitcoin()
            price_kraken = fetch_price_kraken_bitcoin()

            if price_binance is None or price_kraken is None:
                logger.info("Skipping Bitcoin, Binance/Kraken comparison due to failed price fetch.")
                continue

            avg = (price_binance + price_kraken) / 2
            diff = abs(price_binance - price_kraken)
            percent_diff = (diff / avg) * 100

            logger.info(f"Binance: {price_binance:.6f}, Kraken: {price_kraken:.6f}, Diff: {percent_diff:.8f}%")
            price_diff_queue.put(("Binance vs Kraken", percent_diff, 0))

            if percent_diff >= 0.00002:
                send_slack_alert("Bitcoin", "Binance vs Kraken", price_binance, price_kraken, percent_diff)

        except Exception:
            logger.exception("Error comparing Bitcoin,Binance vs Kraken")
            if not running:
                break
            time.sleep(5)

        # Bitcoin,Binance vs crypto.com
        try:
            price_binance = fetch_price_binance_bitcoin()
            price_crypto_exchange = fetch_price_crypto_exchange_bitcoin()

            if price_crypto_exchange is None:
                logger.info("Skipping Bitcoin, Binance/Crypto.com comparison due to failed price fetch.")
                continue

            avg = (price_binance + price_crypto_exchange) / 2
            diff = abs(price_binance - price_crypto_exchange)
            percent_diff = (diff / avg) * 100

            logger.info(f"Binance: {price_binance:.6f}, Crypto Exchange: {price_crypto_exchange:.6f}, Diff: {percent_diff:.8f}%")
            price_diff_queue.put(("Binance vs Crypto", percent_diff, 0))

            if percent_diff >= 0.00002:
                send_slack_alert("Bitcoin", "Binance vs Crypto", price_binance, price_crypto_exchange, percent_diff)

        except Exception:
            logger.exception("Error comparing Bitcoin, Binance vs Crypto.com")
            if not running:
                break
            time.sleep(5)

        # Bitcoin,Binance vs Bitget
        try:
            price_binance = fetch_price_binance_bitcoin()
            price_bitget = fetch_price_bitget_bitcoin()

            if price_bitget is None:
                if not exchange_rate_alert_sent:
                    send_exchange_rate_alert()
                    exchange_rate_alert_sent = True
                logger.info("Skipping Bitcoin, Binance/Bitget comparison due to failed price or exchange rate fetch.")
                continue

            exchange_rate_alert_sent = False

            avg = (price_binance + price_bitget) / 2
            diff = abs(price_binance - price_bitget)
            percent_diff = (diff / avg) * 100

            logger.info(f"Binance: {price_binance:.6f}, Bitget: {price_bitget:.6f}, Diff: {percent_diff:.8f}%")
            price_diff_queue.put(("Binance vs Bitget", percent_diff, 0))

            if percent_diff >= 0.00002:
                send_slack_alert("Bitcoin", "Binance vs Bitget", price_binance, price_bitget, percent_diff)
        except Exception:
            logger.exception("Error comparing Bitcoin, Binance vs Bitget")
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
