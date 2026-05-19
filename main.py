import streamlit as st
import yfinance as yf
import pandas as pd
import time

# Configuración soberana de la interfaz de la App
st.set_page_config(page_title="M82 Sovereign Core", page_icon="📊", layout="wide")

st.title("🦅 MOLINA HOLDINGS & GLOBAL LLC")
st.subheader("Consola de Inteligencia Soberana - Broad Market Portfolio")
st.markdown("---")

# Matriz Multisectorial (Radar M82)
SECTORES = {
    "🚀 TECNOLOGÍA & IA": ["NVDA", "TSLA", "MSFT", "AAPL"],
    "🏦 FINANCIERO & BANCA": ["JPM", "BAC"],
    "📦 CONSUMO & DEFENSA": ["WMT", "KO", "LMT"]
}

def consultar_ticker_seguro(ticker):
    """Extrae métricas usando canales históricos de alta disponibilidad"""
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

# Renderizado dinámico de la App por Sectores
for sector, tickers in SECTORES.items():
    st.header(sector)
    cols = st.columns(len(tickers))
    
    datos_tabla = []
    
    for i, ticker in enumerate(tickers):
        price, pe_ratio, change = consultar_ticker_seguro(ticker)
        pe_str = f"{pe_ratio:.2f}x" if pe_ratio > 0 else "N/A"
        
        # Inyectar tarjetas métricas de alta visibilidad (Roncando duro)
        with cols[i]:
            if price > 0:
                st.metric(
                    label=f"🔥 {ticker}" if ticker == "NVDA" else ticker, 
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
                st.error(f"{ticker} - Error de red")
                
    # Mostrar tabla resumen limpia del sector para control de datos crudos
    if datos_tabla:
        df = pd.DataFrame(datos_tabla)
        st.dataframe(df, hide_index=True, use_container_width=True)
    st.markdown("---")

st.caption("M82 Sovereign Core App v2.0 • Datos provistos directamente desde Wall Street en tiempo real.")
