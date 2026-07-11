import streamlit as st
import yfinance as yf
import pandas as pd
import ta
import requests
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# --- 1. JŪSŲ TELEGRAM BOT DUOMENYS (PILNAI INTEGRUOTA) ---
TELEGRAM_TOKEN = "8746397096:AAG1BrQq76_YuhHhL5f8AXwsX9unnCCCwYI"
TELEGRAM_CHAT_ID = "8198885277"

def send_telegram_message(message):
    url = f"https://telegram.org{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode": "Markdown"}
    try:
        requests.post(url, json=payload)
        return True
    except:
        return False

# Puslapio konfigūracija
st.set_page_config(page_title="Gold Terminal ULTIMATE PRO", layout="wide")
st.title("🏆 Gold Terminal PRO: Auksas, DXY, FED ir Trump + Telegram 🚨")

# Šoninė panelė rizikos valdymui
st.sidebar.header("💰 Rizikos valdymo parametrai")
account_size = st.sidebar.number_input("Jūsų sąskaitos balansas ($)", value=10000, step=500)
risk_percent = st.sidebar.slider("Rizika vienam sandoriui (%)", 0.5, 5.0, 1.0, 0.1)

# --- 2. GYVŲ DUOMENŲ APDOROJIMAS (XAU/USD ir DXY) ---
@st.cache_data(ttl=900)
def load_all_market_data():
    gold = yf.download("GC=F", period="60d", interval="1h")
    dxy = yf.download("DX-Y.NYB", period="60d", interval="1h")
    return gold, dxy

gold_raw, dxy_raw = load_all_market_data()

def process_data(df, is_gold=True):
    df = df.copy()
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
    df = df.ffill().bfill()
    
    # Skaičiuojame techninius indikatorius
    df['EMA_9'] = ta.trend.ema_indicator(df['Close'], window=9)
    df['EMA_21'] = ta.trend.ema_indicator(df['Close'], window=21)
    df['ADX'] = ta.trend.ADXIndicator(df['High'], df['Low'], df['Close'], window=14).adx()
    df['RSI'] = ta.momentum.rsi(df['Close'], window=14)
    
    if is_gold:
        typical_price = (df['High'] + df['Low'] + df['Close']) / 3
        df['VWAP'] = (typical_price * df['Volume']).rolling(window=24, min_periods=1).sum() / df['Volume'].rolling(window=24, min_periods=1).sum()
        df['ATR'] = ta.volatility.average_true_range(df['High'], df['Low'], df['Close'], window=14)
        
    return df

gold_df = process_data(gold_raw, is_gold=True)
dxy_df = process_data(dxy_raw, is_gold=False)

g_last = gold_df.iloc[-1]
d_last = dxy_df.iloc[-1]
d_prev = dxy_df.iloc[-2]

# Dolerio tendencijos nustatymas
dxy_trend = "Stiprėja 📈" if float(d_last['EMA_9']) > float(d_last['EMA_21']) else "Silpnėja 📉"
dxy_change = float(d_last['Close']) - float(d_prev['Close'])

# --- 3. SIGNALŲ GENERAVIMO ALGORITMAS ---
signal_type = "NEUTRALUS (Laukite)"
stop_loss, take_profit, position_size_lots = 0.0, 0.0, 0.0
reason = "Rinka neturi aiškaus trendo (ADX per žemas) arba kaina konsoliduojasi aplink VWAP."

current_price = float(g_last['Close'])
vwap_val = float(g_last['VWAP'])
adx_val = float(g_last['ADX'])
atr_value = float(g_last['ATR'])

is_trending = adx_val > 25

if is_trending:
    # BUY sąlyga: Kaina virš VWAP, EMA rodo kilimą IR Doleris silpnėja
    if current_price > vwap_val and float(g_last['EMA_9']) > float(g_last['EMA_21']) and "Silpnėja" in dxy_trend:
        signal_type = "BUY (PIRKTI)"
        stop_loss = current_price - (1.5 * atr_value)
        take_profit = current_price + (3.0 * atr_value)
        reason = f"Auksas virš VWAP. ADX patvirtina jėgą. JAV Doleris (DXY) silpnėja, kas suteikia papildomo stūmimo aukštyn."
        
    # SELL sąlyga: Kaina žemiau VWAP, EMA rodo kritimą IR Doleris stiprėja
    elif current_price < vwap_val and float(g_last['EMA_9']) < float(g_last['EMA_21']) and "Stiprėja" in dxy_trend:
        signal_type = "SELL (PARDUOTI)"
        stop_loss = current_price + (1.5 * atr_value)
        take_profit = current_price - (3.0 * atr_value)
        reason = f"Auksas žemiau VWAP. ADX patvirtina jėgą. JAV Doleris (DXY) stiprėja, spausdamas aukso kainą žemyn."

# Lotų skaičiuoklė
if stop_loss > 0:
    signal_loss_dist = abs(current_price - stop_loss)
    allowed_loss_usd = account_size * (risk_percent / 100)
    position_size_lots = allowed_loss_usd / (signal_loss_dist * 100)

# --- 4. PANELĖS ATVAIZDAVIMAS ---
st.subheader("📊 Pagrindinės Rinkos Metrikos")
col_g, col_d, col_s = st.columns(3)

