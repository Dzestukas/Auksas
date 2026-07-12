import streamlit as st
import pandas as pd

st.title("Pandas test")

df = pd.DataFrame({
    "Price": [4000, 4010, 4020],
    "Volume": [100, 200, 300]
})

st.write(df)
