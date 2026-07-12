import streamlit as st
import yfinance as yf
import pandas as pd

from indicators import add_indicators
from scoring import calculate_gold_score
from intraday import calculate_intraday_score
from decision import final_decision
from risk import calculate_risk
from chart import create_gold_chart
from history_signals import generate_history_signals
st.set_page_config(
    page_title="Gold Terminal PRO",
    layout="wide"
)


st.title("🟡 Gold Terminal PRO V3")


@st.cache_data(ttl=300)
def load_gold():

    data = yf.download(
        "GC=F",
        period="30d",
        interval="5m"
    )

    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)

    return data.dropna()



gold = load_gold()

gold = add_indicators(gold)
gold = generate_history_signals(gold)

last = gold.iloc[-1]
score, signal, confidence, reasons = calculate_gold_score(last)

c1,c2,c3,c4 = st.columns(4)


c1.metric(
    "Gold",
    f"${float(last['Close']):.2f}"
)

c2.metric(
    "EMA 9",
    f"{float(last['EMA_9']):.2f}"
)

c3.metric(
    "EMA 21",
    f"{float(last['EMA_21']):.2f}"
)

c4.metric(
    "RSI",
    f"{float(last['RSI']):.1f}"
)
st.divider()

st.subheader("🤖 Gold AI Score")

col5, col6 = st.columns(2)

col5.metric(
    "Gold Score",
    f"{score}/100"
)

col6.metric(
    "Signalas",
    signal
)

st.write(
    f"Confidence: {confidence}"
)


with st.expander("🔍 Kodėl toks signalas?"):
    for reason in reasons:
        st.write(reason)

st.subheader("📊 Indicators")

st.dataframe(
    gold.tail(20)
)
st.divider()

st.subheader("📈 Gold Chart")


fig = create_gold_chart(gold.tail(200))


st.plotly_chart(
    fig,
    use_container_width=True
)
st.divider()

st.subheader("🔵 Gold Intraday Radar (H1)")


@st.cache_data(ttl=300)
def load_intraday():

    data = yf.download(
        "GC=F",
        period="100d",
        interval="1h"
    )

    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)

    return data.dropna()



gold_h1 = load_intraday()


gold_h1 = add_indicators(gold_h1)


last_h1 = gold_h1.iloc[-1]


h1_score, h1_signal, h1_reasons = calculate_intraday_score(last_h1)


c7, c8 = st.columns(2)


c7.metric(
    "H1 Score",
    f"{h1_score}/100"
)


c8.metric(
    "H1 Trend",
    h1_signal
)


with st.expander("🔍 H1 analizė"):
    for r in h1_reasons:
        st.write(r)
st.divider()

st.subheader("🧠 GOLD FINAL DECISION")


final_score, final_signal, confidence_final, final_reasons = final_decision(
    score,
    signal,
    h1_score,
    h1_signal
)
if "BUY" in final_signal:
    trade_direction = "BUY"

elif "SELL" in final_signal:
    trade_direction = "SELL"

else:
    trade_direction = "BUY"


risk_plan = calculate_risk(
    last,
    trade_direction
)



d1, d2, d3 = st.columns(3)


d1.metric(
    "Final Score",
    f"{final_score}/100"
)

d2.metric(
    "Final Signal",
    final_signal
)

d3.metric(
    "Confidence",
    confidence_final
)
with st.expander("🔍 Final analizė"):
    for r in final_reasons:
        st.write(r)
st.divider()

st.subheader("🎯 TRADE PLAN")


r1, r2, r3 = st.columns(3)


r1.metric(
    "Entry",
    risk_plan["entry"]
)

r2.metric(
    "Stop Loss",
    risk_plan["stop_loss"]
)

r3.metric(
    "Take Profit",
    risk_plan["take_profit"]
)


st.write(
    f"Risk / Reward: 1 : {risk_plan['risk_reward']}"
)
