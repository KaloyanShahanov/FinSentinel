import tkinter as tk
from app.sentinel import start_crypto_monitor, stop_crypto_monitor

# GUI Setup
root = tk.Tk()
root.title("Crypto Price Monitor")
root.geometry("300x150")

def start_monitor():
    start_crypto_monitor()
    status_label.config(text="Monitoring started")

def stop_monitor():
    stop_crypto_monitor()
    status_label.config(text="Monitoring stopped")

tk.Label(root, text="FinSentinel Monitor", font=("Arial", 14)).pack(pady=10)

tk.Button(root, text="Start", width=15, command=start_monitor).pack(pady=5)
tk.Button(root, text="Stop", width=15, command=stop_monitor).pack(pady=5)

status_label = tk.Label(root, text="Not monitoring")
status_label.pack(pady=10)

root.mainloop()
