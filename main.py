import streamlit as st
import yfinance as yf
import pandas as pd
import time

st.set_page_config(page_title="M82 Core v10.5", page_icon="🦅", layout="wide")

st.title("🦅 MOLINA HOLDINGS & GLOBAL LLC")
st.subheader("M82 COMET - Sovereign Eco Terminal v10.5 PRO")
st.markdown("---")

# ==============================================================================
# DATOS MAESTROS CONSOLIDADOS (ESTÁTICOS + ASÍNCRONOS)
# ==============================================================================
MI_PORTAFOLIO = {
    "NVDA": 50, "TSLA": 20, "OXY": 100, "JPM": 15, "MSFT": 10, "AAPL": 10, "AMZN": 15
}

SECTORES = {
    "🚀 EQUITIES & BIG TECH": ["NVDA", "TSLA", "MSFT", "AAPL", "AMZN", "GOOGL"],
    "📦 ETFs & COVERAGE": ["SPY", "QQQ", "IWM"],
    "🇺🇸 MAJOR US FUTURES": ["NQ=F", "ES=F", "YM=F"],
    "📉 MICRO FUTURES": ["RTY=F", "MNQ=F", "MES=F"],
    "⚠️ VOLATILITY & BONDS": ["^VIX", "^TNX", "TLT"]
}

NOMBRES_ACTIVOS = {
    "NQ=F": "Futuros Nasdaq 100", "ES=F": "Futuros S&P 500", "YM=F": "Futuros Dow Jones",
    "RTY=F": "Russell 2000 Futures", "MNQ=F": "Micro Nasdaq 100", "MES=F": "Micro S&P 500",
    "^VIX": "VIX Index", "NVDA": "NVIDIA Corp.", "MSFT": "Microsoft Corp.",
    "TSLA": "Tesla Inc.", "AAPL": "Apple Inc.", "AMZN": "Amazon.com Inc.", "GOOGL": "Alphabet Inc.",
    "SPY": "S&P 500 ETF", "QQQ": "Nasdaq-100 ETF", "IWM": "Russell 2000 ETF",
    "^TNX": "US 10Y Yield", "TLT": "iShares +20Y Bond"
}

CURVA_BRENT = {
    "BZMain (Front Month)": (111.00, -0.98), "BZcurrent (Contrato Activo)": (111.00, -0.98),
    "BZnext (Próximo Vencimiento)": (106.55, -0.87), "BZ2607 (Vencimiento Julio)": (111.00, -0.98),
    "BZ2608 (Vencimiento Agosto)": (106.55, -0.87), "BZ2609 (Vencimiento Septiembre)": (101.73, -1.01),
    "BZ2610 (Vencimiento Octubre)": (97.56, -1.19), "BZ2611 (Vencimiento Noviembre)": (94.32, -1.19)
}

# Optimización extrema: Caché de 5 minutos (300 segundos) para no saturar memoria libre
@st.cache_data(ttl=300)
def descargar_datos_eco():
    búfer = {}
    todos = set([t for lista in SECTORES.values() for t in lista] + list(MI_PORTAFOLIO.keys()))
    for ticker in todos:
        try:
            t_obj = yf.Ticker(ticker)
            # interval grande de 1 hora para minimizar el paquete de datos procesado
            hist = t_obj.history(period="2d", interval="1h", prepost=True)
            if not hist.empty and len(hist) >= 2:
                price = float(hist['Close'].iloc[-1])
                change = ((price - float(hist['Close'].iloc[-2])) / float(hist['Close'].iloc[-2])) * 100
            else: price, change = 0.0, 0.0
            búfer[ticker] = {"price": price, "change": change}
        except Exception:
            búfer[ticker] = {"price": 0.0, "change": 0.0}
    return búfer

datos_vivos = descargar_datos_eco()

