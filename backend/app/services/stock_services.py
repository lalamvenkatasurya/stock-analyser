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

def get_fundamentals(ticker: str):
    stock = yf.Ticker(ticker)
    info = stock.info

    if not info or "regularMarketPrice" not in info and "currentPrice" not in info:
        return None

    return {
        "ticker": ticker,
        "company_name": info.get("longName"),
        "sector": info.get("sector"),
        "industry": info.get("industry"),

        # Valuation
        "pe_ratio": info.get("trailingPE"),
        "forward_pe": info.get("forwardPE"),
        "pb_ratio": info.get("priceToBook"),
        "peg_ratio": info.get("pegRatio"),
        "ev_to_ebitda": info.get("enterpriseToEbitda"),
        "price_to_sales": info.get("priceToSalesTrailing12Months"),

        # Profitability
        "roe": info.get("returnOnEquity"),
        "roa": info.get("returnOnAssets"),
        "operating_margin": info.get("operatingMargins"),
        "net_margin": info.get("profitMargins"),

        # Financial health
        "debt_to_equity": info.get("debtToEquity"),
        "current_ratio": info.get("currentRatio"),
        "quick_ratio": info.get("quickRatio"),

        # Growth
        "revenue_growth": info.get("revenueGrowth"),
        "earnings_growth": info.get("earningsGrowth"),

        # Dividend
        "dividend_yield": info.get("dividendYield"),
        "payout_ratio": info.get("payoutRatio"),

        # Market context
        "market_cap": info.get("marketCap"),
        "beta": info.get("beta"),
        "week52_high": info.get("fiftyTwoWeekHigh"),
        "week52_low": info.get("fiftyTwoWeekLow"),
        "eps": info.get("trailingEps"),
    }