import tkinter as tk
from tkinter import messagebox, scrolledtext, filedialog
import time
import os
from datetime import datetime
import pandas as pd

from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame

from config import ALPACA_API_KEY, ALPACA_SECRET_KEY


""""
By - Yash Sarawgi, CFTe, CMT L3
"""


# -----------------------------
# ALPACA CLIENT
# -----------------------------
client = StockHistoricalDataClient(
    ALPACA_API_KEY,
    ALPACA_SECRET_KEY
)

OUTPUT_DIR = ""


# -----------------------------
# HELPER FUNCTIONS
# -----------------------------
def log(message):
    log_box.insert(tk.END, message + "\n")
    log_box.see(tk.END)
    root.update_idletasks()


def choose_folder():
    global OUTPUT_DIR
    folder = filedialog.askdirectory()
    if folder:
        OUTPUT_DIR = folder
        folder_label.config(text=f"Save to: {OUTPUT_DIR}")


# -----------------------------
# FETCH FUNCTION
# -----------------------------
def start_download():
    try:
        if not OUTPUT_DIR:
            messagebox.showerror("Error", "Please choose a save folder")
            return

        tickers = [t.strip().upper() for t in ticker_entry.get().split(",") if t.strip()]
        start_date = datetime.strptime(start_entry.get(), "%Y-%m-%d")
        end_date = datetime.strptime(end_entry.get(), "%Y-%m-%d")
        pause_sec = int(pause_entry.get())

        timeframe_map = {
            "1 Minute": TimeFrame.Minute,
            "5 Minutes": TimeFrame(5, "Min"),
            "15 Minutes": TimeFrame(15, "Min")
        }

        timeframe_label = timeframe_var.get().replace(" ", "")
        timeframe = timeframe_map[timeframe_var.get()]

        if not tickers:
            messagebox.showerror("Error", "No tickers provided")
            return

        log_box.delete("1.0", tk.END)
        log("Starting batch download")
        log(f"Tickers: {', '.join(tickers)}")
        log(f"Date range: {start_entry.get()} → {end_entry.get()}")
        log(f"Pause: {pause_sec} seconds\n")

        for i, symbol in enumerate(tickers, start=1):
            try:
                log(f"[{i}/{len(tickers)}] Fetching {symbol}")

                request = StockBarsRequest(
                    symbol_or_symbols=[symbol],
                    timeframe=timeframe,
                    start=start_date,
                    end=end_date
                )

                bars = client.get_stock_bars(request)
                df = bars.df

                if df.empty:
                    log(f"[WARN] No data for {symbol}\n")
                    time.sleep(pause_sec)
                    continue

                # -----------------------------
                # CLEAN DATA
                # -----------------------------
                df = df.reset_index()
                df["timestamp"] = df["timestamp"].dt.tz_convert("US/Eastern")
                df = df.set_index("timestamp")
                df = df.between_time("09:30", "16:00")
                df = df.sort_index()

                df = df[[
                    "symbol",
                    "open",
                    "high",
                    "low",
                    "close",
                    "volume",
                    "trade_count",
                    "vwap"
                ]]

                filename = (
                    f"{symbol}_"
                    f"{timeframe_label}_"
                    f"{start_entry.get()}_"
                    f"{end_entry.get()}.csv"
                )

                full_path = os.path.join(OUTPUT_DIR, filename)
                df.to_csv(full_path)

                log(f"[OK] Saved → {filename}")
                log(f"Rows: {len(df)}")
                log(f"Sleeping {pause_sec} sec...\n")

                time.sleep(pause_sec)

            except Exception as e:
                log(f"[ERROR] {symbol}: {e}")
                log(f"Sleeping {pause_sec} sec...\n")
                time.sleep(pause_sec)

        log("Batch download completed")

    except Exception as e:
        messagebox.showerror("Error", str(e))


# -----------------------------
# GUI LAYOUT
# -----------------------------
root = tk.Tk()
root.title("Alpaca Batch Intraday Downloader")
root.geometry("560x560")

tk.Label(root, text="Tickers (comma separated)").pack()
ticker_entry = tk.Entry(root, width=65)
ticker_entry.pack()
ticker_entry.insert(0, "AAPL, MSFT, NVDA")

tk.Label(root, text="Timeframe").pack()
timeframe_var = tk.StringVar(value="1 Minute")
tk.OptionMenu(
    root,
    timeframe_var,
    "1 Minute",
    "5 Minutes",
    "15 Minutes"
).pack()

tk.Label(root, text="Start Date (YYYY-MM-DD)").pack()
start_entry = tk.Entry(root)
start_entry.pack()
start_entry.insert(0, "2016-02-01")

tk.Label(root, text="End Date (YYYY-MM-DD)").pack()
end_entry = tk.Entry(root)
end_entry.pack()
end_entry.insert(0, "2026-01-31")

tk.Label(root, text="Pause Between Requests (seconds)").pack()
pause_entry = tk.Entry(root)
pause_entry.pack()
pause_entry.insert(0, "10")

tk.Button(
    root,
    text="Choose Save Folder",
    command=choose_folder,
    bg="#444",
    fg="white"
).pack(pady=5)

folder_label = tk.Label(root, text="Save to: (not selected)", fg="blue")
folder_label.pack()

tk.Button(
    root,
    text="Start Download",
    command=start_download,
    bg="green",
    fg="white",
    height=2
).pack(pady=10)

log_box = scrolledtext.ScrolledText(root, width=70, height=16)
log_box.pack()

root.mainloop()
