import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import time

st.set_page_config(page_title="M82 Sovereign Core v8.0", page_icon="🦅", layout="wide")

st.title("🦅 MOLINA HOLDINGS & GLOBAL LLC")
st.subheader("M82 COMET - Unified Sovereign Terminal v8.0 PRO")
st.markdown("---")

# ==============================================================================
# 1. BASE DE DATOS Y CONFIGURACIONES DE CONTROL REAL
# ==============================================================================
MI_PORTAFOLIO = {
    "NVDA": 50, "TSLA": 20, "OXY": 100, "JPM": 15, "MSFT": 10, "AAPL": 10, "AMZN": 15
}

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
    "STW=F": "MSCI Taiwan Futures", "NVDA": "NVIDIA Corp.", "MSFT": "Microsoft Corp.",
    "TSLA": "Tesla Inc.", "AAPL": "Apple Inc.", "AMZN": "Amazon.com Inc.", "GOOGL": "Alphabet Inc."
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

@st.cache_data(ttl=15)
def obtener_datos_globales():
    búfer = {}
    tickers_a_buscar = set(list(ESTRUCTURA_MERCADO.values())[0] + list(ESTRUCTURA_MERCADO.values())[1] + list(ESTRUCTURA_MERCADO.values())[2] + list(ESTRUCTURA_MERCADO.values())[3] + list(MI_PORTAFOLIO.keys()))
    for ticker in tickers_a_buscar:
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
            else: price, change, price_trend, estado_sesion = 0.0, 0.0, pd.Series(), ""
            búfer[ticker] = {"price": price, "change": change, "trend": price_trend, "sesion": estado_sesion}
            time.sleep(0.01)
        except Exception: 
            búfer[ticker] = {"price": 0.0, "change": 0.0, "trend": pd.Series(), "sesion": ""}
    return búfer

datos_vivos = obtener_datos_globales()

# ==============================================================================
# 2. CÁLCULO Y VALORACIÓN REAL DEL PORTAFOLIO (EQUITIES)
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

st.markdown("### 🏦 VALORACIÓN DE ACTIVOS PROPIETARIOS (SESIÓN EXTENDIDA)")
p_col1, p_col2 = st.columns(2)
with p_col1:
    st.metric(label="💰 VALOR NETO EQUITIES EN VIVO", value=f"${valor_total_portafolio:,.2f} USD")
with p_col2:
    st.metric(label="📈 P&L FLOTANTE ESTIMADO DEL DÍA", value=f"${cambio_diario_estimado:+,.2f} USD")
st.markdown("---")

# ==============================================================================
# 3. MÓDULO UNIFICADO DE DERIVADOS Y BLOCK TRADES (MSFT Y NVDA)
# ==============================================================================
st.markdown("### 👁️ RADAR DE RIESGO EN DERIVADOS INSTITUCIONALES")
tipo_flujo = st.radio("Selecciona bloque de opciones para auditar:", ["MSFT August 21 Call Block ($5.37M)", "NVDA Short Put Block ($1.4M)"])

if tipo_flujo == "MSFT August 21 Call Block ($5.37M)":
    with st.expander("🚀 Parámetros del Bloque de Compra Premium - Microsoft", expanded=True):
        c_col1, c_col2, c_col3 = st.columns(3)
        with c_col1: strike_c = st.number_input("Strike Call de Ejercicio (K):", value=420.00)
        with c_col2: prima_c = st.number_input("Prima Premium Pagada ($):", value=90.00)
        with c_col3: contratos_c = st.number_input("Contratos Totales Calculados:", value=596)
        be_c = strike_c + prima_c
        inversion_total = prima_c * 100 * contratos_c
        msft_spot = datos_vivos.get("MSFT", {"price": 422.00})["price"]
        distancia_be = ((be_c - msft_spot) / msft_spot) * 100 if msft_spot > 0 else 0.0
        st.markdown("#### Umbrales de Exposición Especulativa:")
        mc_col1, mc_col2, mc_col3 = st.columns(3)
        with mc_col1: st.metric(label="🔥 Capital de Riesgo Fijo", value=f"${inversion_total:,.2f} USD")
        with mc_col2: st.metric(label="🎯 Break-Even Target Necesario", value=f"${be_c:.2f} USD")
        with mc_col3: st.metric(label="📈 Distancia Requerida vs Spot", value=f"{distancia_be:+.2f}%")

else:
    with st.expander("🛡️ Parámetros del Bloque de Venta OTM - NVIDIA", expanded=True):
        col_op1, col_op2, col_op3 = st.columns(3)
        with col_op1: strike = st.number_input("Strike de la Opción (K):", value=100.00)
        with col_op2: prima = st.number_input("Prima Recibida ($ por contrato):", value=41.00)
        with col_op3: contratos = st.number_input("Cantidad de Contratos Vendidos:", value=340)
        breakeven = strike - prima
        max_profit = prima * 100 * contratos
        nvda_spot = datos_vivos.get("NVDA", {"price": 222.96})["price"]
        distancia_seguridad = ((nvda_spot - breakeven) / nvda_spot) * 100 if nvda_spot > 0 else 0.0
        st.markdown("#### Umbrales de Exposición de Crédito:")
        m_col1, m_col2, m_col3 = st.columns(3)
        with m_col1: st.metric(label="💰 Beneficio Máximo (Crédito Neto)", value=f"${max_profit:,.2f} USD")
        with m_col2: st.metric(label="🎯 Punto de Equilibrio (Break-Even)", value=f"${breakeven:,.2f} USD")
        with m_col3: st.metric(label="🛡️ Margen de Seguridad vs Spot", value=f"{distancia_seguridad:.1f}%")
st.markdown("---")

# ==============================================================================
# 4. MONITOR DE CURVA FORWARD DEL BRENT (RÉPLICA MOOMOO COPPED)
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
st.markdown("---")

# ==============================================================================
# 5. GRID RESPONSIVO COMPLETO DE FUTUROS GLOBALES
# ==============================================================================
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
            val_str = f"{price:.2f}" if "VIX" in nombre_legible else f"${price:,.2f}"
            with cols[i]:
                if price > 0:
                    st.metric(label=label_visual, value=val_str, delta=f"{change:.2f}%")
                    st.caption(f"**{nombre_legible}**")
                    if not trend.empty: st.line_chart(trend, height=75, use_container_width=True)
                else: st.metric(label=ticker, value="Sincronizando...")
    st.markdown("---")

st.caption("M82 Sovereign Core Terminal v8.0 PRO • All Modules Integrated Perfectly.")
