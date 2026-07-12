import streamlit as st
import yfinance as yf
import pandas as pd

from indicators import add_indicators
from scoring import calculate_gold_score

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
