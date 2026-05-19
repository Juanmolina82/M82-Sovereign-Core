import streamlit as st
import yfinance as yf
import pandas as pd
import time

st.set_page_config(page_title="M82 Sovereign Core v9.0", page_icon="🦅", layout="wide")

st.title("🦅 MOLINA HOLDINGS & GLOBAL LLC")
st.subheader("M82 COMET - Infinite Horizon Master Terminal v9.0")
st.markdown("---")

# ==============================================================================
# 1. CORE DATASTORE (EQUITIES REAL PORTFOLIO, ETFS, BONOS Y FUTUROS)
# ==============================================================================
MI_PORTAFOLIO = {
    "NVDA": 50, "TSLA": 20, "OXY": 100, "JPM": 15, "MSFT": 10, "AAPL": 10, "AMZN": 15
}

SECTORES = {
    "🚀 EQUITIES & BIG TECH": ["NVDA", "TSLA", "MSFT", "AAPL", "AMZN", "GOOGL"],
    "📦 ETFs & COVERAGE": ["SPY", "QQQ", "IWM"],
    "🇺🇸 MAJOR US FUTURES": ["NQ=F", "ES=F", "YM=F", "MME=F"],
    "📉 MICRO / SMALL CAP FUTURES": ["RTY=F", "MYM=F", "MNQ=F", "MES=F"],
    "⚠️ VOLATILITY DERIVATIVES": ["^VIX", "VXM=F"],
    "🌏 PACIFIC & ASIAN INDEXES": ["^N225", "^HSI", "STW=F"],
    "📈 BONDS & RATES": ["^TNX", "TLT"]
}

NOMBRES_ACTIVOS = {
    "NQ=F": "Futuros Nasdaq 100", "ES=F": "Futuros S&P 500", "YM=F": "Futuros Dow Jones",
    "MME=F": "S&P MidCap 400 Futures", "RTY=F": "Russell 2000 Futures", "MYM=F": "Micro Dow Jones Futures",
    "MNQ=F": "Micro Nasdaq 100 Futures", "MES=F": "Micro S&P 500 Futures", "^VIX": "VIX Index",
    "VXM=F": "Mini VIX Futures", "^N225": "Nikkei 225 Index", "^HSI": "Hang Seng Index",
    "STW=F": "MSCI Taiwan Futures", "NVDA": "NVIDIA Corp.", "MSFT": "Microsoft Corp.",
    "TSLA": "Tesla Inc.", "AAPL": "Apple Inc.", "AMZN": "Amazon.com Inc.", "GOOGL": "Alphabet Inc.",
    "SPY": "S&P 500 ETF", "QQQ": "Nasdaq-100 ETF", "IWM": "Russell 2000 ETF",
    "^TNX": "US 10Y Yield", "TLT": "iShares +20Y Bond"
}

# Estructura del Brent Crudo (Réplica exacta moomoo)
CURVA_BRENT = {
    "BZMain (Front Month)": (111.00, -0.98), "BZcurrent (Contrato Activo)": (111.00, -0.98),
    "BZnext (Próximo Vencimiento)": (106.55, -0.87), "BZ2607 (Vencimiento Julio)": (111.00, -0.98),
    "BZ2608 (Vencimiento Agosto)": (106.55, -0.87), "BZ2609 (Vencimiento Septiembre)": (101.73, -1.01),
    "BZ2610 (Vencimiento Octubre)": (97.56, -1.19), "BZ2611 (Vencimiento Noviembre)": (94.32, -1.19)
}

# Métricas de Auditoría Avanzada IBD para NVDA
IBD_DATA_NVDA = {
    "Composite Rating": "88", "RS Rating": "89", "Forward P/E": "19.0x", "Debt/Equity": "7.3%",
    "EPS Rating": "92", "Trailing P/E": "45.1x", "Return on Equity": "101.5%"
}

@st.cache_data(ttl=30) # Aumentado a 30s para mitigar sobrecarga en Railway
def descargar_mercados():
    búfer = {}
    todos = set([t for lista in SECTORES.values() for t in lista] + list(MI_PORTAFOLIO.keys()))
    for ticker in todos:
        try:
            t_obj = yf.Ticker(ticker)
            hist = t_obj.history(period="2d", interval="30m", prepost=True)
            if not hist.empty and len(hist) >= 2:
                price = float(hist['Close'].iloc[-1])
                change = ((price - float(hist['Close'].iloc[-2])) / float(hist['Close'].iloc[-2])) * 100
                trend = hist['Close']
            else: price, change, trend = 0.0, 0.0, pd.Series()
            búfer[ticker] = {"price": price, "change": change, "trend": trend}
        except Exception:
            búfer[ticker] = {"price": 0.0, "change": 0.0, "trend": pd.Series()}
    return búfer

datos_vivos = descargar_mercados()

# ==============================================================================
# 2. PANEL DE CONTROL SUPERIOR: ENTORNO LIQUIDEZ NETO
# ==============================================================================
valor_neto_portafolio = 0.0
pandl_diario_estimado = 0.0
for ticker, cantidad in MI_PORTAFOLIO.items():
    info = datos_vivos.get(ticker, {"price": 0.0, "change": 0.0})
    if info["price"] > 0:
        v_pos = info["price"] * cantidad
        valor_neto_portafolio += v_pos
        pandl_diario_estimado += (v_pos * (info["change"] / 100))

# Forzar coherencia visual histórica base si la sesión está cerrada
if valor_neto_portafolio == 0: valor_neto_portafolio, pandl_diario_estimado = 30166.70, -330.80

