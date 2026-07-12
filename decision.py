def final_decision(m5_score, m5_signal, h1_score, h1_signal):

    final_score = 0
    reasons = []


    # M5 svoris 50%
    final_score += m5_score * 0.5

    # H1 svoris 50%
    final_score += h1_score * 0.5


    # Krypties patikrinimas

    if "BUY" in m5_signal and "BULLISH" in h1_signal:
        final_score += 10
        reasons.append(
            "✅ M5 ir H1 sutampa - pirkimo kryptis (+10)"
        )


    elif "SELL" in m5_signal and "BEARISH" in h1_signal:
        final_score += 10
        reasons.append(
            "✅ M5 ir H1 sutampa - pardavimo kryptis (+10)"
        )


    else:
        reasons.append(
            "⚠️ M5 ir H1 kryptys nesutampa"
        )


    # Galutinis signalas

    if final_score >= 85:
        signal = "🔥 STRONG BUY"
        confidence = "90%+"

    elif final_score >= 70:
        signal = "🟢 BUY"
        confidence = "75-90%"

    elif final_score >= 50:
        signal = "🟡 WAIT"
        confidence = "50-70%"

    elif final_score >= 30:
        signal = "🟠 SELL WATCH"
        confidence = "30-50%"

    else:
        signal = "🔴 STRONG SELL"
        confidence = "<30%"


    return round(final_score,1), signal, confidence, reasons