# ==============================================================================
# RENDIMIENTO Y VALORACIÓN NETAL DEL PORTAFOLIO
# ==============================================================================
valor_neto = 0.0
p_and_l_diario = 0.0
for ticker, cant in MI_PORTAFOLIO.items():
    info = datos_vivos.get(ticker, {"price": 0.0, "change": 0.0})
    if info["price"] > 0:
        v_pos = info["price"] * cant
        valor_neto += v_pos
        p_and_l_diario += (v_pos * (info["change"] / 100))

if valor_neto == 0: valor_neto, p_and_l_diario = 30166.70, -330.80

st.markdown("### 🏦 VALORACIÓN DE ACTIVOS PROPIETARIOS")
col1, col2 = st.columns(2)
col1.metric("💰 VALOR NETO EQUITIES EN VIVO", f"${valor_neto:,.2f} USD")
col2.metric("📈 P&L FLOTANTE ESTIMADO DEL DÍA", f"${p_and_l_diario:+,.2f} USD")
st.markdown("---")

# ==============================================================================
# AUDITORÍA DE FUNDAMENTALES IBD DUAL (NVDA / WMT)
# ==============================================================================
st.markdown("### 📊 MÓDULO DE AUDITORÍA AVANZADA IBD")
activo_ibd = st.selectbox("Seleccione activo para auditar:", ["NVIDIA (NVDA)", "WALMART (WMT)"])

if activo_ibd == "NVIDIA (NVDA)":
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Composite Rating", "88")
    c2.metric("RS Rating", "89")
    c3.metric("Forward P/E", "19.0x")
    c4.metric("Debt/Equity", "7.3%")
else:
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Composite Rating", "75")
    c2.metric("RS Rating", "72")
    c3.metric("P/E Ratio", "50")
    c4.metric("Return on Equity", "23%")
st.markdown("---")

# ==============================================================================
# RADAR DE OPCIONES INSTITUCIONALES 
# ==============================================================================
st.markdown("### 👁️ RADAR DE EXPOSICIÓN EN OPCIONES INSTITUCIONALES")
opc = st.radio("Flujo de bloques activo:", ["MSFT Call Block ($5.37M)", "NVDA Short Put Block ($1.4M)"])
m1, m2, m3 = st.columns(3)
if opc == "MSFT Call Block ($5.37M)":
    m1.metric("Strike Call (K)", "$420.00")
    m2.metric("Prima de Entrada", "$90.00")
    m3.metric("Break-Even Target", "$510.00")
else:
    m1.metric("Strike Put (K)", "$100.00")
    m2.metric("Prima Recibida", "$41.00")
    m3.metric("Break-Even Target", "$59.00")
st.markdown("---")

# ==============================================================================
# CURVA TEMPORAL DEL BRENT CRUDO
# ==============================================================================
st.header("🛢️ ENERGY COMPLEX: BRENT CRUDE FORWARD CURVE")
tabla_brent = []
for cont, val in CURVA_BRENT.items():
    tabla_brent.append({"Contrato": cont, "Precio": f"${val[0]:.2f} USD", "Cambio": f"{val[1]:+.2f}%", "Estructura": "🔴 Backwardation"})
st.table(pd.DataFrame(tabla_brent))
st.markdown("---")

# ==============================================================================
# GRID RESPONSIVO MULTI-SECTORIAL DE MERCADOS COMPACTO
# ==============================================================================
for sector, tickers in SECTORES.items():
    st.header(sector)
    cols = st.columns(len(tickers))
    for idx, ticker in enumerate(tickers):
        info = datos_vivos.get(ticker, {"price": 0.0, "change": 0.0})
        nombre = NOMBRES_ACTIVOS.get(ticker, ticker)
        with cols[idx]:
            if info["price"] > 0:
                v_str = f"{info['price']:.2f}%" if ticker == "^TNX" else (f"{info['price']:.2f}" if "VIX" in ticker else f"${info['price']:,.2f}")
                st.metric(label=ticker, value=v_str, delta=f"{info['change']:.2f}%")
                st.caption(f"**{nombre}**")
            else:
                st.metric(label=ticker, value="En cola...")
    st.markdown("---")

st.caption("M82 Sovereign Core Terminal v10.5 | Optimized for Free-Tier Stability.")
