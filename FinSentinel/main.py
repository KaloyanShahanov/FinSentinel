import tkinter as tk
import logging

from app.logger import logger
from app.sentinel import start_crypto_monitor, stop_crypto_monitor

# === Theme Colors and Fonts ===
BG_COLOR = "#000000"
FG_COLOR = "#00FF00"
BTN_HOVER = "#003300"
FONT = ("Courier New", 11)

# === Setup main window ===
root = tk.Tk()
root.title("FinSentinel")
root.geometry("1920x1080")
root.minsize(900, 600)
root.configure(bg=BG_COLOR)

# === Status label ===
status_label = tk.Label(root, text="Not monitoring", font=("Courier New", 12), bg=BG_COLOR, fg=FG_COLOR)
status_label.pack(pady=5)

# === Log display ===
log_display = tk.Text(root, wrap='word', state='normal', font=FONT, bg=BG_COLOR, fg=FG_COLOR,
                      insertbackground=FG_COLOR, relief='flat')
log_display.pack(side='left', fill='both', expand=True, padx=10, pady=10)

scrollbar = tk.Scrollbar(root, command=log_display.yview, bg=BG_COLOR, troughcolor=BG_COLOR,
                         activebackground=BTN_HOVER)
scrollbar.pack(side='left', fill='y', pady=10)

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

exiting = False

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

def exit_app():
    global exiting
    exiting = True
    try:
        stop_crypto_monitor()
    except Exception:
        logger.exception("Exception stopping monitor on exit")
    root.destroy()

# === Buttons Frame at bottom center ===
frame_buttons = tk.Frame(root, bg=BG_COLOR)
frame_buttons.pack(side='bottom', fill='x', pady=10)

left_spacer = tk.Frame(frame_buttons, bg=BG_COLOR)
left_spacer.pack(side='left', expand=True, fill='x')

btn_start = tk.Button(frame_buttons, text="Start", font=("Courier New", 14, "bold"), width=12,
                      command=start_monitor,
                      bg=BG_COLOR, fg=FG_COLOR, activebackground=BTN_HOVER, activeforeground=FG_COLOR)
btn_start.pack(side='left', padx=10, pady=10)

btn_stop = tk.Button(frame_buttons, text="Stop", font=("Courier New", 14, "bold"), width=12,
                     command=stop_monitor,
                     bg=BG_COLOR, fg=FG_COLOR, activebackground=BTN_HOVER, activeforeground=FG_COLOR)
btn_stop.pack(side='left', padx=10, pady=10)

btn_exit = tk.Button(frame_buttons, text="Exit", font=("Courier New", 14, "bold"), width=12,
                     command=exit_app,
                     bg=BG_COLOR, fg="red", activebackground="#330000", activeforeground=FG_COLOR)
btn_exit.pack(side='left', padx=10, pady=10)

right_spacer = tk.Frame(frame_buttons, bg=BG_COLOR)
right_spacer.pack(side='left', expand=True, fill='x')

# === Run ===
root.mainloop()