with col_g:
    st.metric("Aukso kaina (XAU/USD)", f"${current_price:,.2f}", f"ADX: {adx_val:.2f}")
    st.caption(f"VWAP lygis: ${vwap_val:,.2f} | RSI: {float(g_last['RSI']):.2f}")

with col_d:
    st.metric("JAV Dolerio Indeksas (DXY)", f"{float(d_last['Close']):.2f}", f"{dxy_change:+.2f} ({dxy_trend})")
    st.caption(f"DXY RSI: {float(d_last['RSI']):.2f} (Jei RSI > 70, doleris perpirktas -> auksas gali kilti)")

with col_s:
    st.markdown(f"**Strategijos Nuosprendis:**<br><span style='font-size:24px; font-weight:bold; color:{'#2ecc71' if 'BUY' in signal_type else ('#e74c3c' if 'SELL' in signal_type else '#7f8c8d')}'>{signal_type}</span>", unsafe_allow_html=True)
    st.caption(f"**Logika:** {reason}")

st.markdown("---")

# Tikslūs prekybos rėžiai ekrane (pasirodo tik kai yra signalas)
if stop_loss > 0:
    st.subheader("🎯 Tikslūs Prekybos Rėžiai")
    col_t1, col_t2, col_t3, col_t4 = st.columns(4)
    col_t1.metric("Įėjimo kaina", f"${current_price:,.2f}")
    col_t2.metric("🛑 STOP LOSS", f"${stop_loss:,.2f}")
    col_t3.metric("🎯 TAKE PROFIT", f"${take_profit:,.2f}")
    col_t4.metric("📊 REKOMENDUOJAMAS DYDIS", f"{position_size_lots:.2f} Lot", f"Rizika: ${account_size * (risk_percent / 100):.2f}")
    st.markdown("---")

# --- KORELIACIJOS GRAFIKAI ---
st.subheader("📈 Koreliacijos Grafikai")
fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.08, row_heights=[0.5, 0.5])
fig.add_trace(go.Scatter(x=gold_df.index, y=gold_df['Close'], name="Auksas (XAU/USD)", line=dict(color='#f39c12', width=2)), row=1, col=1)
fig.add_trace(go.Scatter(x=gold_df.index, y=gold_df['VWAP'], name="Aukso VWAP", line=dict(color='#9b59b6', width=1, dash='dash')), row=1, col=1)
fig.add_trace(go.Scatter(x=dxy_df.index, y=dxy_df['Close'], name="Dolerio indeksas (DXY)", line=dict(color='#3498db', width=2)), row=2, col=1)
fig.update_layout(height=550, template="plotly_dark", margin=dict(l=20, r=20, t=10, b=10))
st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# --- 5. NAUJIENŲ FILTRAS (FED & TRUMP) ---
st.subheader("📰 Svarbiausios Naujienos (FED, Trump, Makroekonomika)")
try:
    gold_ticker = yf.Ticker("GC=F")
    all_news = gold_ticker.news
    col_fed, col_trump, col_general = st.columns(3)
    
    with col_fed:
        st.markdown("🏛️ **FED & Palūkanų Normos**")
        fed_count = 0
        for n in all_news:
            t_low = n['title'].lower()
            if any(w in t_low for w in ["fed", "powell", "rate", "fomc", "inflation", "cpi"]):
                st.markdown(f"🔹 [{n['title']}]({n['link']})")
                fed_count += 1
        if fed_count == 0: st.caption("Šiuo metu specifinių FED naujienų nėra.")

    with col_trump:
        st.markdown("🇺🇸 **Trump & JAV Politika**")
        trump_count = 0
        for n in all_news:
            t_low = n['title'].lower()
            if any(w in t_low for w in ["trump", "tariff", "election", "policy"]):
                st.markdown(f"🔸 [{n['title']}]({n['link']})")
                trump_count += 1
        if trump_count == 0: st.caption("Šiuo metu specifinių Trumpo naujienų nėra.")

    with col_general:
        st.markdown("🌐 **Bendros Rinkos Žinios**")
        for n in all_news[:4]:
            st.markdown(f"▪️ [{n['title']}]({n['link']})")
except:
    st.write("Nepavyko užkrauti naujienų filtro.")

# --- 6. AUTOMATINIS TELEGRAM PRANEŠĖJAS (FONINIS SEKMAS) ---
if 'last_signal' not in st.session_state:
    st.session_state.last_signal = "NEUTRALUS"

tg_message = f"🚨 *XAU/USD Naujas Signalas* 🚨\nNuosprendis: *{signal_type}*\n\n📈 Įėjimas: ${current_price:,.2f}\n🛑 SL: ${stop_loss:,.2f}\n🎯 TP: ${take_profit:,.2f}\n📊 Dydis: {position_size_lots:.2f} Lot\n\n💵 *DXY būsena:* {dxy_trend} (${float(d_last['Close']):.2f})"

# Jei atsiranda realus signalas ir jis pasikeitė nuo buvusio – siunčiame žinutę
if signal_type != "NEUTRALUS (Laukite)" and signal_type != st.session_state.last_signal:
    send_telegram_message(tg_message)
    st.session_state.last_signal = signal_type
