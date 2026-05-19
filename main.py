import streamlit as st
import yfinance as yf
import pandas as pd
import time

st.set_page_config(page_title="M82 Sovereign Core v4.0", page_icon="🦅", layout="wide")

st.title("🦅 MOLINA HOLDINGS & GLOBAL LLC")
st.subheader("M82 COMET - Advanced Performance Terminal v4.0")
st.markdown("---")

# 📥 CONFIGURACIÓN DE TU PORTAFOLIO REAL DE EQUITIES
MI_PORTAFOLIO = {
    "NVDA": 50,
    "TSLA": 20,
    "OXY": 100,
    "JPM": 15,
    "MSFT": 10,
    "AAPL": 10,
    "AMZN": 15
}

# 🗺️ MATRIZ DE MERCADO SATURADA (Inyección de Estamina Global)
ESTRUCTURA_MERCADO = {
    "🚀 EQUITIES & BIG TECH": ["NVDA", "TSLA", "MSFT", "AAPL", "AMZN", "GOOGL"],
    "📦 ETFs & FUTURES": ["SPY", "QQQ", "IWM", "NQ=F"],           # Russell 2000 y Futuros Nasdaq
    "🧱 COMMODITIES CRÍTICOS": ["CL=F", "GC=F", "NG=F", "SI=F"], # Gas Natural y Plata
    "📉 BONDS & RATES": ["^TNX", "TLT"]
}

# Diccionario de nombres institucionales M82
NOMBRES_ACTIVOS = {
    "CL=F": "Petróleo Crudo", "GC=F": "Oro Spot",
    "^TNX": "US 10Y Yield", "TLT": "iShares +20Y Bond",
    "SPY": "S&P 500 ETF", "QQQ": "Nasdaq-100 ETF", "IWM": "Russell 2000 ETF",
    "NQ=F": "Futuros Nasdaq-100", "NG=F": "Gas Natural", "SI=F": "Plata Spot"
}

# UMBRAL DE VOLATILIDAD PARA ALERTAS DE RIESGO
UMBRAL_RIESGO = 5.0 # Porcentaje

# FEED ACELERADO DE 15 SEGUNDOS CON TRACCIÓN DE MOMENTUM (2 DIAS DE DATOS)
@st.cache_data(ttl=15)
def obtener_datos_globales():
    búfer = {}
    todos_los_tickers = set([t for lista in ESTRUCTURA_MERCADO.values() for t in lista])
    
    for ticker in todos_los_tickers:
        try:
            t_obj = yf.Ticker(ticker)
            # Solicitamos 2 días de datos para tener momentum intradiario/previo
            hist = t_obj.history(period="2d", interval="15m")
            
            if not hist.empty and len(hist) >= 2:
                # Datos de cierre de sesión previa para delta real (estilo moomoo)
                daily_hist = t_obj.history(period="5d")
                price = float(daily_hist['Close'].iloc[-1])
                prev_close = float(daily_hist['Close'].iloc[-2])
                change = ((price - prev_close) / prev_close) * 100
                # Historial para minicharts
                price_trend = hist['Close']
            else:
                price, change, price_trend = 0.0, 0.0, pd.Series()
                
            búfer[ticker] = {"price": price, "change": change, "trend": price_trend}
            time.sleep(0.08)  # Descarga ultra-rápida y sincronizada
        except Exception:
            búfer[ticker] = {"price": 0.0, "change": 0.0, "trend": pd.Series()}
            
    return búfer

# Panel Lateral Control Remoto Táctico
st.sidebar.header("🕹️ MÓDULO DE CONTROL v4.0")
st.sidebar.markdown("**Estatus:** ⚡ Motor Comet Activo")
st.sidebar.markdown("**Frecuencia:** ⏱️ 15s (CME Feed Style)")
if st.sidebar.button("🔄 Sincronizar Todo Wall Street"):
    st.cache_data.clear()
    st.rerun()

datos_vivos = obtener_datos_globales()

# --- BALANCE CONSOLIDADO DEL PORTAFOLIO DE EQUITIES ---
valor_total_portafolio = 0.0
cambio_diario_estimado = 0.0

