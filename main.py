import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import time

st.set_page_config(page_title="M82 Sovereign Core v7.0", page_icon="🦅", layout="wide")

st.title("🦅 MOLINA HOLDINGS & GLOBAL LLC")
st.subheader("M82 COMET - Total Market Mapping Terminal v7.0 PRO")
st.markdown("---")

# 📥 PORTAFOLIO DE CONTROL REAL
MI_PORTAFOLIO = {
    "NVDA": 50, "TSLA": 20, "OXY": 100, "JPM": 15, "MSFT": 10, "AAPL": 10, "AMZN": 15
}

# 🗺️ MATRIZ DE EXPOSICIÓN TOTAL (INCORPORANDO TUS CAPTURAS EXTRAS)
ESTRUCTURA_MERCADO = {
    "🇺🇸 MAJOR US FUTURES": ["NQ=F", "ES=F", "YM=F", "MME=F"],
    "📉 MICRO / SMALL CAP FUTURES": ["RTY=F", "MYM=F", "MNQ=F", "MES=F"],
    "⚠️ VOLATILITY DERIVATIVES": ["^VIX", "VXM=F"],
    "🌏 PACIFIC & ASIAN INDEXES": ["^N225", "^HSI", "STW=F"]
}

NOMBRES_ACTIVOS = {
    "NQ=F": "Futuros Nasdaq 100", "ES=F": "Futuros S&P 500", "YM=F": "Futuros Dow Jones",
    "MME=F": "S&P MidCap 400 Futures", "RTY=F": "Russell 2000 Futures", "MYM=F": "Micro Dow Jones Futures",
    "MNQ=F": "Micro Nasdaq 100 Futures", "MES=F": "Micro S&P 500 Futures", "^VIX": "VIX Index",
    "VXM=F": "Mini VIX Futures", "^N225": "Nikkei 225 Index", "^HSI": "Hang Seng Index",
    "STW=F": "MSCI Taiwan Futures"
}

@st.cache_data(ttl=15)
def obtener_datos_globales():
    búfer = {}
    todos_los_tickers = set([t for lista in ESTRUCTURA_MERCADO.values() for t in lista])
    for ticker in todos_los_tickers:
        try:
            t_obj = yf.Ticker(ticker)
            hist = t_obj.history(period="2d", interval="15m", prepost=True)
            
            if not hist.empty and len(hist) >= 2:
                price = float(hist['Close'].iloc[-1])
                prev_close = float(hist['Close'].iloc[-2])
                change = ((price - prev_close) / prev_close) * 100
                price_trend = hist['Close']
                
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

# --- PANEL DE CONTROL DE SELECCIÓN DE ACTIVOS ---
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
            
            # Formateo visual adaptado a índices o volatilidad
            val_str = f"{price:.2f}" if "VIX" in nombre_legible else f"{price:,.2f}"
            
            with cols[i]:
                if price > 0:
                    st.metric(label=label_visual, value=val_str, delta=f"{change:.2f}%")
                    st.caption(f"**{nombre_legible}**")
                    if not trend.empty: st.line_chart(trend, height=75, use_container_width=True)
                else: 
                    st.metric(label=ticker, value="Sincronizando...")
    st.markdown("---")

st.caption("M82 Sovereign Core Terminal v7.0 PRO • Comprehensive Micro/Macro Derivative Grid.")
