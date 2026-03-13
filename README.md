# 📈 US Markets OHLC Data Downloader

Python GUI application for downloading **historical intraday OHLCV
market data for US equities** using the **Alpaca Market Data API**.

This tool enables traders, quants, and researchers to easily collect
**clean, structured datasets** suitable for **backtesting, quantitative
analysis, and research pipelines**.

------------------------------------------------------------------------

## 🚀 Key Features

-   📊 Download **historical OHLCV data** for US stocks\
-   ⏱ Supports **intraday timeframes**
    -   1 Minute
    -   5 Minutes
    -   15 Minutes
-   🖥 **Simple GUI interface (Tkinter)**
-   🧹 Automatic **data cleaning and formatting**
-   🕒 Converts timestamps to **US/Eastern timezone**
-   📉 Filters **Regular Trading Hours (09:30--16:00)**
-   📁 Exports clean **CSV datasets**

------------------------------------------------------------------------

## 🖥 Application Overview

The application provides a simple interface where users can:

1.  Enter a stock ticker\
2.  Select a timeframe\
3.  Choose start and end dates\
4.  Download the dataset as a CSV file

This allows quick generation of **ready-to-use datasets for trading
research**.

------------------------------------------------------------------------

## 📂 Project Structure

    US-Markets-OHLC-Data-Downloader
    │
    ├── alpaca_gui.py          # Main GUI application
    ├── alpaca_batch_gui.py    # Batch downloader interface
    ├── config.py              # API configuration (not for public sharing)
    ├── README.md              # Project documentation

------------------------------------------------------------------------

## ⚙️ Installation

### 1️⃣ Clone the repository

``` bash
git clone https://github.com/YOUR_USERNAME/US-Markets-OHLC-Data-Downloader.git
cd US-Markets-OHLC-Data-Downloader
```

### 2️⃣ Install dependencies

``` bash
pip install alpaca-py pandas
```

Tkinter is included with most Python installations.

------------------------------------------------------------------------

### 3️⃣ Configure Alpaca API

Create or edit `config.py`:

``` python
ALPACA_API_KEY = "YOUR_API_KEY"
ALPACA_SECRET_KEY = "YOUR_SECRET_KEY"
```

You can obtain API credentials from:

https://alpaca.markets/

------------------------------------------------------------------------

## ▶️ Usage

Run the GUI application:

``` bash
python alpaca_gui.py
```

Then enter:

  Field        Example
  ------------ ------------
  Ticker       AAPL
  Timeframe    1 Minute
  Start Date   2016-02-01
  End Date     2026-01-31

Click **Fetch Data** and the dataset will be saved automatically.

------------------------------------------------------------------------

## 📊 Output Dataset Format

Example CSV output:

``` csv
timestamp,symbol,open,high,low,close,volume,trade_count,vwap
2016-02-01 09:30:00,AAPL,96.47,96.65,96.32,96.60,120340,850,96.52
```

------------------------------------------------------------------------

## 🧠 Use Cases

This tool is useful for:

-   Quantitative trading research\
-   Strategy backtesting\
-   Machine learning datasets\
-   Market microstructure analysis\
-   Intraday volatility studies

------------------------------------------------------------------------

## ⚠️ Important Notes

-   Data availability depends on your **Alpaca Market Data
    subscription**
-   Free tier may have **historical data limitations**
-   Large requests may take longer due to **API rate limits**

------------------------------------------------------------------------

## 📜 License

MIT License

------------------------------------------------------------------------

## 👨‍💻 Author

**Yash Sarawgi**\
CFTe \| CMT Level III\
Equity Trader & Researcher

------------------------------------------------------------------------

## ⚠️ Disclaimer

This project is intended for **educational and research purposes
only**.\
It does **not constitute financial advice or trading recommendations**.

------------------------------------------------------------------------

## ⭐ Contributing

Contributions, improvements, and feature requests are welcome.

If you find this project useful, consider **starring the repository**.
