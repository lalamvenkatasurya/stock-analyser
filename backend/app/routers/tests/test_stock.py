from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "Stock Analyser API running"

def test_invalid_ticker():
    response = client.get("/stock/ZZZZINVALID")
    assert response.status_code == 404