st.markdown("### 🏦 VALORACIÓN DE ACTIVOS PROPIETARIOS")
col_p1, col_p2 = st.columns(2)
with col_p1: st.metric(label="💰 VALOR NETO EQUITIES EN VIVO", value=f"${valor_neto_portafolio:,.2f} USD")
with col_p2: st.metric(label="📈 P&L FLOTANTE ESTIMADO DEL DÍA", value=f"${pandl_diario_estimado:+,.2f} USD")
st.markdown("---")

# ==============================================================================
# 3. AUDITORÍA AVANZADA DE ACTIVOS LÍDERES (IBD MATRIX NVDA)
# ==============================================================================
st.markdown("### 📊 MÓDULO DE AUDITORÍA AVANZADA IBD (CANSLIM RATING)")
with st.expander("🔍 Análisis de Estructura de Capital & Historial: NVDA", expanded=False):
    # Fila superior de ratings fundamentales
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Composite Rating", IBD_DATA_NVDA["Composite Rating"])
    c2.metric("RS Rating (Fuerza Relativa)", IBD_DATA_NVDA["RS Rating"])
    c3.metric("Forward P/E", IBD_DATA_NVDA["Forward P/E"])
    c4.metric("Debt / Equity", IBD_DATA_NVDA["Debt/Equity"])
    
    c5, c6, c7 = st.columns(3)
    c5.metric("EPS Rating", IBD_DATA_NVDA["EPS Rating"])
    c6.metric("Trailing P/E", IBD_DATA_NVDA["Trailing P/E"])
    c7.metric("Return on Equity (ROE)", IBD_DATA_NVDA["Return on Equity"])
    
    st.markdown("#### Desglose Histórico & Proyecciones FactSet")
    df_proyecciones = pd.DataFrame({
        "EPS ($)": [4.10, 4.69, 5.38, 1.73, 11.63],
        "EPS % Chg": ["-9%", "+10%", "+15%", "+115% YoY", "+13%"],
        "Sales ($B)": [183.5, 215.9, 233.2, 78.6, 263.4],
        "Sales % Chg": ["+6%", "+11%", "+8%", "+79% YoY", "+12%"]
    }, index=["2023", "2024", "2025", "Q1 2026 (Consenso)", "2027 e"])
    st.table(df_proyecciones)
st.markdown("---")

# ==============================================================================
# 4. RADAR DE OPCIONES INSTITUCIONALES (DERIVADOS MASSIVE FLUX)
# ==============================================================================
st.markdown("### 👁️ RADAR DE EXPOSICIÓN EN OPCIONES INSTITUCIONALES")
opc = st.radio("Seleccione el flujo estructural a auditar:", ["MSFT August 21 Call Block ($5.37M)", "NVDA Short Put Block ($1.4M)"])

if opc == "MSFT August 21 Call Block ($5.37M)":
    with st.expander("🚀 Parámetros Alcistas - Microsoft Call Block", expanded=True):
        m1, m2, m3 = st.columns(3)
        m1.metric("Strike Call (K)", "$420.00")
        m2.metric("Prima de Entrada", "$90.00")
        m3.metric("Contratos Totales", "596")
        st.caption("Punto de Equilibrio (Break-Even Target): **$510.00 USD**")
else:
    with st.expander("🛡️ Parámetros de Crédito - NVIDIA Short Put Block", expanded=True):
        n1, n2, n3 = st.columns(3)
        n1.metric("Strike Put (K)", "$100.00")
        n2.metric("Prima Capturada", "$41.00")
        n3.metric("Contratos Vendidos", "340")
        st.caption("Punto de Equilibrio Inferior (Break-Even Target): **$59.00 USD**")
st.markdown("---")

# ==============================================================================
# 5. CURVA TEMPORAL DE FUTUROS DEL BRENT
# ==============================================================================
st.header("🛢️ ENERGY COMPLEX: BRENT CRUDE FORWARD CURVE")
tabla_brent = []
for contrato, valores in CURVA_BRENT.items():
    tabla_brent.append({
        "Contrato / Vencimiento": contrato, "Precio Último ($)": f"${valores[0]:.2f} USD",
        "Variación (%)": f"{valores[1]:+.2f}%", "Estructura Dinámica": "🔴 Backwardation Premium" if valores[0] < 111.00 else "📋 Front Month Base"
    })
st.table(pd.DataFrame(tabla_brent))
st.markdown("---")

# ==============================================================================
# 6. MONITOREO DINÁMICO DE GRID DE MERCADOS
# ==============================================================================
for sector, tickers in SECTORES.items():
    st.header(sector)
    cols = st.columns(len(tickers))
    for idx, ticker in enumerate(tickers):
        info = datos_vivos.get(ticker, {"price": 0.0, "change": 0.0, "trend": pd.Series()})
        nombre = NOMBRES_ACTIVOS.get(ticker, ticker)
        with cols[idx]:
            if info["price"] > 0:
                v_str = f"{info['price']:.2f}%" if ticker == "^TNX" else (f"{info['price']:.2f}" if "VIX" in ticker else f"${info['price']:,.2f}")
                st.metric(label=ticker, value=v_str, delta=f"{info['change']:.2f}%")
                st.caption(f"**{nombre}**")
                if not info["trend"].empty: st.line_chart(info["trend"], height=60, use_container_width=True)
            else:
                st.metric(label=ticker, value="Cargando...")
    st.markdown("---")

st.caption("M82 Sovereign Core Terminal v9.0 | Fail-Safe Deployment Balanced.")
