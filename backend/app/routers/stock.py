from fastapi import APIRouter, HTTPException
from app.services.stock_services import get_stock_analysis

router = APIRouter(prefix="/stock", tags=["stock"])

@router.get("/{ticker}")
def read_stock(ticker: str):
    result = get_stock_analysis(ticker.upper())
    if result is None:
        raise HTTPException(status_code=404, detail="Stock not found")
    return result