import streamlit as st
import yfinance as yf
import pandas as pd

st.title("🟡 Gold Terminal V2 - Indicators TEST")

gold = yf.download(
    "GC=F",
    period="30d",
    interval="5m"
)

# Sutvarkome yfinance formatą
if isinstance(gold.columns, pd.MultiIndex):
    gold.columns = gold.columns.get_level_values(0)

gold = gold.dropna()

# EMA
gold["EMA_9"] = gold["Close"].ewm(span=9, adjust=False).mean()
gold["EMA_21"] = gold["Close"].ewm(span=21, adjust=False).mean()
gold["EMA_50"] = gold["Close"].ewm(span=50, adjust=False).mean()

# RSI
delta = gold["Close"].diff()

gain = delta.where(delta > 0, 0)
loss = -delta.where(delta < 0, 0)

avg_gain = gain.rolling(14).mean()
avg_loss = loss.rolling(14).mean()

rs = avg_gain / avg_loss

gold["RSI"] = 100 - (100 / (1 + rs))


last = gold.iloc[-1]

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Gold",
    f"{float(last['Close']):.2f}"
)

col2.metric(
    "EMA 9",
    f"{float(last['EMA_9']):.2f}"
)

col3.metric(
    "EMA 21",
    f"{float(last['EMA_21']):.2f}"
)

col4.metric(
    "RSI",
    f"{float(last['RSI']):.1f}"
)

st.dataframe(
    gold.tail(20)
)
# VWAP
typical_price = (
    gold["High"] +
    gold["Low"] +
    gold["Close"]
) / 3

gold["VWAP"] = (
    (typical_price * gold["Volume"]).cumsum()
    /
    gold["Volume"].cumsum()
)


# Volume analizė
gold["Volume_Avg"] = (
    gold["Volume"]
    .rolling(20)
    .mean()
)

gold["Volume_Spike"] = (
    gold["Volume"] >
    gold["Volume_Avg"] * 1.5
)                                                                                                          
