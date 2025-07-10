from ast import Try
import threading
import time
import requests
# from app.shared_queue import price_diff_queue, this module is for real time data to be sent to a graph in the main.py file as we can add application graph there
from app.logger import get_logger
logger = get_logger("price")
from app.alerts import send_slack_alert, send_exchange_rate_alert

running = False
exchange_rate_alert_sent = False

#Import the fetcher functions from the fetcher module

from app.fetchers import (
    fetch_price_kraken_bitcoin,
    fetch_price_crypto_exchange_bitcoin,
    fetch_price_coinbase_bitcoin,
    fetch_price_binance_bitcoin,
    fetch_price_bitfinex_bitcoin,
    fetch_price_bybit_bitcoin,

    fetch_price_binance_ethereum,
    fetch_price_bitfinex_ethereum,
    fetch_price_coinbase_ethereum,
    fetch_price_crypto_exchange_ethereum,
    fetch_price_kraken_ethereum,
    fetch_price_bybit_ethereum
    
)
def monitor_loop():
    global running, exchange_rate_alert_sent
    while running:
        # ============= Bitcoin, Binance vs =============
        # Bitcoin,Binance vs bitfinex
        try:
            price_binance = fetch_price_binance_bitcoin()
            price_bitfinex = fetch_price_bitfinex_bitcoin()

            if price_bitfinex is None:
                logger.info("Skipping Bitcoin = Binance/Bitfinex comparison due to failed price fetch.")
                pass

            avg = (price_binance + price_bitfinex) / 2
            diff = abs(price_binance - price_bitfinex)
            percent_diff = (diff / avg) * 100

            logger.info(f"Bitcoin = Binance: {price_binance:.2f}, Bitfinex: {price_bitfinex:.2f}, Diff: {percent_diff:.2f}%")
           # price_diff_queue.put(("Binance vs Bitfinex", percent_diff, 0)) - this is needed if the import queue module is enabled

            if percent_diff >= 0.2:
                send_slack_alert("Bitcoin", "Binance vs Bitfinex", price_binance, price_bitfinex, percent_diff)

        except Exception:
            logger.exception("Error comparing Bitcoin = Binance vs Bitfinex")
            if not running:
                break
            time.sleep(5)
        # Bitcoin,Binance vs Coinbase
        try:
            price_binance = fetch_price_binance_bitcoin()
            price_coinbase = fetch_price_coinbase_bitcoin()

            if price_coinbase is None:
                logger.info("Skipping Bitcoin = Binance/Coinbase comparison due to failed price fetch.")
                pass

            avg = (price_binance + price_coinbase) / 2
            diff = abs(price_binance - price_coinbase)
            percent_diff = (diff / avg) * 100

            logger.info(f"Bitcoin = Binance: {price_binance:.2f}, Coinbase: {price_coinbase:.2f}, Diff: {percent_diff:.2f}%")
           # price_diff_queue.put(("Binance vs Coinbase", percent_diff, 0)) - this is needed if the import queue module is enabled

            if percent_diff >= 0.2:
                send_slack_alert("Bitcoin", "Binance vs Coinbase", price_binance, price_coinbase, percent_diff)

        except Exception:
            logger.exception("Error comparing Bitcoin = Binance vs Coinbase")
            if not running:
                break
            time.sleep(5)

        # Bitcoin,Binance vs Kraken
        try:
            price_binance = fetch_price_binance_bitcoin()
            price_kraken = fetch_price_kraken_bitcoin()

            if price_kraken is None:
                logger.info("Skipping Bitcoin = Binance/Kraken comparison due to failed price fetch.")
                pass

            avg = (price_binance + price_kraken) / 2
            diff = abs(price_binance - price_kraken)
            percent_diff = (diff / avg) * 100

            logger.info(f"Bitcoin = Binance: {price_binance:.2f}, Kraken: {price_kraken:.2f}, Diff: {percent_diff:.2f}%")
           # price_diff_queue.put(("Binance vs Kraken", percent_diff, 0)) - this is needed if the import queue module is enabled

            if percent_diff >= 0.2:
                send_slack_alert("Bitcoin", "Binance vs Kraken", price_binance, price_kraken, percent_diff)

        except Exception:
            logger.exception("Error comparing Bitcoin = Binance vs Kraken")
            if not running:
                break
            time.sleep(5)

        # Bitcoin,Binance vs crypto.com
        try:
            price_binance = fetch_price_binance_bitcoin()
            price_crypto_exchange = fetch_price_crypto_exchange_bitcoin()

            if price_crypto_exchange is None:
                logger.info("Skipping Bitcoin = Binance/Crypto.com comparison due to failed price fetch.")
                pass

            avg = (price_binance + price_crypto_exchange) / 2
            diff = abs(price_binance - price_crypto_exchange)
            percent_diff = (diff / avg) * 100

            logger.info(f"Bitcoin = Binance: {price_binance:.2f}, Crypto Exchange: {price_crypto_exchange:.2f}, Diff: {percent_diff:.2f}%")
           # price_diff_queue.put(("Binance vs Crypto", percent_diff, 0)) - this is needed if the import queue module is enabled

            if percent_diff >= 0.2:
                send_slack_alert("Bitcoin", "Binance vs Crypto", price_binance, price_crypto_exchange, percent_diff)

        except Exception:
            logger.exception("Error comparing Bitcoin = Binance vs Crypto.com")
            if not running:
                break
            time.sleep(5)

        #Bitcoin,Binance vs Bybit
        try:
            price_binance = fetch_price_binance_bitcoin()
            price_bybit = fetch_price_bybit_bitcoin()

            if price_bybit is None:
                logger.info("Skipping Bitcoin = Binance/Bybit comparison due to failed price fetch.")
                pass

            avg = (price_binance + price_bybit) / 2
            diff = abs(price_binance - price_bybit)
            percent_diff = (diff / avg) * 100

            logger.info(f"Bitcoin = Binance: {price_binance:.6f}, Bybit: {price_bybit:.6f}, Diff: {percent_diff:.8f}%")
           # price_diff_queue.put(("Binance vs Bybit", percent_diff, 0)) - this is needed if the import queue module is enabled

            if percent_diff >= 0.00002:
                send_slack_alert("Bitcoin", "Binance vs Bybit", price_binance, price_bybit, percent_diff)

        except Exception:
            logger.exception("Error comparing Bitcoin = Binance vs Bybit")
            if not running:
                break
            time.sleep(5)

        # ============= Bitcoin, Bitfinex vs =============
        # Bitcoin,Bitfinex vs Coinbase
        try:
            price_bitfinex = fetch_price_bitfinex_bitcoin()
            price_coinbase = fetch_price_coinbase_bitcoin()

            if price_coinbase is None:
                logger.info("Skipping Bitcoin = Bitfinex/Crypto comparison due to failed price fetch.")
                pass

            avg = (price_coinbase + price_bitfinex) / 2
            diff = abs(price_bitfinex - price_coinbase)
            percent_diff = (diff / avg) * 100

            logger.info(f"Bitcoin = Bitfinex: {price_bitfinex:.2f}, Coinbase: {price_coinbase:.2f}, Diff: {percent_diff:.2f}%")
           # price_diff_queue.put(("Bitfinex vs Coinbase", percent_diff, 0)) - this is needed if the import queue module is enabled

            if percent_diff >= 0.2:
                send_slack_alert("Bitcoin", "Bitfinex vs Coinbase", price_bitfinex, price_coinbase, percent_diff)

        except Exception:
            logger.exception("Error comparing Bitcoin = Bitfinex vs Coinbase")
            if not running:
                break
            time.sleep(5)

        # Bitcoin,Bitfinex vs Kraken
        try:
            price_bitfinex = fetch_price_bitfinex_bitcoin()
            price_kraken = fetch_price_kraken_bitcoin()

            if price_kraken is None:
                logger.info("Skipping Bitcoin = Bitfinex/Kraken comparison due to failed price fetch.")
                pass

            avg = (price_bitfinex + price_kraken) / 2
            diff = abs(price_bitfinex - price_kraken)
            percent_diff = (diff / avg) * 100

            logger.info(f"Bitcoin = Bitfinex: {price_bitfinex:.2f}, Kraken: {price_kraken:.2f}, Diff: {percent_diff:.2f}%")
           # price_diff_queue.put(("Bitfinex vs Kraken", percent_diff, 0)) - this is needed if the import queue module is enabled

            if percent_diff >= 0.2:
                send_slack_alert("Bitcoin", "Bitfinex vs Kraken", price_bitfinex, price_kraken, percent_diff)

        except Exception:
            logger.exception("Error comparing Bitcoin = Bitfinex vs Kraken")
            if not running:
                break
            time.sleep(5)
        
        # Bitcoin,Bitfinex vs Crypto.com
        try:
            price_bitfinex = fetch_price_bitfinex_bitcoin()
            price_crypto_exchange = fetch_price_crypto_exchange_bitcoin()

            if price_crypto_exchange is None:
                logger.info("Skipping Bitcoin = Bitfinex/Crypto comparison due to failed price fetch.")
                pass

            avg = (price_crypto_exchange + price_bitfinex) / 2
            diff = abs(price_bitfinex - price_crypto_exchange)
            percent_diff = (diff / avg) * 100

            logger.info(f"Bitcoin = Bitfinex: {price_bitfinex:.2f}, Crypto: {price_crypto_exchange:.2f}, Diff: {percent_diff:.2f}%")
           # price_diff_queue.put(("Bitfinex vs Crypto", percent_diff, 0)) - this is needed if the import queue module is enabled

            if percent_diff >= 0.2:
                send_slack_alert("Bitcoin", "Bitfinex vs Crypto", price_bitfinex, price_crypto_exchange, percent_diff)

        except Exception:
            logger.exception("Error comparing Bitcoin = Bitfinex vs Crypto")
            if not running:
                break
            time.sleep(5)

        #Bitcoin,Bitfinex vs Bybit
        try:
            price_bitfinex = fetch_price_bitfinex_bitcoin()
            price_bybit = fetch_price_bybit_bitcoin()

            if price_bybit is None:
                logger.info("Skipping Bitcoin = Bitfinex/Bybit comparison due to failed price fetch.")
                pass

            avg = (price_bitfinex + price_bybit) / 2
            diff = abs(price_bitfinex - price_bybit)
            percent_diff = (diff / avg) * 100

            logger.info(f"Bitcoin = Bitfinex: {price_bitfinex:.6f}, Bybit: {price_bybit:.6f}, Diff: {percent_diff:.8f}%")
           # price_diff_queue.put(("Bitfinex vs Bybit", percent_diff, 0)) - this is needed if the import queue module is enabled

            if percent_diff >= 0.00002:
                send_slack_alert("Bitcoin", "Bitfinex vs Bybit", price_bitfinex, price_bybit, percent_diff)

        except Exception:
            logger.exception("Error comparing Bitcoin = Bitfinex vs Bybit")
            if not running:
                break
            time.sleep(5)

        # ============= Bitcoin, Coinbase vs =============
        # Bitcoin,Coinbase vs Kraken
        try:
            price_coinbase = fetch_price_coinbase_bitcoin()
            price_kraken = fetch_price_kraken_bitcoin()

            if price_kraken is None:
                logger.info("Skipping Bitcoin = Bitfinex/Kraken comparison due to failed price fetch.")
                pass

            avg = (price_coinbase + price_kraken) / 2
            diff = abs(price_coinbase - price_kraken)
            percent_diff = (diff / avg) * 100

            logger.info(f"Bitcoin = Coinbase: {price_coinbase:.2f}, Kraken: {price_kraken:.2f}, Diff: {percent_diff:.2f}%")
           # price_diff_queue.put(("Coinbase vs Kraken", percent_diff, 0)) - this is needed if the import queue module is enabled

            if percent_diff >= 0.2:
                send_slack_alert("Bitcoin", "Coinbase vs Kraken", price_coinbase, price_kraken, percent_diff)

        except Exception:
            logger.exception("Error comparing Bitcoin = Coinbase vs Kraken")
            if not running:
                break
            time.sleep(5)

        # Bitcoin,Coinbase vs Crypto.com
        try:
            price_coinbase = fetch_price_coinbase_bitcoin()
            price_crypto_exchange = fetch_price_crypto_exchange_bitcoin()

            if price_crypto_exchange is None:
                logger.info("Skipping Bitcoin = Coinbase/Crypto comparison due to failed price fetch.")
                pass

            avg = (price_crypto_exchange + price_coinbase) / 2
            diff = abs(price_coinbase - price_crypto_exchange)
            percent_diff = (diff / avg) * 100

            logger.info(f"Bitcoin = Coinbase: {price_coinbase:.2f}, Crypto: {price_crypto_exchange:.2f}, Diff: {percent_diff:.2f}%")
           # price_diff_queue.put(("Coinbase vs Crypto", percent_diff, 0)) - this is needed if the import queue module is enabled

            if percent_diff >= 0.2:
                send_slack_alert("Bitcoin", "Coinbase vs Crypto", price_coinbase, price_crypto_exchange, percent_diff)

        except Exception:
            logger.exception("Error comparing Bitcoin = Coinbase vs Crypto")
            if not running:
                break
            time.sleep(5)


        #Bitcoin,Bitfinex vs Bybit
        try:
            price_coinbase = fetch_price_coinbase_bitcoin()
            price_bybit = fetch_price_bybit_bitcoin()

            if price_bybit is None:
                logger.info("Skipping Bitcoin = Coinbase/Bybit comparison due to failed price fetch.")
                pass

            avg = (price_coinbase + price_bybit) / 2
            diff = abs(price_coinbase - price_bybit)
            percent_diff = (diff / avg) * 100

            logger.info(f"Bitcoin = Coinbase: {price_coinbase:.6f}, Bybit: {price_bybit:.6f}, Diff: {percent_diff:.8f}%")
           # price_diff_queue.put(("Coinbase vs Bybit", percent_diff, 0)) - this is needed if the import queue module is enabled

            if percent_diff >= 0.00002:
                send_slack_alert("Bitcoin", "Coinbase vs Bybit", price_coinbase, price_bybit, percent_diff)

        except Exception:
            logger.exception("Error comparing Bitcoin = Coinbase vs Bybit")
            if not running:
                break
            time.sleep(5)

        # ============= Bitcoin, Kraken vs =============
        # Bitcoin,Kraken vs Crypto.com
        try:
            price_kraken = fetch_price_kraken_bitcoin()
            price_crypto_exchange = fetch_price_crypto_exchange_bitcoin()

            if price_crypto_exchange is None:
                logger.info("Skipping Bitcoin = Kraken/Crypto comparison due to failed price fetch.")
                pass

            avg = (price_crypto_exchange + price_kraken) / 2
            diff = abs(price_kraken - price_crypto_exchange)
            percent_diff = (diff / avg) * 100

            logger.info(f"Bitcoin = Kraken: {price_kraken:.2f}, Crypto: {price_crypto_exchange:.2f}, Diff: {percent_diff:.2f}%")
           # price_diff_queue.put(("Kraken vs Crypto", percent_diff, 0)) - this is needed if the import queue module is enabled

            if percent_diff >= 0.2:
                send_slack_alert("Bitcoin", "Kraken vs Crypto", price_kraken, price_crypto_exchange, percent_diff)

        except Exception:
            logger.exception("Error comparing Bitcoin = Kraken vs Crypto")
            if not running:
                break
            time.sleep(5)

        #Bitcoin,Kraken vs Bybit
        try:
            price_kraken = fetch_price_kraken_bitcoin()
            price_bybit = fetch_price_bybit_bitcoin()

            if price_bybit is None:
                logger.info("Skipping Bitcoin = Kraken/Bybit comparison due to failed price fetch.")
                pass

            avg = (price_kraken + price_bybit) / 2
            diff = abs(price_kraken - price_bybit)
            percent_diff = (diff / avg) * 100

            logger.info(f"Bitcoin = Kraken: {price_kraken:.6f}, Bybit: {price_bybit:.6f}, Diff: {percent_diff:.8f}%")
           # price_diff_queue.put(("Kraken vs Bybit", percent_diff, 0)) - this is needed if the import queue module is enabled

            if percent_diff >= 0.00002:
                send_slack_alert("Bitcoin", "Kraken vs Bybit", price_kraken, price_bybit, percent_diff)

        except Exception:
            logger.exception("Error comparing Bitcoin = Kraken vs Bybit")
            if not running:
                break
            time.sleep(5)

        # ============= Bitcoin, Crypto vs =============
        #Bitcoin,Crypto vs Bybit
        try:
            price_crypto_exchange = fetch_price_crypto_exchange_bitcoin()
            price_bybit = fetch_price_bybit_bitcoin()

            if price_bybit is None:
                logger.info("Skipping Bitcoin = Crypto/Bybit comparison due to failed price fetch.")
                pass

            avg = (price_crypto_exchange + price_bybit) / 2
            diff = abs(price_crypto_exchange - price_bybit)
            percent_diff = (diff / avg) * 100

            logger.info(f"Bitcoin = Crypto: {price_crypto_exchange:.6f}, Bybit: {price_bybit:.6f}, Diff: {percent_diff:.8f}%")
           # price_diff_queue.put(("Crypto vs Bybit", percent_diff, 0)) - this is needed if the import queue module is enabled

            if percent_diff >= 0.00002:
                send_slack_alert("Bitcoin", "Crypto vs Bybit", price_crypto_exchange, price_bybit, percent_diff)

        except Exception:
            logger.exception("Error comparing Bitcoin = Crypto vs Bybit")
            if not running:
                break
            time.sleep(5)

        # ============= Ethereum, Binance vs =============
        # Ethereum,Binance vs bitfinex
        try:
            price_binance = fetch_price_binance_ethereum()
            price_bitfinex = fetch_price_bitfinex_ethereum()

            if price_bitfinex is None:
                logger.info("Skipping Ethereum = Binance/Bitfinex comparison due to failed price fetch.")
                pass

            avg = (price_binance + price_bitfinex) / 2
            diff = abs(price_binance - price_bitfinex)
            percent_diff = (diff / avg) * 100

            logger.info(f"Ethereum = Binance: {price_binance:.6f}, Bitfinex: {price_bitfinex:.6f}, Diff: {percent_diff:.8f}%")
           # price_diff_queue.put(("Binance vs Bitfinex", percent_diff, 0)) - this is needed if the import queue module is enabled

            if percent_diff >= 0.000002:
                send_slack_alert("Ethereum", "Binance vs Bitfinex", price_binance, price_bitfinex, percent_diff)

        except Exception:
            logger.exception("Error comparing Ethereum = Binance vs Bitfinex")
            if not running:
                break
            time.sleep(5)

        # Ethereum,Binance vs Coinbase
        try:
            price_binance = fetch_price_binance_ethereum()
            price_coinbase = fetch_price_coinbase_ethereum()

            if price_coinbase is None:
                logger.info("Skipping Ethereum = Binance/Coinbase comparison due to failed price fetch.")
                pass

            avg = (price_binance + price_coinbase) / 2
            diff = abs(price_binance - price_coinbase)
            percent_diff = (diff / avg) * 100

            logger.info(f"Ethereum = Binance: {price_binance:.6f}, Coinbase: {price_coinbase:.6f}, Diff: {percent_diff:.8f}%")
           # price_diff_queue.put(("Binance vs Coinbase", percent_diff, 0)) - this is needed if the import queue module is enabled

            if percent_diff >= 0.000002:
                send_slack_alert("Ethereum", "Binance vs Coinbase", price_binance, price_coinbase, percent_diff)

        except Exception:
            logger.exception("Error comparing Ethereum = Binance vs Coinbase")
            if not running:
                break
            time.sleep(5)

        # Ethereum,Binance vs Kraken
        try:
            price_binance = fetch_price_binance_ethereum()
            price_kraken = fetch_price_kraken_ethereum()

            if price_kraken is None:
                logger.info("Skipping Ethereum = Binance/Kraken comparison due to failed price fetch.")
                pass

            avg = (price_binance + price_kraken) / 2
            diff = abs(price_binance - price_kraken)
            percent_diff = (diff / avg) * 100

            logger.info(f"Ethereum = Binance: {price_binance:.6f}, Kraken: {price_kraken:.6f}, Diff: {percent_diff:.8f}%")
           # price_diff_queue.put(("Binance vs Kraken", percent_diff, 0)) - this is needed if the import queue module is enabled

            if percent_diff >= 0.000002:
                send_slack_alert("Ethereum", "Binance vs Kraken", price_binance, price_kraken, percent_diff)

        except Exception:
            logger.exception("Error comparing Ethereum = Binance vs Kraken")
            if not running:
                break
            time.sleep(5)

        # Ethereum,Binance vs crypto.com
        try:
            price_binance = fetch_price_binance_ethereum()
            price_crypto_exchange = fetch_price_crypto_exchange_ethereum()

            if price_crypto_exchange is None:
                logger.info("Skipping Ethereum = Binance/Crypto.com comparison due to failed price fetch.")
                pass

            avg = (price_binance + price_crypto_exchange) / 2
            diff = abs(price_binance - price_crypto_exchange)
            percent_diff = (diff / avg) * 100

            logger.info(f"Ethereum = Binance: {price_binance:.6f}, Crypto Exchange: {price_crypto_exchange:.6f}, Diff: {percent_diff:.8f}%")
           # price_diff_queue.put(("Binance vs Crypto", percent_diff, 0)) - this is needed if the import queue module is enabled

            if percent_diff >= 0.000002:
                send_slack_alert("Ethereum", "Binance vs Crypto", price_binance, price_crypto_exchange, percent_diff)

        except Exception:
            logger.exception("Error comparing Ethereum = Binance vs Crypto.com")
            if not running:
                break
            time.sleep(5)

        #Ethereum,Binance vs Bybit
        try:
            price_binance = fetch_price_binance_ethereum()
            price_bybit = fetch_price_bybit_ethereum()

            if price_bybit is None:
                logger.info("Skipping Ethereum = Binance/Bybit comparison due to failed price fetch.")
                pass

            avg = (price_binance + price_bybit) / 2
            diff = abs(price_binance - price_bybit)
            percent_diff = (diff / avg) * 100

            logger.info(f"Ethereum = Binance: {price_binance:.6f}, Bybit: {price_bybit:.6f}, Diff: {percent_diff:.8f}%")
           # price_diff_queue.put(("Binance vs Bybit", percent_diff, 0)) - this is needed if the import queue module is enabled

            if percent_diff >= 0.00002:
                send_slack_alert("Ethereum", "Binance vs Bybit", price_binance, price_bybit, percent_diff)

        except Exception:
            logger.exception("Error comparing Ethereum = Binance vs Bybit")
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
