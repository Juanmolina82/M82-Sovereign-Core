import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import time

st.set_page_config(page_title="M82 Sovereign Core v8.5", page_icon="🦅", layout="wide")

st.title("🦅 MOLINA HOLDINGS & GLOBAL LLC")
st.subheader("M82 COMET - Master Sovereign Terminal v8.5 PRO")
st.markdown("---")

# ==============================================================================
# 1. ARQUITECTURA DE DATOS Y MAPEO DE TICKERS M82
# ==============================================================================
MI_PORTAFOLIO = {
    "NVDA": 50, "TSLA": 20, "OXY": 100, "JPM": 15, "MSFT": 10, "AAPL": 10, "AMZN": 15
}

SECTORES = {
    "🚀 EQUITIES & BIG TECH": ["NVDA", "TSLA", "MSFT", "AAPL", "AMZN", "GOOGL"],
    "📦 ETFs & COVERAGE": ["SPY", "QQQ", "IWM"],
    "🇺🇸 MAJOR US FUTURES": ["NQ=F", "ES=F", "YM=F", "MME=F"],
    "📉 MICRO / SMALL CAP FUTURES": ["RTY=F", "MYM=F", "MNQ=F", "MES=F"],
    "⚠️ VOLATILITY DERIVATIVES": ["^VIX", "VXM=F"],
    "🌏 PACIFIC & ASIAN INDEXES": ["^N225", "^HSI", "STW=F"],
    "📈 BONDS & RATES": ["^TNX", "TLT"]
}

NOMBRES_ACTIVOS = {
    "NQ=F": "Futuros Nasdaq 100", "ES=F": "Futuros S&P 500", "YM=F": "Futuros Dow Jones",
    "MME=F": "S&P MidCap 400 Futures", "RTY=F": "Russell 2000 Futures", "MYM=F": "Micro Dow Jones Futures",
    "MNQ=F": "Micro Nasdaq 100 Futures", "MES=F": "Micro S&P 500 Futures", "^VIX": "VIX Index",
    "VXM=F": "Mini VIX Futures", "^N225": "Nikkei 225 Index", "^HSI": "Hang Seng Index",
    "STW=F": "MSCI Taiwan Futures", "NVDA": "NVIDIA Corp.", "MSFT": "Microsoft Corp.",
    "TSLA": "Tesla Inc.", "AAPL": "Apple Inc.", "AMZN": "Amazon.com Inc.", "GOOGL": "Alphabet Inc.",
    "SPY": "S&P 500 ETF", "QQQ": "Nasdaq-100 ETF", "IWM": "Russell 2000 ETF",
    "^TNX": "US 10Y Yield", "TLT": "iShares +20Y Bond"
}

CURVA_BRENT_TICKERS = {
    "BZMain (Front Month)": "BZ=F", "BZcurrent (Contrato Activo)": "BZ=F", 
    "BZnext (Próximo Vencimiento)": "BZQ26.NYM", "BZ2607 (Vencimiento Julio)": "BZN26.NYM",
    "BZ2608 (Vencimiento Agosto)": "BZQ26.NYM", "BZ2609 (Vencimiento Septiembre)": "BZU26.NYM",
    "BZ2610 (Vencimiento Octubre)": "VZV26.NYM", "BZ2611 (Vencimiento Noviembre)": "BZX26.NYM"
}

VALORES_REFERENCIA_BRENT = {
    "BZMain (Front Month)": (111.00, -0.98), "BZcurrent (Contrato Activo)": (111.00, -0.98),
    "BZnext (Próximo Vencimiento)": (106.55, -0.87), "BZ2607 (Vencimiento Julio)": (111.00, -0.98),
    "BZ2608 (Vencimiento Agosto)": (106.55, -0.87), "BZ2609 (Vencimiento Septiembre)": (101.73, -1.01),
    "BZ2610 (Vencimiento Octubre)": (97.56, -1.19), "BZ2611 (Vencimiento Noviembre)": (94.32, -1.19)
}

