import streamlit as st
import yfinance as yf
import pandas as pd
import time

st.set_page_config(page_title="M82 Sovereign Core v4.5", page_icon="🦅", layout="wide")

st.title("🦅 MOLINA HOLDINGS & GLOBAL LLC")
st.subheader("M82 COMET - Fundamental & Performance Terminal v4.5")
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

# 🗺️ MATRIZ BROAD-MARKET UNIFICADA
ESTRUCTURA_MERCADO = {
    "🚀 EQUITIES & BIG TECH": ["NVDA", "TSLA", "MSFT", "AAPL", "AMZN", "GOOGL"],
    "📦 ETFs & FUTURES": ["SPY", "QQQ", "IWM", "NQ=F"],
    "🧱 COMMODITIES CRÍTICOS": ["CL=F", "GC=F", "NG=F", "SI=F"],
    "📉 BONDS & RATES": ["^TNX", "TLT"]
}

NOMBRES_ACTIVOS = {
    "CL=F": "Petróleo Crudo", "GC=F": "Oro Spot",
    "^TNX": "US 10Y Yield", "TLT": "iShares +20Y Bond",
    "SPY": "S&P 500 ETF", "QQQ": "Nasdaq-100 ETF", "IWM": "Russell 2000 ETF",
    "NQ=F": "Futuros Nasdaq-100", "NG=F": "Gas Natural", "SI=F": "Plata Spot"
}

# CACHÉ DE PRECIOS Y TENDENCIAS (15 SEGUNDOS)
@st.cache_data(ttl=15)
def obtener_datos_globales():
    búfer = {}
    todos_los_tickers = set([t for lista in ESTRUCTURA_MERCADO.values() for t in lista])
    
    for ticker in todos_los_tickers:
        try:
            t_obj = yf.Ticker(ticker)
            hist = t_obj.history(period="2d", interval="15m")
            
            if not hist.empty and len(hist) >= 2:
                daily_hist = t_obj.history(period="5d")
                price = float(daily_hist['Close'].iloc[-1])
                prev_close = float(daily_hist['Close'].iloc[-2])
                change = ((price - prev_close) / prev_close) * 100
                price_trend = hist['Close']
            else:
                price, change, price_trend = 0.0, 0.0, pd.Series()
                
            búfer[ticker] = {"price": price, "change": change, "trend": price_trend}
            time.sleep(0.05)
        except Exception:
            búfer[ticker] = {"price": 0.0, "change": 0.0, "trend": pd.Series()}
            
    return búfer

# CACHÉ ESTRATÉGICO PARA FUNDAMENTALES (LARGA DURACIÓN - 1 HORA PARA EVITAR BANEO DE API)
@st.cache_data(ttl=3600)
def obtener_fundamentales_portafolio(tickers):
    búfer_fun = {}
    for ticker in tickers:
        try:
            t_obj = yf.Ticker(ticker)
            info = t_obj.info
            
            búfer_fun[ticker] = {
                "trailing_eps": info.get("trailingEps", 0.0),
                "forward_eps": info.get("forwardEps", 0.0),
                "revenue_growth": info.get("quarterlyRevenueGrowth", 0.0) * 100 if info.get("quarterlyRevenueGrowth") else 0.0,
                "profit_margin": info.get("profitMargins", 0.0) * 100 if info.get("profitMargins") else 0.0,
                "pe_ratio": info.get("trailingPE", 0.0)
            }
            time.sleep(0.1)
        except Exception:
            búfer_fun[ticker] = {"trailing_eps": 0.0, "forward_eps": 0.0, "revenue_growth": 0.0, "profit_margin": 0.0, "pe_ratio": 0.0}
    return búfer_fun

# Interfaz Lateral Activa
st.sidebar.header("🕹️ MÓDULO DE CONTROL M82")
st.sidebar.markdown("**Estatus Fundamental:** 📊 Sincronizado")
if st.sidebar.button("🔄 Refrescar Terminal"):
    st.cache_data.clear()
    st.rerun()

datos_vivos = obtener_datos_globales()
datos_fundamentales = obtener_fundamentales_portafolio(list(MI_PORTAFOLIO.keys()))

# --- DETECCIÓN DE BALANCE FINANCIERO ---
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
    st.metric(label="📈 P&L FLOTANTE ESTIMADO DEL DÍA", value=f"${cambio_diario_estimado:+,.2f} USD")
st.markdown("---")

# ==============================================================================
# 🔥 NUEVA SECCIÓN M82: RADAR DE FUNDAMENTALES DE TU PORTAFOLIO (EPS & REVENUE)
# ==============================================================================
st.markdown("### 🔍 MONITOR DE VALORACIÓN & EARNINGS (PORTAFOLIO)")
tabla_fundamental = []
for ticker, cantidad in MI_PORTAFOLIO.items():
    f = datos_fundamentales.get(ticker, {"trailing_eps": 0.0, "forward_eps": 0.0, "revenue_growth": 0.0, "profit_margin": 0.0, "pe_ratio": 0.0})
    p_info = datos_vivos.get(ticker, {"price": 0.0})
    
    tabla_fundamental.append({
        "Ticker": ticker,
        "Precio Spot": f"${p_info['price']:.2f}" if p_info['price'] > 0 else "N/A",
        "P/E Ratio": f"{f['pe_ratio']:.2f}x" if f['pe_ratio'] > 0 else "N/A",
        "EPS Reciente (Trailing)": f"${f['trailing_eps']:.2f}",
        "EPS Proyectado (Forward)": f"${f['forward_eps']:.2f}",
        "Crecimiento Ingresos (YoY)": f"{f['revenue_growth']:+.2f}%",
        "Margen de Beneficio Neto": f"{f['profit_margin']:.2f}%"
    })

df_fun = pd.DataFrame(tabla_fundamental)
st.dataframe(df_fun, hide_index=True, use_container_width=True)
st.markdown("---")

# --- COMPILACIÓN SECTORIAL CON MINICHARTS DE MOMENTUM ---
for sector, tickers in ESTRUCTURA_MERCADO.items():
    st.header(sector)
    cols = st.columns(len(tickers))
    
    for i, ticker in enumerate(tickers):
        info_ticker = datos_vivos.get(ticker, {"price": 0.0, "change": 0.0, "trend": pd.Series()})
        price = info_ticker["price"]
        change = info_ticker["change"]
        trend = info_ticker["trend"]
        
        nombre_legible = NOMBRES_ACTIVOS.get(ticker, ticker)
        label_visual = f"🔥 {ticker}" if ticker == "NVDA" else ticker
        
        is_bond = (ticker == "^TNX")
        val_str = f"{price:.2f}%" if is_bond else f"${price:.2f}"
        
        with cols[i]:
            if price > 0:
                st.metric(label=label_visual, value=val_str, delta=f"{change:.2f}%")
                st.caption(f"**{nombre_legible}**")
                if not trend.empty:
                    st.line_chart(trend, height=70, use_container_width=True)
            else:
                st.metric(label=label_visual, value="Cargando...", delta="0.00%")
                st.caption(f"⚠️ {nombre_legible}")
    st.markdown("---")

st.caption("M82 Sovereign Core Terminal v4.5 PRO • Earnings Integration Engine.")
