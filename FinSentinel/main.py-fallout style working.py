import tkinter as tk
from tkinter import scrolledtext
import logging
import os
import sys

from app.logger import logger
from app.sentinel import start_crypto_monitor, stop_crypto_monitor

# Colors (Fallout 4 style)
BG_COLOR = "#000000"
FG_COLOR = "#00FF00"
BTN_HOVER = "#003300"
FONT = ("Courier New", 11)

# Determine absolute log path
def get_log_path():
    base_dir = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return r"C:\Users\GRIGS\source\repos\FinSentinel\FinSentinel\logs\crypto_monitor.log"

log_file_path = get_log_path()
os.makedirs(os.path.dirname(log_file_path), exist_ok=True)

# Main window
root = tk.Tk()
root.title("FinSentinel")  # Set window title for taskbar & window frame

# Set your own .ico file path here (or comment out if no icon available)
# Make sure the file exists at this location
icon_path = r"C:\Users\GRIGS\source\repos\FinSentinel\FinSentinel\assets\icon.ico"
if os.path.exists(icon_path):
    root.iconbitmap(icon_path)

root.overrideredirect(False)  # Use normal window decorations (title bar, icon, buttons)
root.geometry("1280x720")
root.configure(bg=BG_COLOR)

# === Custom Title Bar (you can keep or remove this, since we have default frame now) ===
# You can comment out the entire custom title bar section if you want default Windows title bar and controls

# ... (your existing custom title bar code can be removed or kept here as you wish) ...

# For now, I recommend removing custom title bar since overrideredirect is False
# and you want the native window frame with icon and controls

# === Status label ===
status_label = tk.Label(root, text="Not monitoring", font=("Courier New", 12), bg=BG_COLOR, fg=FG_COLOR)
status_label.pack(pady=5)

# === Log display ===
frame = tk.Frame(root, bg=BG_COLOR)
frame.pack(fill='both', expand=True, padx=10, pady=10)

log_display = tk.Text(frame, wrap='word', state='normal', font=FONT, bg=BG_COLOR, fg=FG_COLOR,
                      insertbackground=FG_COLOR, relief='flat')
log_display.pack(side='left', fill='both', expand=True)

scrollbar = tk.Scrollbar(frame, command=log_display.yview, bg=BG_COLOR, troughcolor=BG_COLOR,
                         activebackground=BTN_HOVER)
scrollbar.pack(side='right', fill='y')

log_display.config(yscrollcommand=scrollbar.set)

# === GUI log handler ===
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

gui_handler = TextHandler(log_display)
gui_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(gui_handler)

# === Control functions ===
def start_monitor():
    try:
        start_crypto_monitor()
        status_label.config(text="Monitoring started")
        logger.info("Started crypto monitoring.")
    except Exception:
        status_label.config(text="Error starting monitor")
        logger.exception("Failed to start monitoring")

def stop_monitor():
    try:
        stop_crypto_monitor()
        status_label.config(text="Monitoring stopped")
        logger.info("Stopped crypto monitoring.")
    except Exception:
        status_label.config(text="Error stopping monitor")
        logger.exception("Failed to stop monitoring")

# === Buttons ===
tk.Button(root, text="Start", font=FONT, command=start_monitor,
          bg=BG_COLOR, fg=FG_COLOR, activebackground=BTN_HOVER, activeforeground=FG_COLOR).pack(pady=5)

tk.Button(root, text="Stop", font=FONT, command=stop_monitor,
          bg=BG_COLOR, fg=FG_COLOR, activebackground=BTN_HOVER, activeforeground=FG_COLOR).pack(pady=5)

# Run
root.mainloop()