@st.cache_data(ttl=10)
def obtener_datos_maestros():
    búfer = {}
    todos_los_tickers = set([t for lista in SECTORES.values() for t in lista] + list(MI_PORTAFOLIO.keys()))
    for ticker in todos_los_tickers:
        try:
            t_obj = yf.Ticker(ticker)
            hist = t_obj.history(period="2d", interval="15m", prepost=True)
            if not hist.empty and len(hist) >= 2:
                price = float(hist['Close'].iloc[-1])
                prev_close = float(hist['Close'].iloc[-2])
                change = ((price - prev_close) / prev_close) * 100
                trend = hist['Close']
                
                info = t_obj.info
                sesion = ""
                if "postMarketPrice" in info and info["postMarketPrice"] is not None and info["postMarketPrice"] > 0:
                    price = float(info["postMarketPrice"])
                    sesion = " 🌙 [POST]"
                elif "preMarketPrice" in info and info["preMarketPrice"] is not None and info["preMarketPrice"] > 0:
                    price = float(info["preMarketPrice"])
                    sesion = " 🌅 [PRE]"
            else: price, change, trend, sesion = 0.0, 0.0, pd.Series(), ""
            búfer[ticker] = {"price": price, "change": change, "trend": trend, "sesion": sesion}
            time.sleep(0.01)
        except Exception:
            búfer[ticker] = {"price": 0.0, "change": 0.0, "trend": pd.Series(), "sesion": ""}
    return búfer

datos_vivos = obtener_datos_maestros()

# ==============================================================================
# 2. SECCIÓN SUPERIOR: VALORACIÓN DEL PORTAFOLIO EN VIVO
# ==============================================================================
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

st.markdown("### 🏦 VALORACIÓN DE ACTIVOS PROPIETARIOS")
p_col1, p_col2 = st.columns(2)
with p_col1: st.metric(label="💰 VALOR NETO EQUITIES EN VIVO", value=f"${valor_total_portafolio:,.2f} USD")
with p_col2: st.metric(label="📈 P&L FLOTANTE ESTIMADO DEL DÍA", value=f"${cambio_diario_estimado:+,.2f} USD")
st.markdown("---")

# ==============================================================================
# 3. MÓDULO INTEGRAL DE DERIVADOS (OPTIONS BLOCK RADAR)
# ==============================================================================
st.markdown("### 👁️ RADAR DE EXPOSICIÓN EN OPCIONES INSTITUCIONALES")
opcion_seleccionada = st.selectbox("Seleccione flujo de derivados a auditar:", ["MSFT August 21 Call Block ($5.37M)", "NVDA Short Put Block ($1.4M)"])

if opcion_seleccionada == "MSFT August 21 Call Block ($5.37M)":
    with st.expander("🚀 Estructura Alcista - Microsoft Call Block", expanded=True):
        c_col1, c_col2, c_col3 = st.columns(3)
        with c_col1: strike_c = st.number_input("Strike Call (K):", value=420.00)
        with c_col2: prima_c = st.number_input("Prima de Entrada ($):", value=90.00)
        with c_col3: contratos_c = st.number_input("Contratos:", value=596)
        be_c = strike_c + prima_c
        total_premium = prima_c * 100 * contratos_c
        msft_spot = datos_vivos.get("MSFT", {"price": 422.00})["price"]
        dist_be = ((be_c - msft_spot) / msft_spot) * 100 if msft_spot > 0 else 0.0
        
        m1, m2, m3 = st.columns(3)
        with m1: st.metric(label="🔥 Prima Neta Invertida", value=f"${total_premium:,.2f} USD")
        with m2: st.metric(label="🎯 Break-Even Target", value=f"${be_c:.2f} USD")
        with m3: st.metric(label="📈 Distancia Requerida", value=f"{dist_be:+.2f}%")
