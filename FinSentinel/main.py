import tkinter as tk
from tkinter import scrolledtext
import logging
import queue
from collections import defaultdict

from app.logger import logger
from app.sentinel import start_crypto_monitor, stop_crypto_monitor
from app.shared_queue import price_diff_queue

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

# === Theme Colors and Fonts ===
BG_COLOR = "#000000"
FG_COLOR = "#00FF00"
BTN_HOVER = "#003300"
FONT = ("Courier New", 11)

# === Setup main window ===
root = tk.Tk()
root.title("FinSentinel")
root.geometry("1920x1080")
root.configure(bg=BG_COLOR)
root.minsize(900, 600)  # Ensure window can’t be too small for buttons

# === Status label ===
status_label = tk.Label(root, text="Not monitoring", font=("Courier New", 12), bg=BG_COLOR, fg=FG_COLOR)
status_label.pack(pady=5)

# === Frames for graph and log side by side ===
frame_graph = tk.Frame(root, bg=BG_COLOR)
frame_graph.pack(side='left', fill='both', expand=True, padx=10, pady=10)

frame_log = tk.Frame(root, bg=BG_COLOR)
frame_log.pack(side='right', fill='both', expand=True, padx=10, pady=10)

# === Log display ===
log_display = tk.Text(frame_log, wrap='word', state='normal', font=FONT, bg=BG_COLOR, fg=FG_COLOR,
                      insertbackground=FG_COLOR, relief='flat')
log_display.pack(side='left', fill='both', expand=True)

scrollbar = tk.Scrollbar(frame_log, command=log_display.yview, bg=BG_COLOR, troughcolor=BG_COLOR,
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

# === Real-time Matplotlib Graph Setup ===
current_price_diffs = defaultdict(lambda: {'max': None, 'min': None})

fig, ax = plt.subplots(figsize=(6, 4))
fig.patch.set_facecolor(BG_COLOR)
ax.set_facecolor(BG_COLOR)
ax.tick_params(axis='x', colors=FG_COLOR)
ax.tick_params(axis='y', colors=FG_COLOR)
for spine in ax.spines.values():
    spine.set_color(FG_COLOR)
ax.title.set_color(FG_COLOR)
ax.set_title('Biggest and Lowest Price Differences per API')
ax.set_xlabel('API / Exchange')
ax.set_ylabel('Difference (%)')

canvas = FigureCanvasTkAgg(fig, master=frame_graph)
canvas_widget = canvas.get_tk_widget()
canvas_widget.pack(fill='both', expand=True, padx=10, pady=10)

exiting = False
process_queue_id = None

# Base colors for each pair:
color_map = {
    "Binance vs Bitfinex": "yellow",
    "Binance vs Crypto": "white",
    "Binance vs Kraken": "lime",
    "Binance vs Bitget": "cyan"
}

def update_graph():
    ax.clear()
    ax.set_facecolor(BG_COLOR)
    ax.tick_params(axis='x', colors=FG_COLOR)
    ax.tick_params(axis='y', colors=FG_COLOR)
    for spine in ax.spines.values():
        spine.set_color(FG_COLOR)
    ax.title.set_color(FG_COLOR)
    ax.set_title('Biggest and Lowest Price Differences per API')
    ax.set_xlabel('API / Exchange')
    ax.set_ylabel('Difference (%)')

    apis = list(current_price_diffs.keys())
    if not apis:
        ax.text(0.5, 0.5, 'No data yet', color=FG_COLOR, ha='center', va='center')
        canvas.draw()
        return

    max_vals = [current_price_diffs[api]['max'] or 0 for api in apis]
    min_vals = [current_price_diffs[api]['min'] or 0 for api in apis]

    max_diff_value = max(max_vals)

    bar_width = 0.35
    x = range(len(apis))

    for i, api in enumerate(apis):
        max_val = max_vals[i]
        min_val = min_vals[i]

        base_color = color_map.get(api, "lime")
        # If this API has the highest max difference, color green, else base color
        max_bar_color = "lime" if max_val == max_diff_value else base_color
        min_bar_color = "red"

        ax.bar(i, max_val, width=bar_width, color=max_bar_color, label='Max Difference' if i == 0 else "")
        ax.bar(i + bar_width, min_val, width=bar_width, color=min_bar_color, label='Min Difference' if i == 0 else "")

    ax.set_xticks([i + bar_width / 2 for i in x])
    ax.set_xticklabels(apis, rotation=30, ha='right')
    ax.legend(facecolor=BG_COLOR, labelcolor=FG_COLOR)
    ax.grid(axis='y', color=FG_COLOR, alpha=0.3)

    canvas.draw()

def process_queue():
    global process_queue_id, exiting
    if exiting:
        return

    updated = False
    while True:
        try:
            api_name, max_diff, min_diff = price_diff_queue.get_nowait()
            current_price_diffs[api_name]['max'] = max_diff
            current_price_diffs[api_name]['min'] = min_diff
            updated = True
        except queue.Empty:
            break

    if updated:
        update_graph()

    process_queue_id = root.after(1000, process_queue)

process_queue_id = root.after(1000, process_queue)

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

    if process_queue_id is not None:
        root.after_cancel(process_queue_id)

    root.destroy()

# === Buttons Frame at bottom center ===
frame_buttons = tk.Frame(root, bg=BG_COLOR)
frame_buttons.pack(side='bottom', fill='x', pady=10)

# Center buttons by adding empty expanding frames left and right
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
