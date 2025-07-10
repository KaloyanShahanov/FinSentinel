#This file contains the API fetchers for the FinSentinel application.

import requests
import logging
from app.logger import get_logger
logger = get_logger("API fetchers")

# ================ Fetch Bitcoin from Binance, Bitfinex, Coinbase, Kraken and Crypto.com APIs ================

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
    try:
       url = "https://api.binance.com/api/v3/ticker/price?symbol=BTCEUR"
       data = requests.get(url).json()
       logger.info("Bitcoin Binance API response: %s", data)
       return float(data["price"])
    except Exception:
        logger.exception("Error fetching Bitcoin Bitfinex price")
        return None

# fetch Bitcoin price from Bitfinex
def fetch_price_bitfinex_bitcoin():
    try:
       url = "https://api-pub.bitfinex.com/v2/ticker/tBTCEUR"
       data = requests.get(url).json()
       logger.info("Bitcoin Bitfinex API response: %s", data)
       return float(data[6])  # Last price
    except Exception:
        logger.exception("Error fetching Ethereum Bitfinex price")
        return None

# fetch Bitcoin price from Coinbase Exchange
def fetch_price_coinbase_bitcoin():
    try:
       url = "https://api.exchange.coinbase.com/products/BTC-EUR/ticker"
       data = requests.get(url).json()
       logger.info("Bitcoin Coinbase API response: %s", data)
       return float(data["price"])
    except Exception:
        logger.exception("Error fetching Ethereum Bitfinex price")
        return None

# fetch Bitcoin price from Kraken
def fetch_price_kraken_bitcoin():
    url = "https://api.kraken.com/0/public/Ticker"
    params = {"pair": "XBTEUR"}
    try:
        response = requests.get(url, params=params, timeout=5)
        data = response.json()

        logger.info("Bitcoin Kraken API response: %s", data)

        if "error" in data and data["error"]:
            raise ValueError(f" Bitcoin Kraken API returned error: {data['error']}")

        if "result" not in data:
            raise KeyError("'result' key missing in Bitcoin Kraken response")

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

        logger.info(f"Bitcoin Crypto.com API response: {data}")

        tickers = data.get("result", {}).get("data", [])
        if not tickers:
            raise KeyError("No ticker data in Bitcoin Crypto.com response")

        btc_data = tickers[0]  # First item in the list for BTC_EUR

        bid = float(btc_data["b"])  # Best bid
        ask = float(btc_data["k"])  # Best ask

        # Average price
        last_price = (bid + ask) / 2
        return last_price

    except Exception as e:
        logger.exception("Error fetching Bitcoin Crypto.com price")
        return None
# fetch Bitcoin price from Bybit
def fetch_price_bybit_bitcoin():
   try:
     url = "https://api.bybit.com/v5/market/tickers?category=spot&symbol=BTCEUR"
     data = requests.get(url).json()
     logger.info("Bitcoin Bybit API response: %s", data)
     last_price = float(data["result"]["list"][0]["lastPrice"])
     return last_price
   except Exception:
        logger.exception("Error fetching Bitcoin Bybit price")
        return None
# ================ Fetch Ethereum from Binance, Bitfinex, Coinbase, Kraken and Crypto.com APIs ================

# fetch Ethereum price from Binance
def fetch_price_binance_ethereum():
   try:
     url = "https://api.binance.com/api/v3/ticker/price?symbol=ETHEUR"
     data = requests.get(url).json()
     logger.info("Ethereum Binance API response: %s", data)
     return float(data["price"])
   except Exception:
        logger.exception("Error fetching Ethereum Bitfinex price")
        return None

# fetch Ethereum price from Bitfinex
def fetch_price_bitfinex_ethereum():
    try:
      url = "https://api-pub.bitfinex.com/v2/ticker/tETHEUR"
      data = requests.get(url).json()
      logger.info("Ethereum Bitfinex API response: %s", data)
      return float(data[6])  # Last price
    except Exception:
        logger.exception("Error fetching Ethereum Bitfinex price")
        return None
# fetch Ethereum price from Coinbase Exchange
def fetch_price_coinbase_ethereum():
    try:
      url = "https://api.exchange.coinbase.com/products/ETH-EUR/ticker"
      data = requests.get(url).json()
      logger.info("Ethereum Coinbase API response: %s", data)
      return float(data["price"])
    except Exception:
        logger.exception("Error fetching Ethereum Bitfinex price")
        return None
# fetch Ethereum price from Kraken
def fetch_price_kraken_ethereum():
    url = "https://api.kraken.com/0/public/Ticker"
    params = {"pair": "XETHZEUR"}
    try:
        response = requests.get(url, params=params, timeout=5)
        data = response.json()

        logger.info("Ethereum Kraken API response: %s", data)

        if "error" in data and data["error"]:
            raise ValueError(f" Ethereum Kraken API returned error: {data['error']}")

        if "result" not in data:
            raise KeyError("'result' key missing in Ethereum Kraken response")

        result = data["result"]
        key = next(iter(result))
        last_price = result[key]["c"][0]
        return float(last_price)

    except Exception:
        logger.exception("Error fetching Ethereum Kraken price")
        return None

# fetch Ethereum price from Crypto.com
def fetch_price_crypto_exchange_ethereum():
    url = "https://api.crypto.com/v2/public/get-ticker"
    params = {"instrument_name": "ETH_EUR"}
    try:
        response = requests.get(url, params=params, timeout=5)
        data = response.json()

        logger.info(f"Ethereum Crypto.com API response: {data}")

        tickers = data.get("result", {}).get("data", [])
        if not tickers:
            raise KeyError("No ticker data in Ethereum Crypto.com response")

        eth_data = tickers[0]  # First item in the list for ETH_EUR

        bid = float(eth_data["b"])  # Best bid
        ask = float(eth_data["k"])  # Best ask

        # Average price
        last_price = (bid + ask) / 2
        return last_price

    except Exception:
        logger.exception("Error fetching Ethereum Crypto.com price")
        return None

# fetch Bitcoin price from Bybit
def fetch_price_bybit_ethereum():
   try:
     url = "https://api.bybit.com/v5/market/tickers?category=spot&symbol=ETHEUR"
     data = requests.get(url).json()
     logger.info("Ethereum Bybit API response: %s", data)
     last_price = float(data["result"]["list"][0]["lastPrice"])
     return last_price
   except Exception:
        logger.exception("Error fetching Ethereum Bybit price")
        return None