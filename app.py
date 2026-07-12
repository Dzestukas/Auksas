import streamlit as st
import yfinance as yf
import pandas as pd
import ta
import requests
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# --- 1. TELEGRAM INTEGRACIJA ---
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

st.set_page_config(page_title="Gold 100-Score Terminal", layout="wide")
st.title("🏆 Gold Terminal PRO: 100 Balų „Gold Score“ + Dinaminis RSI 🚨")

st.sidebar.header("💰 Rizikos valdymas")
account_size = st.sidebar.number_input("Sąskaitos balansas ($)", value=10000, step=500)
risk_percent = st.sidebar.slider("Rizika sandoriui (%)", 0.5, 5.0, 1.0, 0.1)

# --- 2. MULTI-TIMEFRAME DUOMENŲ APDOROJIMAS ---
@st.cache_data(ttl=300)
def load_all_data():
    gold_5m = yf.download("GC=F", period="30d", interval="5m")
    gold_4h = yf.download("GC=F", period="100d", interval="4h")
    dxy_5m = yf.download("DX-Y.NYB", period="30d", interval="5m")
    return gold_5m, gold_4h, dxy_5m

g_5m_raw, g_4h_raw, d_5m_raw = load_all_data()

def clean_and_calculate(df, is_gold=True, is_4h=False):
    df = df.copy()
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
    df = df.ffill().bfill()
    
    df['EMA_9'] = ta.trend.ema_indicator(df['Close'], window=9)
    df['EMA_21'] = ta.trend.ema_indicator(df['Close'], window=21)
    df['EMA_200'] = ta.trend.ema_indicator(df['Close'], window=200)
    df['RSI'] = ta.momentum.rsi(df['Close'], window=14)
    df['ADX'] = ta.trend.ADXIndicator(df['High'], df['Low'], df['Close'], window=14).adx()
    
    if is_gold and not is_4h:
        typical_price = (df['High'] + df['Low'] + df['Close']) / 3
        df['VWAP'] = (typical_price * df['Volume']).rolling(window=24, min_periods=1).sum() / df['Volume'].rolling(window=24, min_periods=1).sum()
        df['ATR'] = ta.volatility.average_true_range(df['High'], df['Low'], df['Close'], window=14)
        
    return df

gold_df = clean_and_calculate(g_5m_raw, is_gold=True, is_4h=False)
g_4h = clean_and_calculate(g_4h_raw, is_gold=True, is_4h=True)
d_5m = clean_and_calculate(d_5m_raw, is_gold=False, is_4h=False)

g5 = gold_df.iloc[-1]
g4 = g_4h.iloc[-1]
d5 = d_5m.iloc[-1]

current_price = float(g5['Close'])
vwap_val = float(g5['VWAP'])
adx_val = float(g5['ADX'])
atr_val = float(g5['ATR'])
rsi_val = float(g5['RSI'])

# --- 3. NAUJIENŲ ANALIZATORIUS FONE (FED IR TRUMP RIZIKA) ---
fed_risk_score = 10
trump_risk_score = 10
try:
    ticker = yf.Ticker("GC=F")
    for n in ticker.news:
        t_low = n['title'].lower()
        if any(w in t_low for w in ["fed", "powell", "rate hike", "fomc", "hawkish"]):
            fed_risk_score = 0
        if any(w in t_low for w in ["trump", "tariff", "trade war", "sanctions"]):
            trump_risk_score = 0
except:
    pass

# --- 4. 100 BALŲ „GOLD SCORE“ ALGORITMAS ---
gold_score = 0
breakdown = []

# A. 4h Globalus Trendas (Max 20 balų)
is_4h_bullish = float(g4['Close']) > float(g4['EMA_200']) and float(g4['EMA_9']) > float(g4['EMA_21'])
if is_4h_bullish:
    gold_score += 20
    breakdown.append("✅ Globalus 4h Trendas yra Augantis (+20)")
else:
    breakdown.append("❌ Globalus 4h Trendas yra Krentantis (0)")

# B. 5m Institucinis lygis (Max 10 balų)
if current_price > vwap_val:
    gold_score += 10
    breakdown.append("✅ Kaina yra virš dienos VWAP (+10)")
else:
    breakdown.append("❌ Kaina yra žemiau dienos VWAP (0)")

