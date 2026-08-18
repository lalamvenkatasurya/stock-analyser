def score_stock(fundamentals: dict, technicals: dict) -> dict:
    score = 0
    reasons = []

    # ---- FUNDAMENTALS ----

    pe = fundamentals.get("pe_ratio")
    if pe is not None:
        if 0 < pe < 20:
            score += 1
            reasons.append(f"P/E of {pe:.1f} suggests reasonable valuation")
        elif pe >= 40:
            score -= 1
            reasons.append(f"P/E of {pe:.1f} suggests the stock may be overvalued")

    roe = fundamentals.get("roe")
    if roe is not None:
        if roe > 0.15:
            score += 1
            reasons.append(f"Strong ROE of {roe*100:.1f}% indicates efficient use of equity")
        elif roe < 0.05:
            score -= 1
            reasons.append(f"Weak ROE of {roe*100:.1f}% indicates poor capital efficiency")

    de = fundamentals.get("debt_to_equity")
    if de is not None:
        if de < 50:
            score += 1
            reasons.append(f"Low debt-to-equity ({de:.1f}%) indicates a strong balance sheet")
        elif de > 150:
            score -= 1
            reasons.append(f"High debt-to-equity ({de:.1f}%) indicates elevated financial risk")

    rev_growth = fundamentals.get("revenue_growth")
    if rev_growth is not None:
        if rev_growth > 0.10:
            score += 1
            reasons.append(f"Revenue growing at {rev_growth*100:.1f}%, showing healthy expansion")
        elif rev_growth < 0:
            score -= 1
            reasons.append(f"Revenue declined {abs(rev_growth)*100:.1f}%, a concerning trend")

    cr = fundamentals.get("current_ratio")
    if cr is not None:
        if cr > 1.5:
            score += 1
            reasons.append(f"Current ratio of {cr:.2f} shows solid short-term liquidity")
        elif cr < 1:
            score -= 1
            reasons.append(f"Current ratio of {cr:.2f} may indicate liquidity concerns")

    # ---- TECHNICALS ----

    rsi = technicals.get("rsi")
    if rsi is not None:
        if rsi < 30:
            score += 1
            reasons.append(f"RSI of {rsi:.1f} suggests the stock is oversold, a potential entry point")
        elif rsi > 70:
            score -= 1
            reasons.append(f"RSI of {rsi:.1f} suggests the stock is overbought, caution advised")

    macd = technicals.get("macd")
    if macd is not None:
        if macd > 0:
            score += 1
            reasons.append(f"Positive MACD ({macd:.2f}) indicates bullish momentum")
        elif macd < 0:
            score -= 1
            reasons.append(f"Negative MACD ({macd:.2f}) indicates bearish momentum")

    # ---- FINAL CALL ----

    if score >= 4:
        recommendation = "Strong Buy"
    elif score >= 2:
        recommendation = "Buy"
    elif score <= -3:
        recommendation = "Sell"
    elif score <= -1:
        recommendation = "Weak Sell"
    else:
        recommendation = "Hold"

    return {
        "score": score,
        "recommendation": recommendation,
        "reasons": reasons
    }
def score_stock(fundamentals: dict, technicals: dict) -> dict:
    score = 0
    reasons = []
    signals_evaluated = 0
    total_possible_signals = 7  # pe, roe, debt_to_equity, revenue_growth, current_ratio, rsi, macd

    # ---- FUNDAMENTALS ----

    pe = fundamentals.get("pe_ratio")
    if pe is not None:
        signals_evaluated += 1
        if 0 < pe < 20:
            score += 1
            reasons.append(f"P/E of {pe:.1f} suggests reasonable valuation")
        elif pe >= 40:
            score -= 1
            reasons.append(f"P/E of {pe:.1f} suggests the stock may be overvalued")

    roe = fundamentals.get("roe")
    if roe is not None:
        signals_evaluated += 1
        if roe > 0.15:
            score += 1
            reasons.append(f"Strong ROE of {roe*100:.1f}% indicates efficient use of equity")
        elif roe < 0.05:
            score -= 1
            reasons.append(f"Weak ROE of {roe*100:.1f}% indicates poor capital efficiency")

    de = fundamentals.get("debt_to_equity")
    if de is not None:
        signals_evaluated += 1
        if de < 50:
            score += 1
            reasons.append(f"Low debt-to-equity ({de:.1f}%) indicates a strong balance sheet")
        elif de > 150:
            score -= 1
            reasons.append(f"High debt-to-equity ({de:.1f}%) indicates elevated financial risk")

    rev_growth = fundamentals.get("revenue_growth")
    if rev_growth is not None:
        signals_evaluated += 1
        if rev_growth > 0.10:
            score += 1
            reasons.append(f"Revenue growing at {rev_growth*100:.1f}%, showing healthy expansion")
        elif rev_growth < 0:
            score -= 1
            reasons.append(f"Revenue declined {abs(rev_growth)*100:.1f}%, a concerning trend")

    cr = fundamentals.get("current_ratio")
    if cr is not None:
        signals_evaluated += 1
        if cr > 1.5:
            score += 1
            reasons.append(f"Current ratio of {cr:.2f} shows solid short-term liquidity")
        elif cr < 1:
            score -= 1
            reasons.append(f"Current ratio of {cr:.2f} may indicate liquidity concerns")

    # ---- TECHNICALS ----

    rsi = technicals.get("rsi")
    if rsi is not None:
        signals_evaluated += 1
        if rsi < 30:
            score += 1
            reasons.append(f"RSI of {rsi:.1f} suggests the stock is oversold, a potential entry point")
        elif rsi > 70:
            score -= 1
            reasons.append(f"RSI of {rsi:.1f} suggests the stock is overbought, caution advised")

    macd = technicals.get("macd")
    if macd is not None:
        signals_evaluated += 1
        if macd > 0:
            score += 1
            reasons.append(f"Positive MACD ({macd:.2f}) indicates bullish momentum")
        elif macd < 0:
            score -= 1
            reasons.append(f"Negative MACD ({macd:.2f}) indicates bearish momentum")

    # ---- FINAL CALL ----

    if score >= 4:
        recommendation = "Strong Buy"
    elif score >= 2:
        recommendation = "Buy"
    elif score <= -3:
        recommendation = "Sell"
    elif score <= -1:
        recommendation = "Weak Sell"
    else:
        recommendation = "Hold"

    confidence_pct = round((signals_evaluated / total_possible_signals) * 100)

    if confidence_pct >= 70:
        confidence_label = "High"
    elif confidence_pct >= 40:
        confidence_label = "Medium"
    else:
        confidence_label = "Low"

    return {
        "score": score,
        "recommendation": recommendation,
        "reasons": reasons,
        "signals_evaluated": signals_evaluated,
        "total_possible_signals": total_possible_signals,
        "confidence_pct": confidence_pct,
        "confidence_label": confidence_label,
    }