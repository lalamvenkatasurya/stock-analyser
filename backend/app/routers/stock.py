from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import requests
from app.database import get_db
from app.services.stock_services import get_stock_analysis, get_fundamentals
from app.services.recommendation import score_stock
from app.models import StockAnalysis, Fundamentals
from app.schemas import StockAnalysisResponse, StockHistoryItem, FundamentalsResponse, RecommendationResponse

router = APIRouter(prefix="/stock", tags=["stock"])


@router.get("/search/{query}")
def search_stocks(query: str):
    q = query.strip()
    if not q:
        return []

    url = "https://query1.finance.yahoo.com/v1/finance/search"
    params = {"q": q, "quotesCount": 10, "newsCount": 0}
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        res = requests.get(url, params=params, headers=headers, timeout=5)
        data = res.json()
    except Exception:
        return []

    results = []
    for item in data.get("quotes", []):
        symbol = item.get("symbol", "")
        quote_type = item.get("quoteType", "")
        name = item.get("longname") or item.get("shortname") or symbol

        is_fund_like = "MUTUAL FUND" in name.upper() or "ETF" in name.upper()

        if symbol.endswith(".NS")  and quote_type == "EQUITY" and not is_fund_like:
            results.append({
                "symbol": symbol,
                "name": name,
            })

    return results[:8]


@router.get("/history/{ticker}", response_model=list[StockHistoryItem])
def get_stock_history(ticker: str, db: Session = Depends(get_db)):
    records = (
        db.query(StockAnalysis)
        .filter(StockAnalysis.ticker == ticker.upper())
        .order_by(StockAnalysis.created_at.desc())
        .all()
    )
    if not records:
        raise HTTPException(status_code=404, detail="No history found for this ticker")

    return records


@router.get("/list/tickers")
def list_tracked_tickers(db: Session = Depends(get_db)):
    tickers = db.query(StockAnalysis.ticker).distinct().all()
    return [t[0] for t in tickers]


@router.get("/fundamentals/{ticker}", response_model=FundamentalsResponse)
def read_fundamentals(ticker: str, db: Session = Depends(get_db)):
    ticker = ticker.upper()
    data = get_fundamentals(ticker)
    if data is None:
        raise HTTPException(status_code=404, detail="Fundamentals not found")

    recent = (
        db.query(Fundamentals)
        .filter(Fundamentals.ticker == ticker)
        .filter(Fundamentals.created_at >= datetime.utcnow() - timedelta(hours=24))
        .first()
    )

    if not recent:
        record = Fundamentals(**data)
        db.add(record)
        db.commit()

    return data


@router.get("/recommendation/{ticker}", response_model=RecommendationResponse)
def get_recommendation(ticker: str):
    ticker = ticker.upper()

    technicals = get_stock_analysis(ticker)
    if technicals is None:
        raise HTTPException(status_code=404, detail="Stock not found")

    fundamentals = get_fundamentals(ticker)
    if fundamentals is None:
        raise HTTPException(status_code=404, detail="Fundamentals not found")

    result = score_stock(fundamentals, technicals)
    result["ticker"] = ticker
    result["current_price"] = technicals["current_price"]

    return result


@router.get("/{ticker}", response_model=StockAnalysisResponse)
def read_stock(ticker: str, db: Session = Depends(get_db)):
    result = get_stock_analysis(ticker.upper())
    if result is None:
        raise HTTPException(status_code=404, detail="Stock not found")

    recent = (
        db.query(StockAnalysis)
        .filter(StockAnalysis.ticker == result["ticker"])
        .filter(StockAnalysis.created_at >= datetime.utcnow() - timedelta(hours=1))
        .first()
    )

    if not recent:
        record = StockAnalysis(
            ticker=result["ticker"],
            current_price=result["current_price"],
            rsi=result["rsi"],
            macd=result["macd"],
            volume=result["volume"]
        )
        db.add(record)
        db.commit()
        db.refresh(record)

    return result