# C. Trendo Jėga / Greitis (Max 10 balų)
if adx_val > 25:
    gold_score += 10
    breakdown.append(f"✅ ADX patvirtina stiprų rinkos judėjimą (+10)")
else:
    breakdown.append(f"❌ ADX rodo silpną/šoninį judėjimą (0)")

# D. 5m Momentum sankirta (Max 10 balų)
if float(g5['EMA_9']) > float(g5['EMA_21']):
    gold_score += 10
    breakdown.append("✅ Trumpieji vidurkiai EMA 9/21 susikirtę į viršų (+10)")
else:
    breakdown.append("❌ Trumpieji vidurkiai EMA 9/21 susikirtę žemyn (0)")

# E. JAV Dolerio (DXY) filtras (Max 20 balų)
dxy_trend = "Stiprėja 💵" if float(d5['EMA_9']) > float(d5['EMA_21']) else "Silpnėja 📉"
if "Silpnėja" in dxy_trend:
    gold_score += 20
    breakdown.append("✅ JAV Doleris (DXY) silpnėja – palanku auksui (+20)")
else:
    breakdown.append("❌ JAV Doleris (DXY) stiprėja – spaudžia auksą (0)")

# F. --- DINAMINIS RSI VERTINIMAS (Max 10 balų) --- [NAUJA]
if 40 <= rsi_val <= 60:
    gold_score += 10
    breakdown.append(f"🔥 Ideali RSI zona ({rsi_val:.1f}). Rinka sveika, turi daug vietos judesiui (+10)")
elif 60 < rsi_val <= 68 or 32 <= rsi_val < 40:
    gold_score += 5
    breakdown.append(f"⚠️ Pavėluota RSI zona ({rsi_val:.1f}). Judesys jau įsibėgėjęs, rizika didesnė (+5)")
else:
    breakdown.append(f"🚨 Ekstremali RSI zona ({rsi_val:.1f}). Rinka perpirkta arba perparduota (0)")

# G. Fundamentali aplinka (Max 20 balų)
gold_score += fed_risk_score
gold_score += trump_risk_score
if fed_risk_score == 10: breakdown.append("✅ FED aplinka stabili, jokių netikėtų pranešimų (+10)")
else: breakdown.append("⚠️⚠️ AUKŠTA FED RIZIKA: Užfiksuoti agresyvūs pranešimai (0)")
if trump_risk_score == 10: breakdown.append("✅ Trumpo aplinka rami, naujų tarifų grėsmių nėra (+10)")
else: breakdown.append("⚠️⚠️ GEOPOLITINĖ RIZIKA: Užfiksuoti Trumpo pareiškimai apie tarifus (0)")

# --- 5. REKOMENDACIJA PAGAL BALUS ---
signal_type = "NEUTRALUS (Laukite)"
confidence_level = "❌ NO TRADE ZONE"
ai_summary = "Sąlygos nepakankamos sandoriui. Rodikliai prieštarauja vieni kitiems, rinka neturi vieningos krypties."
stop_loss, take_profit, position_size_lots = 0.0, 0.0, 0.0

if gold_score >= 80:
    signal_type = "BUY"
    confidence_level = "🔥 STRONG BUY CONFIDENCE"
    stop_loss = current_price - (1.5 * atr_val)
    take_profit = current_price + (3.0 * atr_val)
    ai_summary = f"Maksimalus pirkimo signalas ({gold_score}/100). Techniniai rodikliai, įskaitant puikią RSI zoną, idealiai sutampa su silpstančiu doleriu ir ramia makroekonomine aplinka."
elif gold_score >= 50:
    signal_type = "BUY (SPECULATIVE)"
    confidence_level = "⚖️ MEDIUM CONFIDENCE"
    ai_summary = f"Vidutinis pirkimo signalas ({gold_score}/100). Trendas yra teigiamas, tačiau rinka jau yra stipriai pažengusi (RSI rodo mažesnį likusį potencialą) arba priešinasi DXY doleris."

if gold_score <= 30:
    signal_type = "SELL"
    confidence_level = "💥 STRONG SELL CONFIDENCE"
    stop_loss = current_price + (1.5 * atr_val)
    take_profit = current_price - (3.0 * atr_val)
    ai_summary = f"Maksimalus pardavimo signalas. „Gold Score“ yra itin žemas ({gold_score}/100), stambūs žaidėjai atsikrato auksu, o doleris perima rinkos kontrolę."

