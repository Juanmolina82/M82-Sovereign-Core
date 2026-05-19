import streamlit as st
import yfinance as yf
import pandas as pd
import time

st.set_page_config(page_title="M82 Sovereign Core", page_icon="📊", layout="wide")

st.title("🦅 MOLINA HOLDINGS & GLOBAL LLC")
st.subheader("Consola de Inteligencia Soberana - Broad Market Portfolio")
st.markdown("---")

# Matriz Ampliada: Inclusión de Energía de Grado Institucional
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

# Módulo de Control Sidebar
st.sidebar.header("🕹️ MÓDULO DE CONTROL M82")
st.sidebar.markdown("**Estatus de Red:** 🟢 Conectado a Wall Street")
if st.sidebar.button("🔄 Refrescar Métricas en Vivo"):
    st.rerun()

# Despliegue de los Cuatro Pilares
for sector, tickers in SECTORES.items():
    st.header(sector)
    cols = st.columns(len(tickers))
    datos_tabla = []
    
    for i, ticker in enumerate(tickers):
        price, pe_ratio, change = consultar_ticker_seguro(ticker)
        pe_str = f"{pe_ratio:.2f}x" if pe_ratio > 0 else "N/A"
        
        with cols[i]:
            if price > 0:
                # Distintivo especial para el núcleo de IA
                label_ticker = f"🔥 {ticker}" if ticker == "NVDA" else ticker
                st.metric(
                    label=label_ticker, 
                    value=f"${price:.2f} USD", 
                    delta=f"{change:.2f}%"
                )
                st.caption(f"**P/E Ratio:** {pe_str}")
                
                datos_tabla.append({
                    "Ticker": ticker,
                    "Precio Spot": f"${price:.2f}",
                    "Variación": f"{change:.2f}%",
                    "Múltiplo P/E": pe_str
                })
            else:
                st.error(f"{ticker} - Error de canal")
                
    if datos_tabla:
        df = pd.DataFrame(datos_tabla)
        st.dataframe(df, hide_index=True, use_container_width=True)
    st.markdown("---")

st.caption("M82 Sovereign Core App v2.2 • Datos multisectoriales consolidados y optimizados.")
