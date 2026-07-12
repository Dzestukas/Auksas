def calculate_risk(row, direction="BUY", risk_reward=2):

    entry = float(row["Close"])
    atr = float(row["ATR"])


    if direction == "BUY":

        stop_loss = entry - atr * 1.5
        take_profit = entry + (entry - stop_loss) * risk_reward


    else:

        stop_loss = entry + atr * 1.5
        take_profit = entry - (stop_loss - entry) * risk_reward


    return {
        "entry": round(entry, 2),
        "stop_loss": round(stop_loss, 2),
        "take_profit": round(take_profit, 2),
        "risk_reward": risk_reward
    }
