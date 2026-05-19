import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(page_title="M82 Sovereign Core", page_icon="📊", layout="wide")

st.title("🦅 MOLINA HOLDINGS & GLOBAL LLC")
st.subheader("Consola de Inteligencia Soberana - Broad Market Portfolio")
st.markdown("---")

# 📥 CONFIGURACIÓN DE TU PORTAFOLIO (Modifica las cantidades a tu gusto)
# Estructura: "TICKER": Cantidad de acciones en tenencia
MI_PORTAFOLIO = {
    "NVDA": 50,    # Ejemplo: 50 acciones de NVIDIA
    "TSLA": 20,    # Ejemplo: 20 acciones de Tesla
    "OXY": 100,    # Ejemplo: 100 acciones de Occidental Petroleum
    "JPM": 15,     # Ejemplo: 15 acciones de JPMorgan
    "MSFT": 10     # Ejemplo: 10 acciones de Microsoft
}

# Matriz Ampliada de Sectores
SECTORES = {
    "🚀 TECNOLOGÍA & IA": ["NVDA", "TSLA", "MSFT", "AAPL"],
    "🛢️ ENERGÍA E INFRAESTRUCTURA": ["OXY", "CVX", "XOM"],
    "🏦 FINANCIERO & BANCA": ["JPM", "BAC"],
    "📦 CONSUMO & DEFENSA": ["WMT", "KO", "LMT"]
}

def consultar_ticker_seguro(ticker):
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
            
        return price, pe_ratio, change
    except Exception:
        return 0.0, 0.0, 0.0

# Sidebar de Control Operacional
st.sidebar.header("🕹️ MÓDULO DE CONTROL M82")
st.sidebar.markdown("**Estatus de Red:** 🟢 Conectado a Wall Street")
if st.sidebar.button("🔄 Refrescar Métricas en Vivo"):
    st.rerun()

# --- PROCESAMIENTO PREVIO DEL PORTAFOLIO ---
valor_total_portafolio = 0.0
cambio_diario_estimado = 0.0

# Mapear de antemano todos los tickers del portafolio para el cálculo del balance
for ticker, cantidad in MI_PORTAFOLIO.items():
    p, _, c = consultar_ticker_seguro(ticker)
    if p > 0:
        valor_posicion = p * cantidad
        valor_total_portafolio += valor_posicion
        # Calcular impacto ponderado del cambio diario en USD
        cambio_diario_estimado += (valor_posicion * (c / 100))

# --- DESPLIEGUE DEL BALANCE NETO EN LA PARTE SUPERIOR ---
st.markdown("### 🏦 RESUMEN EJECUTIVO DEL PORTAFOLIO")
p_col1, p_col2 = st.columns(2)
with p_col1:
    st.metric(label="💰 VALOR NETO TOTAL DE ACTIVOS", value=f"${valor_total_portafolio:,.2f} USD")
with p_col2:
    st.metric(
        label="📈 RENDIMIENTO ESTIMADO DEL DÍA (USD)", 
        value=f"${cambio_diario_estimado:+,.2f} USD",
        delta=f"Impacto directo" if cambio_diario_estimado != 0 else "Estable"
    )
st.markdown("---")

# Despliegue de las Matrices Sectoriales del Market
for sector, tickers in SECTORES.items():
    st.header(sector)
    cols = st.columns(len(tickers))
    datos_tabla = []
    
    for i, ticker in enumerate(tickers):
        price, pe_ratio, change = consultar_ticker_seguro(ticker)
        pe_str = f"{pe_ratio:.2f}x" if pe_ratio > 0 else "N/A"
        
        with cols[i]:
            if price > 0:
                label_ticker = f"🔥 {ticker}" if ticker == "NVDA" else ticker
                # Si el usuario posee este ticker, mostrar la cantidad abajo
                tenencia_str = f"📦 Tienes: {MI_PORTAFOLIO[ticker]} acc" if ticker in MI_PORTAFOLIO else "No posicionado"
                
                st.metric(label=label_ticker, value=f"${price:.2f} USD", delta=f"{change:.2f}%")
                st.caption(f"**P/E:** {pe_str} | {tenencia_str}")
                
                datos_tabla.append({
                    "Ticker": ticker,
                    "Precio Spot": f"${price:.2f}",
                    "Variación": f"{change:.2f}%",
                    "Múltiplo P/E": pe_str,
                    "Tu Tenencia": MI_PORTAFOLIO.get(ticker, 0)
                })
            else:
                st.error(f"{ticker} - Error de canal")
                
    if datos_tabla:
        df = pd.DataFrame(datos_tabla)
        st.dataframe(df, hide_index=True, use_container_width=True)
    st.markdown("---")

st.caption("M82 Sovereign Core App v2.3 • Balance y analíticas de mercado consolidadas para uso exclusivo de la firma.")
