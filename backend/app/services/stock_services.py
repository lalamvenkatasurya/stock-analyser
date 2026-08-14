import yfinance as yf
import pandas as pd
import pandas_ta_classic as ta

def get_stock_analysis(ticker: str):
    # NSE stocks need .NS suffix, e.g. RELIANCE.NS
    stock = yf.Ticker(ticker)
    df = stock.history(period="6mo")

    if df.empty:
        return None

    # Calculate indicators
    df["RSI"] = ta.rsi(df["Close"], length=14)
    macd = ta.macd(df["Close"])
    df = pd.concat([df, macd], axis=1)

    latest = df.iloc[-1]

    return {
        "ticker": ticker,
        "current_price": round(latest["Close"], 2),
        "rsi": round(latest["RSI"], 2) if pd.notna(latest["RSI"]) else None,
        "macd": round(latest["MACD_12_26_9"], 2) if pd.notna(latest.get("MACD_12_26_9")) else None,
        "volume": int(latest["Volume"]),
        "history": df["Close"].tail(30).round(2).to_dict()
    }