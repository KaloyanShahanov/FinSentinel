# app/logger.py

import logging
import os
import sys
from datetime import datetime

logger = logging.getLogger("FinSentinel")
logger.setLevel(logging.DEBUG)

if not logger.hasHandlers():
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s')

    # Create logs directory
    log_dir = os.path.join(os.path.dirname(__file__), "..", "logs")
    os.makedirs(log_dir, exist_ok=True)

    # New log filename with timestamp (new file every run)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_filename = f"crypto_monitor_{timestamp}.log"
    log_path = os.path.join(log_dir, log_filename)

    # File handler with new log file every run
    file_handler = logging.FileHandler(log_path, mode='w', encoding='utf-8')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # Stdout handler (for PowerShell or terminal)
   # stream_handler = logging.StreamHandler(sys.stdout)
   # stream_handler.setFormatter(formatter)
   # logger.addHandler(stream_handler)
