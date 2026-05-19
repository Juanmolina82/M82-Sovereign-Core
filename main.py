import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import time

st.set_page_config(page_title="M82 Sovereign Core v6.2", page_icon="🦅", layout="wide")

st.title("🦅 MOLINA HOLDINGS & GLOBAL LLC")
st.subheader("M82 COMET - Premium Derivative Terminal v6.2")
st.markdown("---")

# 📥 PORTAFOLIO REAL
MI_PORTAFOLIO = {
    "NVDA": 50, "TSLA": 20, "OXY": 100, "JPM": 15, "MSFT": 10, "AAPL": 10, "AMZN": 15
}

ESTRUCTURA_MERCADO = {
    "🚀 EQUITIES & BIG TECH": ["NVDA", "TSLA", "MSFT", "AAPL", "AMZN", "GOOGL"],
    "📦 ETFs & FUTURES": ["SPY", "QQQ", "IWM", "NQ=F"],
    "🧱 COMMODITIES CRÍTICOS": ["CL=F", "GC=F", "NG=F", "SI=F"]
}

NOMBRES_ACTIVOS = {
    "CL=F": "Petróleo Crudo", "GC=F": "Oro Spot", "SPY": "S&P 500 ETF", 
    "QQQ": "Nasdaq-100 ETF", "IWM": "Russell 2000 ETF", "NQ=F": "Futuros Nasdaq-100"
}

@st.cache_data(ttl=15)
def obtener_datos_globales():
    búfer = {}
    todos_los_tickers = set([t for lista in ESTRUCTURA_MERCADO.values() for t in lista])
    for ticker in todos_los_tickers:
        try:
            t_obj = yf.Ticker(ticker)
            hist = t_obj.history(period="2d", interval="15m")
            if not hist.empty and len(hist) >= 2:
                price = float(hist['Close'].iloc[-1])
                prev_close = float(hist['Close'].iloc[-2])
                change = ((price - prev_close) / prev_close) * 100
                price_trend = hist['Close']
            else: price, change, price_trend = 0.0, 0.0, pd.Series()
            búfer[ticker] = {"price": price, "change": change, "trend": price_trend}
        except Exception: búfer[ticker] = {"price": 0.0, "change": 0.0, "trend": pd.Series()}
    return búfer

datos_vivos = obtener_datos_globales()

# ==============================================================================
# 👁️ RADAR DE DERIVADOS - TARGET PREMIUM v6.2
# ==============================================================================
st.markdown("### 👁️ AUDITORÍA DE FLUJOS DE ALTA GAMA (BLOCK TRADES)")
tipo_flujo = st.radio("Selecciona tipo de flujo detectado:", ["MSFT August 21 Block ($5.37M)", "Bullish Short Put (Caso NVDA)"])

if tipo_flujo == "MSFT August 21 Block ($5.37M)":
    with st.expander("🚀 Parámetros del Bloque de Compra Premium - Microsoft", expanded=True):
        c_col1, c_col2, c_col3 = st.columns(3)
        with c_col1:
            strike_c = st.number_input("Strike Call de Ejercicio (K):", value=420.00)
        with c_col2:
            prima_c = st.number_input("Prima Premium Pagada ($):", value=90.00)
        with c_col3:
            contratos_c = st.number_input("Contratos Totales Calculados:", value=596)

        be_c = strike_c + prima_c
        inversion_total = prima_c * 100 * contratos_c
        msft_spot = datos_vivos.get("MSFT", {"price": 422.00})["price"]
        distancia_be = ((be_c - msft_spot) / msft_spot) * 100 if msft_spot > 0 else 0.0

        st.markdown("#### 📊 Umbrales de Exposición Especulativa:")
        mc_col1, mc_col2, mc_col3 = st.columns(3)
        with mc_col1:
            st.metric(label="🔥 Capital de Riesgo Fijo", value=f"${inversion_total:,.2f} USD")
        with mc_col2:
            st.metric(label="🎯 Break-Even Target Necesario", value=f"${be_c:.2f} USD")
        with mc_col3:
            st.metric(label="📈 Distancia Requerida vs Spot", value=f"{distancia_be:+.2f}%")

        if msft_spot >= be_c:
            st.success(f"🟢 IN THE MONEY: MSFT (${msft_spot:.2f}) ha roto la barrera cuántica del Break-Even.")
        else:
            st.warning(f"⚠️ CAPITULACIÓN INTRADÍA: MSFT cotiza por debajo del objetivo. Se requiere un rally del {distancia_be:.2f}% para activar este bloque.")

else:
    with st.expander("🛡️ Parámetros del Bloque de Venta - NVIDIA", expanded=True):
        col_op1, col_op2 = st.columns(2)
        with col_op1: strike = st.number_input("Strike (K):", value=100.00)
        with col_op2: prima = st.number_input("Prima Recibida ($):", value=41.00)
        
        breakeven = strike - prima
        nvda_spot = datos_vivos.get("NVDA", {"price": 222.96})["price"]
        st.metric(label="🎯 Break-Even", value=f"${breakeven:,.2f} USD")

st.markdown("---")

# --- GRID RESPONSIVO DE PRECIOS VIVOS ---
for sector, tickers in ESTRUCTURA_MERCADO.items():
    st.header(sector)
    columnas_por_fila = 2
    for chunk_idx in range(0, len(tickers), columnas_por_fila):
        chunk_tickers = tickers[chunk_idx:chunk_idx + columnas_por_fila]
        cols = st.columns(len(chunk_tickers))
        for i, ticker in enumerate(chunk_tickers):
            info_ticker = datos_vivos.get(ticker, {"price": 0.0, "change": 0.0, "trend": pd.Series()})
            price, change, trend = info_ticker["price"], info_ticker["change"], info_ticker["trend"]
            with cols[i]:
                if price > 0:
                    st.metric(label=ticker, value=f"${price:.2f}", delta=f"{change:.2f}%")
                    if not trend.empty: st.line_chart(trend, height=70, use_container_width=True)
                else: st.metric(label=ticker, value="Sincronizando...")
    st.markdown("---")

st.caption("M82 Sovereign Core Terminal v6.2 PRO • Premium Options Cluster.")
