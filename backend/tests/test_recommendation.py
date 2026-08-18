import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.services.recommendation import score_stock


def test_all_positive_signals():
    fundamentals = {
        "pe_ratio": 15,
        "roe": 0.20,
        "debt_to_equity": 30,
        "revenue_growth": 0.15,
        "current_ratio": 2.0,
    }
    technicals = {"rsi": 25, "macd": 5}

    result = score_stock(fundamentals, technicals)

    assert result["score"] == 7  # was 6, corrected
    assert result["recommendation"] == "Strong Buy"
    assert len(result["reasons"]) == 7  # was 6, corrected


def test_all_negative_signals():
    fundamentals = {
        "pe_ratio": 50,
        "roe": 0.02,
        "debt_to_equity": 200,
        "revenue_growth": -0.05,
        "current_ratio": 0.8,
    }
    technicals = {"rsi": 85, "macd": -3}

    result = score_stock(fundamentals, technicals)

    assert result["score"] == -7  # was -6, corrected
    assert result["recommendation"] == "Sell"


def test_all_none_fundamentals_returns_neutral():
    fundamentals = {
        "pe_ratio": None,
        "roe": None,
        "debt_to_equity": None,
        "revenue_growth": None,
        "current_ratio": None,
    }
    technicals = {"rsi": None, "macd": None}

    result = score_stock(fundamentals, technicals)

    assert result["score"] == 0
    assert result["recommendation"] == "Hold"
    assert result["reasons"] == []


def test_mixed_signals_nets_correctly():
    fundamentals = {
        "pe_ratio": 15,      # +1
        "roe": 0.02,         # -1
        "debt_to_equity": 30,  # +1
        "revenue_growth": -0.05,  # -1
        "current_ratio": 2.0,  # +1
    }
    technicals = {"rsi": 50, "macd": 0}  # neutral, no points

    result = score_stock(fundamentals, technicals)

    assert result["score"] == 1
    assert result["recommendation"] == "Hold"


def test_rsi_oversold_signals_buy_direction():
    fundamentals = {}
    technicals = {"rsi": 20, "macd": None}

    result = score_stock(fundamentals, technicals)

    assert result["score"] == 1
    assert "oversold" in result["reasons"][0]


def test_rsi_overbought_signals_sell_direction():
    fundamentals = {}
    technicals = {"rsi": 80, "macd": None}

    result = score_stock(fundamentals, technicals)

    assert result["score"] == -1
    assert "overbought" in result["reasons"][0]


def test_borderline_pe_no_signal():
    # PE exactly 20 shouldn't trigger the "under 20" bonus (boundary check)
    fundamentals = {"pe_ratio": 20}
    technicals = {}

    result = score_stock(fundamentals, technicals)

    assert result["score"] == 0
def test_confidence_high_with_all_signals():
    fundamentals = {
        "pe_ratio": 15,
        "roe": 0.20,
        "debt_to_equity": 30,
        "revenue_growth": 0.15,
        "current_ratio": 2.0,
    }
    technicals = {"rsi": 25, "macd": 5}

    result = score_stock(fundamentals, technicals)

    assert result["signals_evaluated"] == 7
    assert result["confidence_pct"] == 100
    assert result["confidence_label"] == "High"


def test_confidence_low_with_sparse_data():
    fundamentals = {"pe_ratio": 15}
    technicals = {}

    result = score_stock(fundamentals, technicals)

    assert result["signals_evaluated"] == 1
    assert result["confidence_pct"] == 14  # 1/7 rounded
    assert result["confidence_label"] == "Low"    