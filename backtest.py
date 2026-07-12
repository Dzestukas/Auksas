import pandas as pd


def run_backtest(data, tp_points=15, sl_points=10):

    trades = []

    for i in range(len(data) - 1):

        signal = data["History_Signal"].iloc[i]

        entry = float(data["Close"].iloc[i])


        if signal == "BUY":

            future = data.iloc[i+1:]

            hit_tp = future["High"].max() >= entry + tp_points
            hit_sl = future["Low"].min() <= entry - sl_points


            if hit_tp and not hit_sl:
                result = "WIN"

            elif hit_sl:
                result = "LOSS"

            else:
                result = "OPEN"


            trades.append({
                "Signal": "BUY",
                "Entry": entry,
                "Result": result
            })


        elif signal == "SELL":

            future = data.iloc[i+1:]

            hit_tp = future["Low"].min() <= entry - tp_points
            hit_sl = future["High"].max() >= entry + sl_points


            if hit_tp and not hit_sl:
                result = "WIN"

            elif hit_sl:
                result = "LOSS"

            else:
                result = "OPEN"


            trades.append({
                "Signal": "SELL",
                "Entry": entry,
                "Result": result
            })


    results = pd.DataFrame(trades)


    if len(results) == 0:
        return results, 0


    wins = len(
        results[results["Result"] == "WIN"]
    )


    win_rate = round(
        wins / len(results) * 100,
        2
    )


    return results, win_rate
