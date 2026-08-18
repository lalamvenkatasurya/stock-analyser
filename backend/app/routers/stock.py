from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app.database import get_db
from app.services.stock_services import get_stock_analysis
from app.models import StockAnalysis
from app.schemas import StockAnalysisResponse, StockHistoryItem

router = APIRouter(prefix="/stock", tags=["stock"])


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

    return [
        {
            "id": r.id,
            "current_price": r.current_price,
            "rsi": r.rsi,
            "macd": r.macd,
            "volume": r.volume,
            "created_at": r.created_at
        }
        for r in records
    ]


@router.get("/list/tickers" )
def list_tracked_tickers(db: Session = Depends(get_db)):
    tickers = db.query(StockAnalysis.ticker).distinct().all()
    return [t[0] for t in tickers]




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
from app.services.stock_services import get_stock_analysis, get_fundamentals
from app.models import StockAnalysis, Fundamentals
from app.schemas import StockAnalysisResponse, StockHistoryItem, FundamentalsResponse

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
from app.services.recommendation import score_stock
from app.schemas import RecommendationResponse

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