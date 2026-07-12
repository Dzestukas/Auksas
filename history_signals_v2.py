def generate_history_signals_v2(data):

    data = data.copy()


    # Volume patvirtinimas
    data["Volume_Avg"] = (
        data["Volume"]
        .rolling(20)
        .mean()
    )


    data = data.dropna()


    signals = []

    last_signal = ""


    for i in range(len(data)):

        row = data.iloc[i]

        signal = ""


        # BUY signalas
        if (
            row["EMA_50"] > row["EMA_200"]
            and row["Close"] > row["VWAP"]
            and row["RSI"] > 40
            and row["RSI"] < 70
            and row["Volume"] > row["Volume_Avg"]
        ):

            signal = "BUY"


        # SELL signalas
        elif (
            row["EMA_50"] < row["EMA_200"]
            and row["Close"] < row["VWAP"]
            and row["RSI"] > 30
            and row["RSI"] < 60
            and row["Volume"] > row["Volume_Avg"]
        ):

            signal = "SELL"



        # neleidžia kartoti to paties signalo iš eilės
        if signal == last_signal:

            signal = ""


        if signal != "":

            last_signal = signal


        signals.append(signal)



    data["History_Signal"] = signals


    return data
