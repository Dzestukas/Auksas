import streamlit as st
import yfinance as yf

st.title("🟡 Gold Terminal V2 TEST")

gold = yf.download(
    "GC=F",
    period="5d",
    interval="5m"
)

st.write("Aukso duomenys:")
st.dataframe(gold.tail())
