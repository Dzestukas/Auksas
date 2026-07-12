def calculate_intraday_score(row):

    score = 0
    reasons = []


    # H1 trendas pagal EMA
    if row["EMA_50"] > row["EMA_200"]:
        score += 25
        reasons.append("✅ H1 EMA50 virš EMA200 (+25)")
    else:
        reasons.append("❌ H1 EMA50 žemiau EMA200 (0)")


    # Kaina prieš EMA200
    if row["Close"] > row["EMA_200"]:
        score += 20
        reasons.append("✅ Kaina virš EMA200 (+20)")
    else:
        reasons.append("❌ Kaina žemiau EMA200")


    # RSI H1
    if 45 <= row["RSI"] <= 65:
        score += 15
        reasons.append("✅ H1 RSI sveika zona (+15)")
    elif row["RSI"] > 70:
        reasons.append("⚠️ RSI perpirkta")
    else:
        reasons.append("⚠️ RSI silpna")


    # ATR - ar yra judėjimo
    if row["ATR"] > 0:
        score += 10
        reasons.append("✅ Pakankamas volatilumas (+10)")


    # Signalas

    if score >= 60:
        signal = "🟢 BULLISH"

    elif score >= 35:
        signal = "🟡 NEUTRAL"

    else:
        signal = "🔴 BEARISH"


    return score, signal, reasons
