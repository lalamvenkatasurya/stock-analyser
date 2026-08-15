from pydantic import BaseModel, field_validator
from datetime import datetime
from typing import Optional

class StockAnalysisResponse(BaseModel):
    ticker: str
    current_price: float
    rsi: Optional[float]
    macd: Optional[float]
    volume: int
    history: dict

class StockHistoryItem(BaseModel):
    id: int
    current_price: float
    rsi: Optional[float]
    macd: Optional[float]
    volume: int
    created_at: datetime

    class Config:
        from_attributes = True  # lets Pydantic read SQLAlchemy objects directly

class TickerRequest(BaseModel):
    ticker: str

    @field_validator("ticker")
    @classmethod
    def ticker_must_be_valid_format(cls, v):
        v = v.strip().upper()
        if not v.replace(".", "").isalnum():
            raise ValueError("Ticker must be alphanumeric (with optional . suffix)")
        return v