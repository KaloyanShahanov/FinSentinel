import threading
import time
import requests

from app.logger import logger
from app.alerts import send_slack_alert

def fetch_price_bitget():
    url = "https://api.bitget.com/api/v2/mix/market/tickers?productType=COIN-FUTURES"
    params = {"lastPr": "BTCEUR"}
    try:
        response = requests.get(url, params=params, timeout=5)
        data = response.json()

        logger.info("Bitget API response: %s", data)

        if "error" in data and data["error"]:
            raise ValueError(f"Bitget API returned error: {data['error']}")

        if "result" not in data:
            raise KeyError("'result' key missing in Bitget response")

        result = data["lastpr"]
        key = next(iter(result))
        last_price = result[key]["lastPr"][0]

    except Exception as e:
        logger.exception("Error fetching Bitget price")
        return None




