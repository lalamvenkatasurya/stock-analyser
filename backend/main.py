from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import stock
from app.database import engine, Base
from app import models
from app.routers import auth as auth_router
from app.routers import watchlist as watchlist_router


Base.metadata.create_all(bind=engine)

app = FastAPI(title="Stock Analyser API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten this later for production
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(stock.router)
app.include_router(auth_router.router)
app.include_router(watchlist_router.router)
@app.get("/")
def root():
    return {"status": "Stock Analyser API running"}