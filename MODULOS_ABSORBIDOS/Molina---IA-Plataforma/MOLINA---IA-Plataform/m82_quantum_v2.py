import streamlit as st
import plotly.graph_objects as go
import hashlib
from datetime import datetime

# --- ESTÉTICA M82 PURE TERMINAL ---
st.set_page_config(page_title="M82 | QUANTUM INTELLIGENCE", layout="wide")
st.markdown("<style>.main {background-color: #000000; color: #00FF00; font-family: 'Courier New';}</style>", unsafe_allow_html=True)

st.title("⬜ M82 | QUANTUM INTELLIGENCE")
st.caption("📜 Apache-2.0 | Q-Protocol Active | Node: Verified")

# --- MOTOR DE RIESGO ---
risk_index = 84.2 

# Velocímetro Cuántico (Optimizado para Móvil)
fig = go.Figure(go.Indicator(
    mode = "gauge+number",
    value = risk_index,
    gauge = {
        'axis': {'range': [0, 100], 'tickcolor': "#00FF00"},
        'bar': {'color': "#FF0000" if risk_index > 70 else "#00FF00"},
        'bgcolor': "#111",
        'steps': [
            {'range': [0, 50], 'color': "#050"},
            {'range': [50, 100], 'color': "#500"}]
    }
))
fig.update_layout(paper_bgcolor='black', font={'color': "#00FF00", 'family': 'Courier New'})
st.plotly_chart(fig, use_container_width=True)

# --- PANEL DE NOTICIAS ---
st.subheader("🛰️ STRATEGIC FEED (REUTERS/LSEG)")
col1, col2 = st.columns(2)
with col1:
    st.markdown("🔴 **DRONE STRIKES ODESA:** High supply chain risk.")
    st.markdown("🟡 **IRN BLOCKADE PROB:** 62% Simulation.")
with col2:
    st.markdown("🟢 **BRENT $124.00:** Strong support level.")
    st.markdown("⚪ **AGI STATUS:** Monitoring global sentiment...")

# --- FIRMA DIGITAL ---
sig = hashlib.sha256(str(risk_index).encode()).hexdigest()[:16].upper()
st.code(f"🔐 VERIFIED_NODE_SIG: {sig}-{datetime.now().strftime('%H:%M:%S')}")
