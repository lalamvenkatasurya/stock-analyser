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
class FundamentalsResponse(BaseModel):
    ticker: str
    company_name: Optional[str] = None
    sector: Optional[str] = None
    industry: Optional[str] = None
    pe_ratio: Optional[float] = None
    forward_pe: Optional[float] = None
    pb_ratio: Optional[float] = None
    peg_ratio: Optional[float] = None
    ev_to_ebitda: Optional[float] = None
    price_to_sales: Optional[float] = None
    roe: Optional[float] = None
    roa: Optional[float] = None
    operating_margin: Optional[float] = None
    net_margin: Optional[float] = None
    debt_to_equity: Optional[float] = None
    current_ratio: Optional[float] = None
    quick_ratio: Optional[float] = None
    revenue_growth: Optional[float] = None
    earnings_growth: Optional[float] = None
    dividend_yield: Optional[float] = None
    payout_ratio: Optional[float] = None
    market_cap: Optional[float] = None
    beta: Optional[float] = None
    week52_high: Optional[float] = None
    week52_low: Optional[float] = None
    eps: Optional[float] = None    
class RecommendationResponse(BaseModel):
    ticker: str
    recommendation: str
    score: int
    reasons: list[str]
    current_price: float
    signals_evaluated: int
    total_possible_signals: int
    confidence_pct: int
    confidence_label: str   