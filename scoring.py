def calculate_gold_score(row):

    score = 0
    reasons = []

    # EMA trumpas trendas
    if row["EMA_9"] > row["EMA_21"]:
        score += 10
        reasons.append("✅ EMA 9 > EMA 21 (+10)")
    else:
        reasons.append("❌ EMA 9 < EMA 21 (0)")


    # Vidutinis trendas
    if row["EMA_21"] > row["EMA_50"]:
        score += 10
        reasons.append("✅ EMA 21 > EMA 50 (+10)")
    else:
        reasons.append("❌ EMA 21 < EMA 50 (0)")


    # VWAP
    if row["Close"] > row["VWAP"]:
        score += 15
        reasons.append("✅ Kaina virš VWAP (+15)")
    else:
        reasons.append("❌ Kaina žemiau VWAP (0)")


    # RSI
    if 45 <= row["RSI"] <= 65:
        score += 10
        reasons.append("✅ RSI optimali zona (+10)")
    elif row["RSI"] > 70:
        reasons.append("⚠️ RSI perpirkta")
    else:
        reasons.append("⚠️ RSI silpna")


    # Volume
    if row["Volume_Spike"]:
        score += 15
        reasons.append("🔥 Volume spike (+15)")
    else:
        reasons.append("❌ Volume spike nėra")


    # Ilgas trendas
    if row["Close"] > row["EMA_200"]:
        score += 15
        reasons.append("✅ Virš EMA200 (+15)")
    else:
        reasons.append("❌ Žemiau EMA200")


    # ATR - rinkos judėjimas
    if row["ATR"] > 0:
        score += 5
        reasons.append("✅ Yra volatilumas (+5)")


    # Signalas

    if score >= 80:
        signal = "🔥 STRONG BUY"
        confidence = "Aukšta"

    elif score >= 60:
        signal = "🟢 BUY"
        confidence = "Vidutinė"

    elif score >= 40:
        signal = "🟡 WAIT"
        confidence = "Neaišku"

    elif score >= 20:
        signal = "🟠 SELL WATCH"
        confidence = "Silpna"

    else:
        signal = "🔴 STRONG SELL"
        confidence = "Aukšta"


    return score, signal, confidence, reasons
