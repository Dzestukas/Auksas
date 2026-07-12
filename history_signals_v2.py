import pandas as pd


def generate_history_signals_v2(data):

    data = data.copy()

    signals = []

    last_signal = ""


    for i in range(len(data)):

        row = data.iloc[i]


        signal = ""


        # BUY sąlygos
        if (
            row["EMA_50"] > row["EMA_200"]
            and row["Close"] > row["VWAP"]
            and row["RSI"] > 45
            and row["RSI"] < 65
            and row["Volume"] > row["Volume_Avg"]
        ):

            signal = "BUY"


        # SELL sąlygos
        elif (
            row["EMA_50"] < row["EMA_200"]
            and row["Close"] < row["VWAP"]
            and row["RSI"] > 35
            and row["RSI"] < 55
            and row["Volume"] > row["Volume_Avg"]
        ):

            signal = "SELL"


        # leidžiame tik naują signalą
        if signal == last_signal:

            signal = ""


        if signal != "":
            last_signal = signal


        signals.append(signal)


    data["History_Signal"] = signals


    return data
