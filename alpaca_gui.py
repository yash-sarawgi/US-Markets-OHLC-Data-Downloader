print("GUI script started")

""""
By - Yash Sarawgi, CFTe, CMT L3
"""

import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import pandas as pd

from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame

from config import ALPACA_API_KEY, ALPACA_SECRET_KEY


# -----------------------------
# ALPACA CLIENT
# -----------------------------
client = StockHistoricalDataClient(
    ALPACA_API_KEY,
    ALPACA_SECRET_KEY
)


# -----------------------------
# FETCH FUNCTION
# -----------------------------
def fetch_data():
    try:
        symbol = ticker_entry.get().upper()
        timeframe_str = timeframe_var.get()
        start_date = datetime.strptime(start_entry.get(), "%Y-%m-%d")
        end_date = datetime.strptime(end_entry.get(), "%Y-%m-%d")

        timeframe_map = {
            "1 Minute": TimeFrame.Minute,
            "5 Minutes": TimeFrame(5, "Min"),
            "15 Minutes": TimeFrame(15, "Min")
        }


        request = StockBarsRequest(
            symbol_or_symbols=[symbol],
            timeframe=timeframe_map[timeframe_str],
            start=start_date,
            end=end_date
        )

        bars = client.get_stock_bars(request)
        df = bars.df

        if df.empty:
            messagebox.showerror("Error", "No data returned")
            return

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

        filename = f"{symbol}_{timeframe_str.replace(' ', '')}.csv"
        df.to_csv(filename)

        messagebox.showinfo(
            "Success",
            f"Data saved as {filename}\nRows: {len(df)}"
        )

    except Exception as e:
        messagebox.showerror("Error", str(e))


# -----------------------------
# GUI LAYOUT
# -----------------------------
root = tk.Tk()
root.title("Alpaca Intraday Data Downloader")
root.geometry("420x320")

tk.Label(root, text="Ticker").pack()
ticker_entry = tk.Entry(root)
ticker_entry.pack()
ticker_entry.insert(0, "AAPL")

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

tk.Button(
    root,
    text="Fetch Data",
    command=fetch_data,
    bg="green",
    fg="white"
).pack(pady=15)

root.mainloop()
