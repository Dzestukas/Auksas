import pandas as pd


def generate_history_signals(data):

    signals = []

    for i in range(len(data)):

        row = data.iloc[i]


        signal = ""


        # paprasta pradinė logika
        # vėliau prijungsime pilną AI score

        if (
            row["EMA_50"] > row["EMA_200"]
            and row["RSI"] < 70
        ):
            signal = "BUY"


        elif (
            row["EMA_50"] < row["EMA_200"]
            and row["RSI"] > 30
        ):
            signal = "SELL"


        signals.append(signal)


    data = data.copy()

    data["History_Signal"] = signals


    return data