for ticker, cantidad in MI_PORTAFOLIO.items():
    info_ticker = datos_vivos.get(ticker, {"price": 0.0, "change": 0.0})
    p = info_ticker["price"]
    c = info_ticker["change"]
    
    # Exclusión táctica de Bonos e Indices del cálculo del valor neto
    if p > 0 and ticker not in ["^TNX", "SPY", "QQQ", "IWM", "NQ=F"]:
        valor_posicion = p * cantidad
        valor_total_portafolio += valor_posicion
        cambio_diario_estimado += (valor_posicion * (c / 100))

# --- CENTRO DE MANDO SUPERIOR: VISUALIZACIÓN DE PERFORMANCE ---
st.markdown("### 🏦 VALORACIÓN DE ACTIVOS PROPIETARIOS")
p_col1, p_col2 = st.columns(2)
with p_col1:
    if valor_total_portafolio > 0:
        st.metric(label="💰 VALOR NETO EQUITIES EN VIVO", value=f"${valor_total_portafolio:,.2f} USD")
    else:
        st.warning("🔄 Sincronizando balance...")
with p_col2:
    # Lógica de alerta de volatilidad
    status_msg = "Sincronizado con CME Feed"
    volatility_alert = any(abs(datos_vivos.get(t, {}).get("change", 0.0)) >= UMBRAL_RIESGO for t in ["NQ=F", "NVDA", "CL=F"])
    if volatility_alert:
        status_msg = "🚨 ALERTA DE VOLATILIDAD ELEVADA 🚨"
        st.metric(
            label="📈 P&L FLOTANTE ESTIMADO DEL DÍA", 
            value=f"${cambio_diario_estimado:+,.2f} USD",
            delta=status_msg,
            delta_color="off" # Color neutro para alertar
        )
    else:
        st.metric(
            label="📈 P&L FLOTANTE ESTIMADO DEL DÍA", 
            value=f"${cambio_diario_estimado:+,.2f} USD",
            delta=status_msg
        )
st.markdown("---")

# --- COMPILACIÓN SECTORIAL CON MOMENTUM (Minicharts) ---
for sector, tickers in ESTRUCTURA_MERCADO.items():
    st.header(sector)
    cols = st.columns(len(tickers))
    datos_tabla = []
    
    for i, ticker in enumerate(tickers):
        info_ticker = datos_vivos.get(ticker, {"price": 0.0, "change": 0.0, "trend": pd.Series()})
        price = info_ticker["price"]
        change = info_ticker["change"]
        trend = info_ticker["trend"]
        
        nombre_legible = NOMBRES_ACTIVOS.get(ticker, ticker)
        label_visual = f"🔥 {ticker}" if ticker == "NVDA" else ticker
        
        is_bond = (ticker == "^TNX")
        is_qty = (ticker not in ["^TNX", "SPY", "QQQ", "IWM", "NQ=F", "CL=F", "GC=F", "NG=F", "SI=F"])
        
        val_str = f"{price:.2f}%" if is_bond else f"${price:.2f}"
        
        cantidad_tengo = MI_PORTAFOLIO.get(ticker, 0)
        tenencia_str = f"📦 {cantidad_tengo} acc" if is_qty and cantidad_tengo > 0 else "Monitor"
        
        with cols[i]:
            if price > 0:
                st.metric(label=label_visual, value=val_str, delta=f"{change:.2f}%")
                st.caption(f"**{nombre_legible}**")
                # Inyección de Minichart (Momentum)
                if not trend.empty:
                    st.line_chart(trend, height=80, use_container_width=True)
                st.caption(f"*{tenencia_str}*")
                
                datos_tabla.append({
                    "Activo": nombre_legible,
                    "Ticker": ticker,
                    "Cotización": val_str,
                    "Variación": f"{change:.2f}%",
                    "Estatus": tenencia_str
                })
            else:
                st.metric(label=label_visual, value="Actualizando", delta="0.00%")
                st.caption(f"⚠️ {nombre_legible}")

    if datos_tabla:
        df = pd.DataFrame(datos_tabla)
        st.dataframe(df, hide_index=True, use_container_width=True)
    st.markdown("---")

st.caption("M82 Sovereign Core Terminal v4.0 PRO • Advanced Performance Edition con Módulos de Momentum y Control de Riesgo.")
