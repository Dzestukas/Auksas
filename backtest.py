import pandas as pd


def run_backtest(data, tp_points=15, sl_points=10, max_bars=50):

    trades = []

    i = 0


    while i < len(data) - max_bars:


        signal = data["History_Signal"].iloc[i]


        if signal == "":

            i += 1
            continue


        entry = float(data["Close"].iloc[i])


        future = data.iloc[i+1:i+1+max_bars]


        result = "OPEN"


        if signal == "BUY":

            for _, row in future.iterrows():

                if row["High"] >= entry + tp_points:

                    result = "WIN"
                    break


                if row["Low"] <= entry - sl_points:

                    result = "LOSS"
                    break



        elif signal == "SELL":

            for _, row in future.iterrows():

                if row["Low"] <= entry - tp_points:

                    result = "WIN"
                    break


                if row["High"] >= entry + sl_points:

                    result = "LOSS"
                    break



        trades.append(
            {
                "Signal": signal,
                "Entry": entry,
                "Result": result
            }
        )


        # praleidžiame laiką po sandorio
        i += max_bars


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
