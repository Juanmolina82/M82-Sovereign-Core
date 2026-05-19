import streamlit as st
import yfinance as yf
import pandas as pd
import time

st.set_page_config(page_title="M82 Sovereign Core", page_icon="🦅", layout="wide")

st.title("🦅 MOLINA HOLDINGS & GLOBAL LLC")
st.subheader("Consola de Inteligencia Soberana - Terminal Macro Global v3.2")
st.markdown("---")

# 📥 CONFIGURACIÓN DE TU PORTAFOLIO REAL DE ACCIONES (EQUITIES)
MI_PORTAFOLIO = {
    "NVDA": 50,
    "TSLA": 20,
    "OXY": 100,
    "JPM": 15,
    "MSFT": 10,
    "AAPL": 10,
    "AMZN": 15
}

# 🗺️ ESTRUCTURA BROAD-MARKET UNIFICADA
ESTRUCTURA_MERCADO = {
    "🚀 EQUITIES & BIG TECH": ["NVDA", "TSLA", "MSFT", "AAPL", "AMZN", "GOOGL"],
    "📦 ETFs & BROAD MARKET": ["SPY", "QQQ", "IWM"],
    "🧱 COMMODITIES CRÍTICOS": ["CL=F", "GC=F"],  # Petróleo Crudo y Oro Spot
    "📉 BONDS & RENDIMIENTOS": ["^TNX", "TLT"]     # Tasa de Bonos 10Y y ETF de Bonos Largos
}

NOMBRES_ACTIVOS = {
    "CL=F": "Petróleo Crudo", "GC=F": "Oro Spot",
    "^TNX": "US 10Y Yield", "TLT": "iShares +20Y Bond",
    "SPY": "S&P 500 ETF", "QQQ": "Nasdaq-100 ETF", "IWM": "Russell 2000 ETF"
}

# CACHÉ OPTIMIZADO DE 15 SEGUNDOS CON BUFFER DE SEGURIDAD HISTÓRICA
@st.cache_data(ttl=15)
def obtener_datos_globales():
    búfer = {}
    todos_los_tickers = set([t for lista in ESTRUCTURA_MERCADO.values() for t in lista])
    
    for ticker in todos_los_tickers:
        try:
            t_obj = yf.Ticker(ticker)
            # Solicitamos 5 días para evitar huecos de datos durante cierres o fines de semana
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
            time.sleep(0.1)  # Descarga ultra rápida y segura
        except Exception:
            búfer[ticker] = {"price": 0.0, "change": 0.0}
            
    return búfer

# Panel Control Remoto Lateral
st.sidebar.header("🕹️ MÓDULO DE CONTROL M82")
st.sidebar.markdown("**Estatus PR #1:** 🛠️ Refactorizado")
st.sidebar.markdown("**Motor Feed:** 🦅 Sincronizado")
if st.sidebar.button("🔄 Sincronizar Todo"):
    st.cache_data.clear()
    st.rerun()

datos_vivos = obtener_datos_globales()

# --- NÚCLEO MATEMÁTICO BLINDADO DE BALANCE ---
valor_total_portafolio = 0.0
cambio_diario_estimado = 0.0

for ticker, cantidad in MI_PORTAFOLIO.items():
    info_ticker = datos_vivos.get(ticker, {"price": 0.0, "change": 0.0})
    p = info_ticker["price"]
    c = info_ticker["change"]
    
    # Exclusión táctica: Aseguramos que solo sume si el precio es real y consistente
    if p > 0 and ticker != "^TNX":
        valor_posicion = p * cantidad
        valor_total_portafolio += valor_posicion
        cambio_diario_estimado += (valor_posicion * (c / 100))

# --- DESPLIEGUE DEL BALANCE NETO CORPORATIVO ---
st.markdown("### 🏦 VALORACIÓN DE ACTIVOS PROPIETARIOS")
p_col1, p_col2 = st.columns(2)
with p_col1:
    if valor_total_portafolio > 0:
        st.metric(label="💰 VALOR NETO EQUITIES EN VIVO", value=f"${valor_total_portafolio:,.2f} USD")
    else:
        st.warning("🔄 Sincronizando balance con Wall Street...")
with p_col2:
    st.metric(
        label="📈 P&L FLOTANTE ESTIMADO DEL DÍA", 
        value=f"${cambio_diario_estimado:+,.2f} USD",
        delta="Cálculo neto ponderado"
    )
st.markdown("---")

# --- COMPILACIÓN VISUAL ADAPTATIVA ---
for sector, tickers in ESTRUCTURA_MERCADO.items():
    st.header(sector)
    cols = st.columns(len(tickers))
    datos_tabla = []
    
    for i, ticker in enumerate(tickers):
        info_ticker = datos_vivos.get(ticker, {"price": 0.0, "change": 0.0})
        price = info_ticker["price"]
        change = info_ticker["change"]
        
        nombre_legible = NOMBRES_ACTIVOS.get(ticker, ticker)
        label_visual = f"🔥 {ticker}" if ticker == "NVDA" else ticker
        
        # Formatear visualmente según naturaleza del activo (Bono % vs Moneda USD)
        is_bond = (ticker == "^TNX")
        val_str = f"{price:.2f}%" if is_bond else f"${price:.2f}"
        
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
                    "Cotización": val_str,
                    "Variación": f"{change:.2f}%",
                    "Estatus": tenencia_str
                })
            else:
                st.metric(label=label_visual, value="Cargando...", delta="0.00%")
                st.caption(f"⚠️ {nombre_legible} en espera")

    if datos_tabla:
        df = pd.DataFrame(datos_tabla)
        st.dataframe(df, hide_index=True, use_container_width=True)
    st.markdown("---")

st.caption("M82 Sovereign Core Terminal v3.2 • Stable Pull Request Multi-Asset Version.")