else:
    with st.expander("🛡️ Estructura de Crédito - NVIDIA Short Put Block", expanded=True):
        p_col1, p_col2, p_col3 = st.columns(3)
        with p_col1: strike_p = st.number_input("Strike Put (K):", value=100.00)
        with p_col2: prima_p = st.number_input("Prima Recibida ($):", value=41.00)
        with p_col3: contratos_p = st.number_input("Contratos Vendidos:", value=340)
        be_p = strike_p - prima_p
        max_credit = prima_p * 100 * contratos_p
        nvda_spot = datos_vivos.get("NVDA", {"price": 222.96})["price"]
        dist_seg = ((nvda_spot - be_p) / nvda_spot) * 100 if nvda_spot > 0 else 0.0
        
        n1, n2, n3 = st.columns(3)
        with n1: st.metric(label="💰 Crédito Máximo Capturado", value=f"${max_credit:,.2f} USD")
        with n2: st.metric(label="🎯 Umbral Inferior Break-Even", value=f"${be_p:.2f} USD")
        with n3: st.metric(label="🛡️ Colchón de Seguridad vs Spot", value=f"{dist_seg:.1f}%")
st.markdown("---")

# ==============================================================================
# 4. CURVA FORWARD DEL CRUDO BRENT (INTEGRACIÓN MOOMOO)
# ==============================================================================
st.header("🛢️ ENERGY COMPLEX: BRENT CRUDE FORWARD CURVE")
tabla_brent = []
for contrato, ticker in CURVA_BRENT_TICKERS.items():
    ref_price, ref_change = VALORES_REFERENCIA_BRENT[contrato]
    tabla_brent.append({
        "Contrato / Vencimiento": contrato, "Precio Último ($)": f"${ref_price:.2f} USD",
        "Variación (%)": f"{ref_change:+.2f}%", "Estructura Dinámica": "🔴 Backwardation Premium" if ref_price < 111.00 else "📋 Front Month Base"
    })
st.table(pd.DataFrame(tabla_brent))

# Gráfico de Estructura Temporal
precios_curva = [VALORES_REFERENCIA_BRENT[c][0] for c in CURVA_BRENT_TICKERS.keys()]
nombres_curva = [c.split(" ")[0] for c in CURVA_BRENT_TICKERS.keys()]
st.line_chart(pd.DataFrame({"Precio ($)": precios_curva}, index=nombres_curva), height=150)
st.markdown("---")

# ==============================================================================
# 5. MATRIZ MULTI-SECTORIAL DE MERCADOS (SISTEMA DE GRIDS)
# ==============================================================================
for sector, tickers in SECTORES.items():
    st.header(sector)
    columnas_por_fila = 2
    for chunk_idx in range(0, len(tickers), columnas_por_fila):
        chunk_tickers = tickers[chunk_idx:chunk_idx + columnas_por_fila]
        cols = st.columns(len(chunk_tickers))
        for i, ticker in enumerate(chunk_tickers):
            info = datos_vivos.get(ticker, {"price": 0.0, "change": 0.0, "trend": pd.Series(), "sesion": ""})
            price, change, trend, sesion = info["price"], info["change"], info["trend"], info["sesion"]
            nombre_legible = NOMBRES_ACTIVOS.get(ticker, ticker)
            
            # Formateo de etiquetas de visualización
            label_visual = f"{ticker}{sesion}"
            if "Yield" in nombre_legible or "Index" in nombre_legible or "VIX" in ticker:
                val_str = f"{price:.2f}%" if "^TNX" in ticker else f"{price:.2f}"
            else:
                val_str = f"${price:,.2f}"
                
            with cols[i]:
                if price > 0:
                    st.metric(label=label_visual, value=val_str, delta=f"{change:.2f}%")
                    st.caption(f"**{nombre_legible}**")
                    if not trend.empty: st.line_chart(trend, height=75, use_container_width=True)
                else:
                    st.metric(label=ticker, value="Sincronizando...")
    st.markdown("---")

st.caption("M82 Sovereign Core Terminal v8.5 PRO • All Modules Consolidated.")
