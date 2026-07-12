import plotly.graph_objects as go


def add_history_markers(fig, data):


    buys = data[data["History_Signal"] == "BUY"]

    sells = data[data["History_Signal"] == "SELL"]


    if not buys.empty:

        fig.add_trace(
            go.Scatter(
                x=buys.index,
                y=buys["Low"],
                mode="markers",
                marker=dict(
                    size=12,
                    symbol="triangle-up"
                ),
                name="BUY"
            )
        )


    if not sells.empty:

        fig.add_trace(
            go.Scatter(
                x=sells.index,
                y=sells["High"],
                mode="markers",
                marker=dict(
                    size=12,
                    symbol="triangle-down"
                ),
                name="SELL"
            )
        )


    return fig
