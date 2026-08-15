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