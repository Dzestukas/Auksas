import streamlit as st
import yfinance as yf

st.title("Gold Data Test")

gold = yf.download(
    "GC=F",
    period="5d",
    interval="5m"
)

st.write("Atsisiųsta")
st.write(gold.shape)
