import plotly.graph_objects as go


def add_signal_marker(fig, data, signal):

    last_time = data.index[-1]
    last_price = float(data["Close"].iloc[-1])


    if "BUY" in signal:

        fig.add_trace(
            go.Scatter(
                x=[last_time],
                y=[last_price],
                mode="markers+text",
                marker=dict(
                    size=18,
                    symbol="triangle-up"
                ),
                text=["BUY"],
                textposition="top center",
                name="BUY"
            )
        )


    elif "SELL" in signal:

        fig.add_trace(
            go.Scatter(
                x=[last_time],
                y=[last_price],
                mode="markers+text",
                marker=dict(
                    size=18,
                    symbol="triangle-down"
                ),
                text=["SELL"],
                textposition="bottom center",
                name="SELL"
            )
        )


    return fig
