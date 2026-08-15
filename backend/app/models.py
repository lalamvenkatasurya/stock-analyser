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