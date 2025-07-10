# app/logger.py
import logging
import os
from datetime import datetime

def get_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    if not logger.hasHandlers():
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s')

        base_log_dir = os.path.join(os.path.dirname(__file__), "..", "logs")

        # Decide folder based on logger name (case-insensitive)
        lower_name = name.lower()
        if "price" in lower_name:
            log_dir = os.path.join(base_log_dir, "price_logs")
        elif "fetcher" in lower_name:
            log_dir = os.path.join(base_log_dir, "api_fetcher_logs")
        else:
            log_dir = base_log_dir  # default folder if no match

        os.makedirs(log_dir, exist_ok=True)

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        log_filename = f"{lower_name.replace(' ', '_')}_{timestamp}.log"
        log_path = os.path.join(log_dir, log_filename)

        file_handler = logging.FileHandler(log_path, mode='w', encoding='utf-8')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger


   # Stdout handler (for PowerShell or terminal)
   # stream_handler = logging.StreamHandler(sys.stdout)
   # stream_handler.setFormatter(formatter)
   # logger.addHandler(stream_handler)
