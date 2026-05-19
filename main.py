import streamlit as st
import yfinance as yf
import pandas as pd
import time

st.set_page_config(page_title="M82 Sovereign Core", page_icon="📊", layout="wide")

st.title("🦅 MOLINA HOLDINGS & GLOBAL LLC")
st.subheader("Consola de Inteligencia Soberana - Ultra Low-Latency Feed")
st.markdown("---")

# 📥 PORTAFOLIO DE ACTIVOS
MI_PORTAFOLIO = {
    "NVDA": 50,
    "TSLA": 20,
    "OXY": 100,
    "JPM": 15,
    "MSFT": 10
}

# MATRIZ MULTISECTORIAL PREMANENTMENTE MONITOREADA
SECTORES = {
    "🚀 TECNOLOGÍA & IA": ["NVDA", "TSLA", "MSFT", "AAPL"],
    "🛢️ ENERGÍA E INFRAESTRUCTURA": ["OXY", "CVX", "XOM"],
    "🏦 FINANCIERO & BANCA": ["JPM", "BAC"],
    "📦 CONSUMO & DEFENSA": ["WMT", "KO", "LMT"]
}

# REDUCCIÓN DE CACHÉ A 15 SEGUNDOS PARA REFRESCAMIENTO CASI INSTANTÁNEO
@st.cache_data(ttl=15)
def obtener_datos_mercado():
    búfer = {}
    todos_los_tickers = set([t for lista in SECTORES.values() for t in lista])
    
    for ticker in todos_los_tickers:
        try:
            t_obj = yf.Ticker(ticker)
            # Traemos un espectro corto pero rápido de datos históricos
            hist = t_obj.history(period="2d")
            if len(hist) >= 2:
                price = float(hist['Close'].iloc[-1])
                prev_close = float(hist['Close'].iloc[-2])
                # Alineación con brókeres: Cambio porcentual respecto al CIERRE de ayer
                change = ((price - prev_close) / prev_close) * 100 if prev_close else 0.0
            elif not hist.empty:
                price = float(hist['Close'].iloc[-1])
                open_p = float(hist['Open'].iloc[-1])
                change = ((price - open_p) / open_p) * 100 if open_p else 0.0
            else:
                price, change = 0.0, 0.0
                
            búfer[ticker] = {"price": price, "pe": 0.0, "change": change}
            time.sleep(0.2)  # Inyección acelerada (0.2s en lugar de 1.5s)
        except Exception:
            búfer[ticker] = {"price": 0.0, "pe": 0.0, "change": 0.0}
            
    return búfer

# Interfaz Lateral Activa
st.sidebar.header("🕹️ MÓDULO DE CONTROL M82")
st.sidebar.markdown("**Modo de Telemetría:** ⚡ Rápido (15s Cache)")
if st.sidebar.button("🔄 Forzar Barrido de Wall Street"):
    st.cache_data.clear()
    st.rerun()

datos_vivos = obtener_datos_mercado()

# --- CÁLCULO SEGURO DEL PORTAFOLIO ---
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

# --- DESPLIEGUE DEL BALANCE NETO ---
st.markdown("### 🏦 RESUMEN EJECUTIVO DEL PORTAFOLIO")
p_col1, p_col2 = st.columns(2)
with p_col1:
    st.metric(label="💰 VALOR NETO TOTAL DE ACTIVOS", value=f"${valor_total_portafolio:,.2f} USD")
with p_col2:
    st.metric(
        label="📈 RENDIMIENTO ESTIMADO DEL DÍA (USD)", 
        value=f"${cambio_diario_estimado:+,.2f} USD",
        delta="Sincronizado con cierre previo"
    )
st.markdown("---")

# --- RENDERIZADO DE MATRICES SECTORIALES ---
for sector, tickers in SECTORES.items():
    st.header(sector)
    cols = st.columns(len(tickers))
    datos_tabla = []
    
    for i, ticker in enumerate(tickers):
        info_ticker = datos_vivos.get(ticker, {"price": 0.0, "change": 0.0})
        price = info_ticker["price"]
        change = info_ticker["change"]
        
        cantidad_tengo = MI_PORTAFOLIO.get(ticker, 0)
        tenencia_str = f"📦 {cantidad_tengo} acc" if cantidad_tengo > 0 else "Sin posición"
        
        with cols[i]:
            if price > 0:
                label_ticker = f"🔥 {ticker}" if ticker == "NVDA" else ticker
                st.metric(label=label_ticker, value=f"${price:.2f} USD", delta=f"{change:.2f}%")
                st.caption(f"**Tenencia:** {tenencia_str}")
                
                datos_tabla.append({
                    "Ticker": ticker,
                    "Precio Spot": f"${price:.2f}",
                    "Variación Diaria": f"{change:.2f}%",
                    "Tu Posición": tenencia_str
                })
            else:
                st.error(f"{ticker} - Actualizando")
                
    if datos_tabla:
        df = pd.DataFrame(datos_tabla)
        st.dataframe(df, hide_index=True, use_container_width=True)
    st.markdown("---")

st.caption("M82 Sovereign Core App v2.5 • Feed optimizado de baja latencia.")
