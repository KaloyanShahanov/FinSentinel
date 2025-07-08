import tkinter as tk
from tkinter import scrolledtext
import logging
import os
import sys
from app.sentinel import start_crypto_monitor, stop_crypto_monitor

# --- Determine absolute log path ---
def get_log_path():
    base_dir = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    # Use fixed path from your request
    return r"C:\Users\GRIGS\source\repos\FinSentinel\FinSentinel\dist\crypto_monitor.log"

log_file_path = get_log_path()

# Ensure the log directory exists
os.makedirs(os.path.dirname(log_file_path), exist_ok=True)

# --- GUI Setup ---
root = tk.Tk()
root.title("Crypto Price Monitor")
root.geometry("550x420")

# --- Status label ---
status_label = tk.Label(root, text="Not monitoring", font=("Arial", 10))
status_label.pack(pady=5)

# --- Log display widget ---
log_display = scrolledtext.ScrolledText(root, width=70, height=18, state='normal', font=("Courier", 9))
log_display.pack(padx=10, pady=10)

# --- Custom log handler for GUI ---
class TextHandler(logging.Handler):
    def __init__(self, widget):
        super().__init__()
        self.widget = widget

    def emit(self, record):
        msg = self.format(record)
        self.widget.after(0, self._write, msg)

    def _write(self, msg):
        self.widget.insert(tk.END, msg + '\n')
        self.widget.see(tk.END)

# --- Logging Setup ---
logger = logging.getLogger()
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

# File handler
file_handler = logging.FileHandler(log_file_path, mode='a', encoding='utf-8')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# GUI handler
gui_handler = TextHandler(log_display)
gui_handler.setFormatter(formatter)
logger.addHandler(gui_handler)

# --- Control functions ---
def start_monitor():
    try:
        start_crypto_monitor()
        status_label.config(text="Monitoring started")
        logging.info("Started crypto monitoring.")
    except Exception as e:
        status_label.config(text="Error starting monitor")
        logging.exception("Failed to start monitoring:")

def stop_monitor():
    try:
        stop_crypto_monitor()
        status_label.config(text="Monitoring stopped")
        logging.info("Stopped crypto monitoring.")
    except Exception as e:
        status_label.config(text="Error stopping monitor")
        logging.exception("Failed to stop monitoring:")

# --- Buttons ---
tk.Label(root, text="FinSentinel Monitor", font=("Arial", 14)).pack(pady=10)
tk.Button(root, text="Start", width=15, command=start_monitor).pack(pady=5)
tk.Button(root, text="Stop", width=15, command=stop_monitor).pack(pady=5)

root.mainloop()
