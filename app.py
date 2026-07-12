import streamlit as st
import yfinance as yf
import pandas as pd

st.title("🟡 Gold Indicator TEST")

gold = yf.download(
    "GC=F",
    period="5d",
    interval="5m"
)

st.write("Duomenys gauti")

st.write(gold.tail())

st.write("Stulpeliai:")
st.write(gold.columns)
