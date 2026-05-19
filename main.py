import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import time

st.set_page_config(page_title="M82 Sovereign Core v5.8", page_icon="🦅", layout="wide")

st.title("🦅 MOLINA HOLDINGS & GLOBAL LLC")
st.subheader("M82 COMET - Options Risk & Catalyst Terminal v5.8")
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
# 🔥 NUEVO RADAR DE SIMULACIÓN DE DERIVADOS INSTITUCIONALES (BLOCK TRADES)
# ==============================================================================
st.markdown("### 👁️ RADAR DE RIESGO EN DERIVADOS (INSTITUTIONAL SHORT PUT)")
with st.expander("🛡️ Auditoría de Posiciones de Opciones de Alta Prima (Caso NVDA $1.4M)", expanded=True):
    col_op1, col_op2, col_op3 = st.columns(3)
    with col_op1:
        strike = st.number_input("Strike de la Opción (K):", value=100.00)
    with col_op2:
        prima = st.number_input("Prima Recibida ($ por contrato):", value=41.00)
    with col_op3:
        contratos = st.number_input("Cantidad de Contratos Vendidos:", value=340)

    # Computación de fórmulas matriciales
    breakeven = strike - prima
    max_profit = prima * 100 * contratos
    max_risk = breakeven * 100 * contratos
    nvda_spot = datos_vivos.get("NVDA", {"price": 222.96})["price"]
    distancia_seguridad = ((nvda_spot - breakeven) / nvda_spot) * 100 if nvda_spot > 0 else 0.0

    st.markdown("#### 📊 Métricas de Exposición al Cierre:")
    m_col1, m_col2, m_col3 = st.columns(3)
    with m_col1:
        st.metric(label="💰 Beneficio Máximo (Crédito Neto)", value=f"${max_profit:,.2f} USD")
    with m_col2:
        st.metric(label="🎯 Punto de Equilibrio (Break-Even)", value=f"${breakeven:,.2f} USD")
    with m_col3:
        st.metric(label="🛡️ Margen de Seguridad vs Spot", value=f"{distancia_seguridad:.1f}%")

    if nvda_spot < breakeven:
        st.error(f"🚨 ALERTA CRÍTICA: El precio Spot (${nvda_spot:.2f}) ha perforado el Break-Even. Pérdida potencial en curso.")
    else:
        st.success(f"🟢 ZONA DE SEGURIDAD: El operador retiene el crédito. Nvidia está un {distancia_seguridad:.1f}% por encima del punto de dolor.")

st.markdown("---")

# --- GRID RESPONSIVO 2x2 DE MONITOREO GENERAL ---
for sector, tickers in ESTRUCTURA_MERCADO.items():
    st.header(sector)
    columnas_por_fila = 2
    for chunk_idx in range(0, len(tickers), columnas_por_fila):
        chunk_tickers = tickers[chunk_idx:chunk_idx + columnas_por_fila]
        cols = st.columns(len(chunk_tickers))
        for i, ticker in enumerate(chunk_tickers):
            info_ticker = datos_vivos.get(ticker, {"price": 0.0, "change": 0.0, "trend": pd.Series()})
            price, change, trend = info_ticker["price"], info_ticker["change"], info_ticker["trend"]
            nombre_legible = NOMBRES_ACTIVOS.get(ticker, ticker)
            with cols[i]:
                if price > 0:
                    st.metric(label=ticker, value=f"${price:.2f}", delta=f"{change:.2f}%")
                    if not trend.empty: st.line_chart(trend, height=70, use_container_width=True)
                else: st.metric(label=ticker, value="Sincronizando...")
    st.markdown("---")

st.caption("M82 Sovereign Core Terminal v5.8 PRO • Options Analytics Engine Enabled.")
