import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import time

st.set_page_config(page_title="M82 Sovereign Core v6.8", page_icon="🦅", layout="wide")

st.title("🦅 MOLINA HOLDINGS & GLOBAL LLC")
st.subheader("M82 COMET - Global Futures & Extended Terminal v6.8 PRO")
st.markdown("---")

# 📥 PORTAFOLIO REAL DE ACCIONES
MI_PORTAFOLIO = {
    "NVDA": 50, "TSLA": 20, "OXY": 100, "JPM": 15, "MSFT": 10, "AAPL": 10, "AMZN": 15
}

# 🗺️ NUEVA MATRIZ GLOBAL EXTENDIDA (MERCADOS INTERNACIONALES INCLUIDOS)
ESTRUCTURA_MERCADO = {
    "🇺🇸 US FUTURES & VOLATILITY": ["NQ=F", "ES=F", "YM=F", "^VIX"],
    "🌏 GLOBAL & ASIAN FUTURES": ["^N225", "^HSI", "^TWII"],
    "🚀 EQUITIES & BIG TECH": ["NVDA", "MSFT", "TSLA", "AAPL", "AMZN", "GOOGL"],
    "🧱 COMMODITIES CRÍTICOS": ["CL=F", "GC=F", "NG=F", "SI=F"]
}

NOMBRES_ACTIVOS = {
    "NQ=F": "Futuros Nasdaq 100", "ES=F": "Futuros S&P 500", "YM=F": "Futuros Dow Jones",
    "^VIX": "Índice de Volatilidad", "^N225": "Nikkei 225 (Japón)", "^HSI": "Hang Seng (Hong Kong)",
    "^TWII": "Taiwan Weighted", "CL=F": "Petróleo Crudo", "GC=F": "Oro Spot",
    "NG=F": "Gas Natural", "SI=F": "Plata Spot"
}

@st.cache_data(ttl=15)
def obtener_datos_globales():
    búfer = {}
    todos_los_tickers = set([t for lista in ESTRUCTURA_MERCADO.values() for t in lista])
    for ticker in todos_los_tickers:
        try:
            t_obj = yf.Ticker(ticker)
            # Solicitamos datos incluyendo el flag de prepost para horas oscuras
            hist = t_obj.history(period="2d", interval="15m", prepost=True)
            
            if not hist.empty and len(hist) >= 2:
                price = float(hist['Close'].iloc[-1])
                prev_close = float(hist['Close'].iloc[-2])
                change = ((price - prev_close) / prev_close) * 100
                price_trend = hist['Close']
                
                # Extracción de precios específicos de horas extendidas
                info = t_obj.info
                estado_sesion = ""
                if "postMarketPrice" in info and info["postMarketPrice"] is not None and info["postMarketPrice"] > 0:
                    price = float(info["postMarketPrice"])
                    estado_sesion = " 🌙 [POST]"
                elif "preMarketPrice" in info and info["preMarketPrice"] is not None and info["preMarketPrice"] > 0:
                    price = float(info["preMarketPrice"])
                    estado_sesion = " 🌅 [PRE]"
            else: 
                price, change, price_trend, estado_sesion = 0.0, 0.0, pd.Series(), ""
                
            búfer[ticker] = {"price": price, "change": change, "trend": price_trend, "sesion": estado_sesion}
            time.sleep(0.01)
        except Exception: 
            búfer[ticker] = {"price": 0.0, "change": 0.0, "trend": pd.Series(), "sesion": ""}
    return búfer

datos_vivos = obtener_datos_globales()

# --- BALANCE NETO DEL PORTAFOLIO ---
valor_total_portafolio = 0.0
cambio_diario_estimado = 0.0
for ticker, cantidad in MI_PORTAFOLIO.items():
    info_ticker = datos_vivos.get(ticker, {"price": 0.0, "change": 0.0})
    p = info_ticker["price"]
    c = info_ticker["change"]
    if p > 0:
        valor_posicion = p * cantidad
        valor_total_portafolio += valor_posicion
        cambio_diario_estimado += (valor_posicion * (c / 100))

# --- DESPLIEGUE SUPERIOR MATRICIAL ---
st.markdown("### 🏦 VALORACIÓN DE ACTIVOS EN HORARIO EXTENDIDO")
p_col1, p_col2 = st.columns(2)
with p_col1:
    st.metric(label="💰 VALOR NETO EQUITIES EN VIVO", value=f"${valor_total_portafolio:,.2f} USD")
with p_col2:
    st.metric(label="📈 P&L EXTENDED ESTIMADO DEL DÍA", value=f"${cambio_diario_estimado:+,.2f} USD")
st.markdown("---")

# --- GRID RESPONSIVO VERTICAL PARA SMARTPHONES ---
for sector, tickers in ESTRUCTURA_MERCADO.items():
    st.header(sector)
    columnas_por_fila = 2
    for chunk_idx in range(0, len(tickers), columnas_por_fila):
        chunk_tickers = tickers[chunk_idx:chunk_idx + columnas_por_fila]
        cols = st.columns(len(chunk_tickers))
        for i, ticker in enumerate(chunk_tickers):
            info_ticker = datos_vivos.get(ticker, {"price": 0.0, "change": 0.0, "trend": pd.Series(), "sesion": ""})
            price, change, trend, sesion = info_ticker["price"], info_ticker["change"], info_ticker["trend"], info_ticker["sesion"]
            
            nombre_legible = NOMBRES_ACTIVOS.get(ticker, ticker)
            label_visual = f"{ticker}{sesion}"
            
            # Formateo dinámico para el VIX o porcentajes de índices
            val_str = f"{price:.2f}" if ticker == "^VIX" else f"${price:,.2f}"
            
            with cols[i]:
                if price > 0:
                    st.metric(label=label_visual, value=val_str, delta=f"{change:.2f}%")
                    st.caption(f"**{nombre_legible}**")
                    if not trend.empty: st.line_chart(trend, height=75, use_container_width=True)
                else: 
                    st.metric(label=ticker, value="Esperando Apertura...")
    st.markdown("---")

st.caption("M82 Sovereign Core Terminal v6.8 PRO • Global Futures Matrix Enabled.")
