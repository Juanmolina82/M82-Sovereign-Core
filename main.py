import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import time

st.set_page_config(page_title="M82 Sovereign Core v6.1", page_icon="🦅", layout="wide")

st.title("🦅 MOLINA HOLDINGS & GLOBAL LLC")
st.subheader("M82 COMET - Multi-Asset Derivative Terminal v6.1")
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
# 👁️ RADAR MULTI-DIRECCIONAL DE DERIVADOS EN VIVO
# ==============================================================================
st.markdown("### 👁️ AUDITORÍA DE FLUJOS INSTITUCIONALES (BLOCK TRADES)")
tipo_flujo = st.radio("Selecciona tipo de flujo detectado:", ["Bullish Long Call (Caso MSFT)", "Bullish Short Put (Caso NVDA)"])

if tipo_flujo == "Bullish Long Call (Caso MSFT)":
    with st.expander("🚀 Parámetros del Bloque de Compra - Microsoft", expanded=True):
        c_col1, c_col2, c_col3 = st.columns(3)
        with c_col1:
            strike_c = st.number_input("Strike Call Seleccionado (K):", value=420.00)
        with c_col2:
            prima_c = st.number_input("Prima Pagada ($ por contrato):", value=10.00)
        with c_col3:
            contratos_c = st.number_input("Contratos del Bloque:", value=416100)

        be_c = strike_c + prima_c
        inversion_total = prima_c * 100 * contratos_c
        msft_spot = datos_vivos.get("MSFT", {"price": 422.00})["price"]
        distancia_be = ((be_c - msft_spot) / msft_spot) * 100 if msft_spot > 0 else 0.0

        st.markdown("#### 📊 Umbrales de Reversión Máxima:")
        mc_col1, mc_col2, mc_col3 = st.columns(3)
        with mc_col1:
            st.metric(label="🔥 Riesgo Fijo (Capital Invertido)", value=f"${inversion_total:,.2f} USD")
        with mc_col2:
            st.metric(label="🎯 Numerante Target (Break-Even)", value=f"${be_c:,.2f} USD")
        with mc_col3:
            st.metric(label="📈 Distancia Requerida para Profit", value=f"{distancia_be:+.2f}%")

        if msft_spot >= be_c:
            st.success(f"🟢 EN EL DINERO (ITM): MSFT (${msft_spot:.2f}) ya superó el Break-Even. El bloque está acumulando valor intrínseco.")
        else:
            st.warning(f"🟡 ESCENARIO DE RECUPERACIÓN: MSFT está a {distancia_be:.2f}% de activar las ganancias del bloque institucional.")

else:
    with st.expander("🛡️ Parámetros del Bloque de Venta - NVIDIA", expanded=True):
        col_op1, col_op2, col_op3 = st.columns(3)
        with col_op1: strike = st.number_input("Strike de la Opción (K):", value=100.00)
        with col_op2: prima = st.number_input("Prima Recibida ($):", value=41.00)
        with col_op3: contratos = st.number_input("Contratos:", value=340)

        breakeven = strike - prima
        max_profit = prima * 100 * contratos
        nvda_spot = datos_vivos.get("NVDA", {"price": 222.96})["price"]
        distancia_seguridad = ((nvda_spot - breakeven) / nvda_spot) * 100 if nvda_spot > 0 else 0.0

        st.markdown("#### 📊 Métricas de Exposición:")
        m_col1, m_col2, m_col3 = st.columns(3)
        with m_col1: st.metric(label="💰 Beneficio Máximo", value=f"${max_profit:,.2f} USD")
        with m_col2: st.metric(label="🎯 Break-Even", value=f"${breakeven:,.2f} USD")
        with m_col3: st.metric(label="🛡️ Margen de Seguridad", value=f"{distancia_seguridad:.1f}%")

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

st.caption("M82 Sovereign Core Terminal v6.1 PRO • Advanced Derivatives Architecture.")
