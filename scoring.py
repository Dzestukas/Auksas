def calculate_gold_score(row):

    score = 0
    reasons = []

    # EMA trendas
    if row["EMA_9"] > row["EMA_21"]:
        score += 10
        reasons.append("✅ EMA 9 virš EMA 21 (+10)")
    else:
        reasons.append("❌ EMA 9 žemiau EMA 21 (0)")


    if row["EMA_21"] > row["EMA_50"]:
        score += 10
        reasons.append("✅ EMA 21 virš EMA 50 (+10)")
    else:
        reasons.append("❌ EMA 21 žemiau EMA 50 (0)")


    # VWAP
    if row["Close"] > row["VWAP"]:
        score += 15
        reasons.append("✅ Kaina virš VWAP (+15)")
    else:
        reasons.append("❌ Kaina žemiau VWAP (0)")


    # RSI
    if 45 <= row["RSI"] <= 65:
        score += 10
        reasons.append("✅ RSI sveikoje zonoje (+10)")
    elif row["RSI"] > 70:
        reasons.append("⚠️ RSI perpirkta")
    else:
        reasons.append("⚠️ RSI silpnas")


    # Volume
    if row["Volume_Spike"]:
        score += 15
        reasons.append("🔥 Volume spike (+15)")
    else:
        reasons.append("❌ Nėra volume spike")


    # Ilgesnis trendas
    if row["Close"] > row["EMA_200"]:
        score += 15
        reasons.append("✅ Kaina virš EMA200 (+15)")
    else:
        reasons.append("❌ Kaina žemiau EMA200")


    # Momentum
    if row["ATR"] > 0:
        score += 5


    # Sprendimas

    if score >= 80:
        signal = "🔥 STRONG BUY"

    elif score >= 60:
        signal = "🟢 BUY"

    elif score >= 40:
        signal = "🟡 WAIT"

    elif score >= 20:
        signal = "🟠 SELL WATCH"

    else:
        signal = "🔴 STRONG SELL"


    return score, signal, reasons
