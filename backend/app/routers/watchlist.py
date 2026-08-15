from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Watchlist, User
from app.dependencies import get_current_user

router = APIRouter(prefix="/watchlist", tags=["watchlist"])

@router.post("/{ticker}")
def add_to_watchlist(ticker: str, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    ticker = ticker.upper()
    existing = db.query(Watchlist).filter(
        Watchlist.user_id == user.id, Watchlist.ticker == ticker
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Already in watchlist")

    entry = Watchlist(user_id=user.id, ticker=ticker)
    db.add(entry)
    db.commit()
    return {"message": f"{ticker} added to watchlist"}

@router.delete("/{ticker}")
def remove_from_watchlist(ticker: str, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    entry = db.query(Watchlist).filter(
        Watchlist.user_id == user.id, Watchlist.ticker == ticker.upper()
    ).first()
    if not entry:
        raise HTTPException(status_code=404, detail="Not found in watchlist")

    db.delete(entry)
    db.commit()
    return {"message": f"{ticker} removed from watchlist"}

@router.get("/")
def get_watchlist(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    entries = db.query(Watchlist).filter(Watchlist.user_id == user.id).all()
    return [{"ticker": e.ticker, "added_at": e.added_at} for e in entries]