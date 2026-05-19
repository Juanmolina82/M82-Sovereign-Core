import streamlit as st
import yfinance as yf
import pandas as pd
import time

st.set_page_config(page_title="M82 Sovereign Core", page_icon="📊", layout="wide")

st.title("🦅 MOLINA HOLDINGS & GLOBAL LLC")
st.subheader("Consola de Inteligencia Soberana - Broad Market Portfolio")
st.markdown("---")

# 📥 CONFIGURACIÓN DE TU PORTAFOLIO (Establece tus tenencias aquí)
MI_PORTAFOLIO = {
    "NVDA": 50,
    "TSLA": 20,
    "OXY": 100,
    "JPM": 15,
    "MSFT": 10
}

# Matriz Ampliada de Sectores
SECTORES = {
    "🚀 TECNOLOGÍA & IA": ["NVDA", "TSLA", "MSFT", "AAPL"],
    "🛢️ ENERGÍA E INFRAESTRUCTURA": ["OXY", "CVX", "XOM"],
    "🏦 FINANCIERO & BANCA": ["JPM", "BAC"],
    "📦 CONSUMO & DEFENSA": ["WMT", "KO", "LMT"]
}

@st.cache_data(ttl=120)  # Caché inteligente de 2 minutos para mitigar bloqueos de IP
def obtener_datos_mercado():
    """Realiza un único barrido de datos limpio y estructurado"""
    búfer = {}
    todos_los_tickers = set([t for lista in SECTORES.values() for t in lista])
    
    for ticker in todos_los_tickers:
        try:
            t_obj = yf.Ticker(ticker)
            hist = t_obj.history(period="1d")
            if not hist.empty:
                price = float(hist['Close'].iloc[-1])
                open_p = float(hist['Open'].iloc[-1])
                change = ((price - open_p) / open_p) * 100 if open_p else 0.0
            else:
                price, change = 0.0, 0.0
                
            try:
                info = t_obj.info
                pe_ratio = info.get("trailingPE") or info.get("forwardPE") or 0.0
            except Exception:
                pe_ratio = 0.0
                
            búfer[ticker] = {"price": price, "pe": pe_ratio, "change": change}
            time.sleep(1.5)  # Retraso defensivo controlado
        except Exception:
            búfer[ticker] = {"price": 0.0, "pe": 0.0, "change": 0.0}
            
    return búfer

# Sidebar de Control Operacional
st.sidebar.header("🕹️ MÓDULO DE CONTROL M82")
st.sidebar.markdown("**Estatus de Red:** 🟢 Conectado a Wall Street")
if st.sidebar.button("🔄 Refrescar Métmeras en Vivo"):
    st.cache_data.clear()
    st.rerun()

# Cargar el búfer unificado de Wall Street
datos_vivos = obtener_datos_mercado()

# --- CÁLCULO FINANCIERO SEGURO DEL PORTAFOLIO ---
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

# --- DESPLIEGUE VISUAL DEL BALANCE NETO ---
st.markdown("### 🏦 RESUMEN EJECUTIVO DEL PORTAFOLIO")
p_col1, p_col2 = st.columns(2)
with p_col1:
    st.metric(label="💰 VALOR NETO TOTAL DE ACTIVOS", value=f"${valor_total_portafolio:,.2f} USD")
with p_col2:
    st.metric(
        label="📈 RENDIMIENTO ESTIMADO DEL DÍA (USD)", 
        value=f"${cambio_diario_estimado:+,.2f} USD",
        delta="Impacto directo" if cambio_diario_estimado != 0 else "Estable"
    )
st.markdown("---")

# --- RENDERIZADO DE MATRICES SECTORIALES ---
for sector, tickers in SECTORES.items():
    st.header(sector)
    cols = st.columns(len(tickers))
    datos_tabla = []
    
    for i, ticker in enumerate(tickers):
        info_ticker = datos_vivos.get(ticker, {"price": 0.0, "pe": 0.0, "change": 0.0})
        price = info_ticker["price"]
        pe_ratio = info_ticker["pe"]
        change = info_ticker["change"]
        
        pe_str = f"{pe_ratio:.2f}x" if pe_ratio > 0 else "N/A"
        cantidad_tengo = MI_PORTAFOLIO.get(ticker, 0)
        tenencia_str = f"📦 Tienes: {cantidad_tengo} acc" if cantidad_tengo > 0 else "No posicionado"
        
        with cols[i]:
            if price > 0:
                label_ticker = f"🔥 {ticker}" if ticker == "NVDA" else ticker
                st.metric(label=label_ticker, value=f"${price:.2f} USD", delta=f"{change:.2f}%")
                st.caption(f"**P/E:** {pe_str} | {tenencia_str}")
                
                datos_tabla.append({
                    "Ticker": ticker,
                    "Precio Spot": f"${price:.2f}",
                    "Variación": f"{change:.2f}%",
                    "Múltiplo P/E": pe_str,
                    "Tu Tenencia": cantidad_tengo
                })
            else:
                st.error(f"{ticker} - En espera")
                
    if datos_tabla:
        df = pd.DataFrame(datos_tabla)
        st.dataframe(df, hide_index=True, use_container_width=True)
    st.markdown("---")

st.caption("M82 Sovereign Core App v2.4 • Entorno optimizado contra rate-limiting y fallos de llave.")
