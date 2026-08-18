from sqlalchemy import Column, ForeignKey, Integer, String, Float, DateTime
from datetime import datetime
from app.database import Base

class StockAnalysis(Base):
    __tablename__ = "stock_analysis"

    id = Column(Integer, primary_key=True, index=True)
    ticker = Column(String(20), index=True)
    current_price = Column(Float)
    rsi = Column(Float)
    macd = Column(Float)
    volume = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(120), unique=True, index=True)
    hashed_password = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)    
class Watchlist(Base):
    __tablename__ = "watchlist"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    ticker = Column(String(20))
    added_at = Column(DateTime, default=datetime.utcnow)    
class Fundamentals(Base):
    __tablename__ = "fundamentals"

    id = Column(Integer, primary_key=True, index=True)
    ticker = Column(String(20), index=True)
    company_name = Column(String(120), nullable=True)
    sector = Column(String(80), nullable=True)
    industry = Column(String(120), nullable=True)

    pe_ratio = Column(Float, nullable=True)
    forward_pe = Column(Float, nullable=True)
    pb_ratio = Column(Float, nullable=True)
    peg_ratio = Column(Float, nullable=True)
    ev_to_ebitda = Column(Float, nullable=True)
    price_to_sales = Column(Float, nullable=True)

    roe = Column(Float, nullable=True)
    roa = Column(Float, nullable=True)
    operating_margin = Column(Float, nullable=True)
    net_margin = Column(Float, nullable=True)

    debt_to_equity = Column(Float, nullable=True)
    current_ratio = Column(Float, nullable=True)
    quick_ratio = Column(Float, nullable=True)

    revenue_growth = Column(Float, nullable=True)
    earnings_growth = Column(Float, nullable=True)

    dividend_yield = Column(Float, nullable=True)
    payout_ratio = Column(Float, nullable=True)

    market_cap = Column(Float, nullable=True)
    beta = Column(Float, nullable=True)
    week52_high = Column(Float, nullable=True)
    week52_low = Column(Float, nullable=True)
    eps = Column(Float, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)    