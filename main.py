import streamlit as st
import yfinance as yf
import pandas as pd
import time

st.set_page_config(page_title="M82 Sovereign Core", page_icon="🦅", layout="wide")

st.title("🦅 MOLINA HOLDINGS & GLOBAL LLC")
st.subheader("Consola de Inteligencia Soberana - Terminal Macro Global v3.0")
st.markdown("---")

# 📥 CONFIGURACIÓN EXPANDIDA DE TU PORTAFOLIO (Equities Activos)
MI_PORTAFOLIO = {
    "NVDA": 50,
    "TSLA": 20,
    "OXY": 100,
    "JPM": 15,
    "MSFT": 10,
    "AAPL": 10,
    "AMZN": 15
}

# 🗺️ MATRIZ DE SEGMENTACIÓN GLOBAL DE MERCADOS
ESTRUCTURA_MERCADO = {
    "🚀 EQUITIES & BIG TECH": ["NVDA", "TSLA", "MSFT", "AAPL", "AMZN", "GOOGL"],
    "📦 ETFs & BROAD MARKET": ["SPY", "QQQ", "IWM", "DIA"],
    "🧱 COMMODITIES CRÍTICOS": ["CL=F", "GC=F", "SI=F", "NG=F"],  # Petróleo, Oro, Plata, Gas Natural
    "📉 BONDS & RENDIMIENTOS": ["^TNX", "TLT", "IEF"]             # Tasa 10Y, Bonos +20Y, Bonos 7-10Y
}

# Diccionario para nombres amigables en la UI
NOMBRES_ACTIVOS = {
    "CL=F": "Petróleo Crudo", "GC=F": "Oro Spot", "SI=F": "Plata Spot", "NG=F": "Gas Natural",
    "^TNX": "US 10Y Yield", "TLT": "iShares +20Y Bond", "IEF": "iShares 7-10Y Bond",
    "SPY": "S&P 500 ETF", "QQQ": "Nasdaq-100 ETF", "IWM": "Russell 2000 ETF", "DIA": "Dow Jones ETF"
}

# FEED ACELERADO: 15 SEGUNDOS DE CACHÉ ANTI-DELAY
@st.cache_data(ttl=15)
def obtener_datos_globales():
    búfer = {}
    todos_los_tickers = set([t for lista in ESTRUCTURA_MERCADO.values() for t in lista])
    
    for ticker in todos_los_tickers:
        try:
            t_obj = yf.Ticker(ticker)
            hist = t_obj.history(period="2d")
            
            if len(hist) >= 2:
                price = float(hist['Close'].iloc[-1])
                prev_close = float(hist['Close'].iloc[-2])
                change = ((price - prev_close) / prev_close) * 100 if prev_close else 0.0
            elif not hist.empty:
                price = float(hist['Close'].iloc[-1])
                open_p = float(hist['Open'].iloc[-1])
                change = ((price - open_p) / open_p) * 100 if open_p else 0.0
            else:
                price, change = 0.0, 0.0
                
            búfer[ticker] = {"price": price, "change": change}
            time.sleep(0.15)  # Barrido asíncrono optimizado de alta velocidad
        except Exception:
            búfer[ticker] = {"price": 0.0, "change": 0.0}
            
    return búfer

# Barra de Mandos Lateral
st.sidebar.header("🕹️ MÓDULO DE CONTROL M82")
st.sidebar.markdown("**Modo Visual:** Multi-Asset Broad Feed")
st.sidebar.markdown("**Latencia:** ⚡ Ultra-Baja (15s)")
if st.sidebar.button("🔄 Forzar Sincronización Global"):
    st.cache_data.clear()
    st.rerun()

# Captura de datos vivos de Wall Street
datos_vivos = obtener_datos_globales()

# --- BALANCE FINANCIERO DE TU CARTERA EQUITIES ---
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

# --- DESPLIEGUE DEL CENTRO DE MANDO SUPERIOR ---
st.markdown("### 🏦 VALORACIÓN DE ACTIVOS PROPIETARIOS")
p_col1, p_col2 = st.columns(2)
with p_col1:
    st.metric(label="💰 VALOR NETO EQUITIES EN VIVO", value=f"${valor_total_portafolio:,.2f} USD")
with p_col2:
    st.metric(
        label="📈 P&L FLOTANTE ESTIMADO DEL DÍA", 
        value=f"${cambio_diario_estimado:+,.2f} USD",
        delta="Sincronizado tick-by-tick"
    )
st.markdown("---")

# --- RENDERIZADO INTELIGENTE DE SECCIONES MULTI-ACTIVOS ---
for sector, tickers in ESTRUCTURA_MERCADO.items():
    st.header(sector)
    cols = st.columns(len(tickers))
    datos_tabla = []
    
    for i, ticker in enumerate(tickers):
        info_ticker = datos_vivos.get(ticker, {"price": 0.0, "change": 0.0})
        price = info_ticker["price"]
        change = info_ticker["change"]
        
        # Formatear etiquetas dinámicas
        nombre_legible = NOMBRES_ACTIVOS.get(ticker, ticker)
        label_final = f"🔥 {ticker}" if ticker == "NVDA" else ticker
        
        # Identificar si el activo es un Bono/Rendimiento para cambiar el sufijo
        sufijo = "%" if ticker == "^TNX" else "USD"
        val_str = f"{price:.2f}%" if sufijo == "%" else f"${price:.2f}"
        
        cantidad_tengo = MI_PORTAFOLIO.get(ticker, 0)
        tenencia_str = f"📦 {cantidad_tengo} acc" if cantidad_tengo > 0 else "Monitor"
        
        with cols[i]:
            if price > 0:
                st.metric(label=label_final, value=val_str, delta=f"{change:.2f}%")
                st.caption(f"**{nombre_legible}**")
                st.caption(f"*{tenencia_str}*")
                
                datos_tabla.append({
                    "Activo": nombre_legible,
                    "Ticker": ticker,
                    "Precio / Cotización": val_str,
                    "Variación": f"{change:.2f}%",
                    "Estatus": tenencia_str
                })
            else:
                st.error(f"{ticker}")
                
    if datos_tabla:
        df = pd.DataFrame(datos_tabla)
        st.dataframe(df, hide_index=True, use_container_width=True)
    st.markdown("---")

st.caption("M82 Sovereign Core Terminal v3.0 • Consolidación Macro Global Multi-Activos.")