if stop_loss > 0:
    loss_dist = abs(current_price - stop_loss)
    position_size_lots = (account_size * (risk_percent / 100)) / (loss_dist * 100)

# --- 6. DASHBOARD ATVAIZDAVIMAS ---
st.subheader("🤖 AI Rinkos Nuosprendis & Rezultatų Suvestinė")
st.info(f"**AI Analizė:** {ai_summary}")

col_s1, col_s2, col_s3 = st.columns(3)
with col_s1:
    st.metric("GOLD SCORE (0-100)", f"{gold_score} / 100", confidence_level)
    st.progress(gold_score / 100)
with col_s2:
    st.metric("Dabartinė Kaina", f"${current_price:,.2f}")
    st.markdown(f"**Rekomendacija:** `{signal_type}`")
with col_s3:
    st.metric("ADX (Momento Jėga)", f"{adx_val:.2f}")
    st.markdown(f"**DXY Doleris:** {dxy_trend}")

st.markdown("---")

with st.expander("🔍 Žiūrėti detalų 100 balų skaičiavimo išrašą"):
    for line in breakdown:
        st.write(line)

st.markdown("---")

if stop_loss > 0:
    st.subheader("🎯 Tikslūs Skalpingto (5m) Rėžiai")
    col_t1, col_t2, col_t3, col_t4 = st.columns(4)
    col_t1.metric("Įėjimas", f"${current_price:,.2f}")
    col_t2.metric("🛑 STOP LOSS", f"${stop_loss:,.2f}")
    col_t3.metric("🎯 TAKE PROFIT", f"${take_profit:,.2f}")
    col_t4.metric("📊 Pozicijos Dydis", f"{position_size_lots:.2f} Lot")
    st.markdown("---")

# --- GRAFIKAI ---
fig = make_subplots(rows=2, cols=1, shared_xaxes=False, vertical_spacing=0.15, subplot_titles=("Auksas 5 min grafike", "Auksas 4 valandų grafike"))
fig.add_trace(go.Scatter(x=gold_df.index[-100:], y=gold_df['Close'][-100:], name="Auksas 5m", line=dict(color='#f39c12', width=2)), row=1, col=1)
fig.add_trace(go.Scatter(x=gold_df.index[-100:], y=gold_df['VWAP'][-100:], name="5m VWAP", line=dict(color='#9b59b6', width=1, dash='dash')), row=1, col=1)
fig.add_trace(go.Scatter(x=g_4h.index[-50:], y=g_4h['Close'][-50:], name="Auksas 4h", line=dict(color='#3498db', width=2)), row=2, col=1)
fig.add_trace(go.Scatter(x=g_4h.index[-50:], y=g_4h['EMA_200'][-50:], name="4h EMA 200", line=dict(color='#2ecc71', width=1.5)), row=2, col=1)
fig.update_layout(height=600, template="plotly_dark", margin=dict(l=20, r=20, t=30, b=10))
st.plotly_chart(fig, use_container_width=True)

# --- TELEGRAM AUTOMATINIS SIUNTĖJAS ---
if 'last_signal' not in st.session_state:
    st.session_state.last_signal = "NEUTRALUS"

tg_message = f"🚨 *GOLD 100-SCORE SIGNALAS* 🚨\nNuosprendis: *{signal_type}*\nBalas: *{gold_score}/100* ({confidence_level})\n\n📈 Įėjimas: ${current_price:,.2f}\n🛑 SL: ${stop_loss:,.2f}\n🎯 TP: ${take_profit:,.2f}\n📊 Dydis: {position_size_lots:.2f} Lot\n\n💡 _AI Suvestinė: {ai_summary}_"

if signal_type != "NEUTRALUS (Laukite)" and signal_type != st.session_state.last_signal:
    send_telegram_message(tg_message)
    st.session_state.last_signal = signal_type
from telegram_bot import send_telegram_message

if st.button("📲 Telegram TEST"):
    result = send_telegram_message(
        "🚀 Gold Terminal PRO Telegram veikia!"
    )
    st.write(result)
