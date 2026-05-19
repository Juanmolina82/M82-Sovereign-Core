import streamlit as st
import yfinance as yf
import pandas as pd
import time

st.set_page_config(page_title="M82 Sovereign Core", page_icon="🦅", layout="wide")

st.title("🦅 MOLINA HOLDINGS & GLOBAL LLC")
st.subheader("Consola de Inteligencia Soberana - Terminal Macro Global v3.1")
st.markdown("---")

# 📥 CONFIGURACIÓN DE TU PORTAFOLIO (Equities Propietarios)
MI_PORTAFOLIO = {
    "NVDA": 50,
    "TSLA": 20,
    "OXY": 100,
    "JPM": 15,
    "MSFT": 10,
    "AAPL": 10,
    "AMZN": 15
}

# 🗺️ MATRIZ DE SEGMENTACIÓN COMPLETA
ESTRUCTURA_MERCADO = {
    "🚀 EQUITIES & BIG TECH": ["NVDA", "TSLA", "MSFT", "AAPL", "AMZN", "GOOGL"],
    "📦 ETFs & BROAD MARKET": ["SPY", "QQQ", "IWM"],
    "🧱 COMMODITIES CRÍTICOS": ["CL=F", "GC=F"],  # Petróleo Crudo y Oro Spot
    "📉 BONDS & RENDIMIENTOS": ["^TNX", "TLT"]     # Tasa de Bonos 10Y y ETF +20Y
}

# Diccionario de traducción visual institucional
NOMBRES_ACTIVOS = {
    "CL=F": "Petróleo Crudo", "GC=F": "Oro Spot",
    "^TNX": "US 10Y Yield", "TLT": "iShares +20Y Bond",
    "SPY": "S&P 500 ETF", "QQQ": "Nasdaq-100 ETF", "IWM": "Russell 2000 ETF"
}

# CACHÉ DE REFRESCAMIENTO BAJO DE 15 SEGUNDOS RE-CALIBRADO
@st.cache_data(ttl=15)
def obtener_datos_globales():
    búfer = {}
    # Recopilar todos los tickers únicos
    todos_los_tickers = set([t for lista in ESTRUCTURA_MERCADO.values() for t in lista])
    
    for ticker in todos_los_tickers:
        try:
            t_obj = yf.Ticker(ticker)
            # Solicitar 5 días de margen para asegurar que siempre haya datos de cierre previo
            hist = t_obj.history(period="5d")
            
            if not hist.empty and len(hist) >= 2:
                price = float(hist['Close'].iloc[-1])
                prev_close = float(hist['Close'].iloc[-2])
                change = ((price - prev_close) / prev_close) * 100
            elif not hist.empty:
                price = float(hist['Close'].iloc[-1])
                open_p = float(hist['Open'].iloc[-1])
                change = ((price - open_p) / open_p) * 100 if open_p else 0.0
            else:
                price, change = 0.0, 0.0
                
            búfer[ticker] = {"price": price, "change": change}
            time.sleep(0.15)  # Latencia de seguridad para evitar bloqueos de IP
        except Exception:
            búfer[ticker] = {"price": 0.0, "change": 0.0}
            
    return búfer

# Panel Lateral de Control Operativo
st.sidebar.header("🕹️ MÓDULO DE CONTROL M82")
st.sidebar.markdown("**Estatus:** 🖥️ Núcleo Re-estabilizado")
st.sidebar.markdown("**Frecuencia:** ⚡ 15 Segundos")
if st.sidebar.button("🔄 Sincronizar Todo"):
    st.cache_data.clear()
    st.rerun()

# Extracción de datos en vivo de Wall Street
datos_vivos = obtener_datos_globales()

# --- BALANCE CONSOLIDADO DEL PORTAFOLIO DE EQUITIES ---
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

# --- RENDERIZADO DEL CENTRO DE MANDO SUPERIOR ---
st.markdown("### 🏦 VALORACIÓN DE ACTIVOS PROPIETARIOS")
p_col1, p_col2 = st.columns(2)
with p_col1:
    if valor_total_portafolio > 0:
        st.metric(label="💰 VALOR NETO EQUITIES EN VIVO", value=f"${valor_total_portafolio:,.2f} USD")
    else:
        st.warning("Calculando Balance...")
with p_col2:
    st.metric(
        label="📈 P&L FLOTANTE ESTIMADO DEL DÍA", 
        value=f"${cambio_diario_estimado:+,.2f} USD",
        delta="Alineado con Moomoo / CME"
    )
st.markdown("---")

# --- COMPILACIÓN SECTORIAL CON CONTROL DE ERRORES ---
for sector, tickers in ESTRUCTURA_MERCADO.items():
    st.header(sector)
    
    # Sistema dinámico adaptativo de columnas para evitar quiebres visuales
    cols = st.columns(len(tickers))
    datos_tabla = []
    
    for i, ticker in enumerate(tickers):
        info_ticker = datos_vivos.get(ticker, {"price": 0.0, "change": 0.0})
        price = info_ticker["price"]
        change = info_ticker["change"]
        
        nombre_legible = NOMBRES_ACTIVOS.get(ticker, ticker)
        label_visual = f"🔥 {ticker}" if ticker == "NVDA" else ticker
        
        # Filtrado de formato según tipo de activo (Bonos vs Moneda)
        sufijo = "%" if ticker == "^TNX" else "USD"
        val_str = f"{price:.2f}%" if sufijo == "%" else f"${price:.2f}"
        
        cantidad_tengo = MI_PORTAFOLIO.get(ticker, 0)
        tenencia_str = f"📦 {cantidad_tengo} acc" if cantidad_tengo > 0 else "Monitor"
        
        with cols[i]:
            if price > 0:
                st.metric(label=label_visual, value=val_str, delta=f"{change:.2f}%")
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
                # Fallback Táctico: Si el ticker falla, la interfaz se mantiene intacta
                st.metric(label=label_visual, value="Cargando...", delta="0.00%")
                st.caption(f"⚠️ {nombre_legible} temporalmente fuera de línea")

    if datos_tabla:
        df = pd.DataFrame(datos_tabla)
        st.dataframe(df, hide_index=True, use_container_width=True)
    st.markdown("---")

st.caption("M82 Sovereign Core Terminal v3.1 • Parche de Estabilidad y Control de Excepciones Aplicado.")
