import plotly.graph_objects as go
from signals import add_history_markers


def create_gold_chart(data):

    fig = go.Figure()


    # Žvakės
    fig.add_trace(
        go.Candlestick(
            x=data.index,
            open=data["Open"],
            high=data["High"],
            low=data["Low"],
            close=data["Close"],
            name="Gold"
        )
    )


    # EMA 50
    fig.add_trace(
        go.Scatter(
            x=data.index,
            y=data["EMA_50"],
            line=dict(width=2),
            name="EMA 50"
        )
    )


    # EMA 200
    fig.add_trace(
        go.Scatter(
            x=data.index,
            y=data["EMA_200"],
            line=dict(width=2),
            name="EMA 200"
        )
    )


    # VWAP
    if "VWAP" in data.columns:

        fig.add_trace(
            go.Scatter(
                x=data.index,
                y=data["VWAP"],
                line=dict(width=2),
                name="VWAP"
            )
        )


    # Istoriniai BUY / SELL signalai
    fig = add_history_markers(
        fig,
        data
    )


    fig.update_layout(
        height=600,
        xaxis_rangeslider_visible=False,
        template="plotly_dark"
    )


    return fig
