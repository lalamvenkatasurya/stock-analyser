from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import stock

app = FastAPI(title="Stock Analyser API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten this later for production
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(stock.router)

@app.get("/")
def root():
    return {"status": "Stock Analyser API running"}