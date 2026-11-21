#!/usr/bin/env python3
import sqlite3, os, datetime, json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

BASE_DIR = os.path.expanduser("~/M82")
DB_PATH = os.path.join(BASE_DIR, "m82_database.db")

conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

now = datetime.datetime.now().isoformat()

# 1. Inyección de Señales Extraídas de la Front Page de M82 Wire
news_signals = [
    {
        "daemon": "m82_lng_gas_global_daemon.py",
        "desk": "ENERGY_DESK",
        "category": "LNG_ALASKA_MEGA_DEAL",
        "headline": "Trump expected to announce $54 billion South Korea investment in Alaska LNG",
        "risk_score": 9.4,
        "gprk": 92.5,
        "meta": {"deal_size_usd_b": 54.0, "partners": ["US", "South Korea"], "target": "Alaska LNG"}
    },
    {
        "daemon": "m82_geopolitical_events_daemon.py",
        "desk": "GEOPOLITICS_DESK",
        "category": "US_IRAQ_PULLOUT_VACUUM",
        "headline": "US forces quit Iraq leaving potential security vacuum; Iran responds to Washington proposal",
        "risk_score": 9.8,
        "gprk": 98.9,
        "meta": {"region": "Middle East", "impact": "Oil Risk Premium High", "status": "US Withdrawal"}
    },
    {
        "daemon": "m82_treasury_bonds_daemon.py",
        "desk": "MACRO_DESK",
        "category": "AI_ARMS_SURGE_BONDS",
        "headline": "The $8 trillion arms surge fueling AI spooking bond yields and US credit markets",
        "risk_score": 9.6,
        "gprk": 95.0,
        "meta": {"ai_defense_capex_usd_t": 8.0, "market_effect": "Bond Yield Spikes"}
    },
    {
        "daemon": "m82_faja_orinoco_ep_daemon.py",
        "desk": "ENERGY_DESK",
        "category": "OPEC_POLICY_STEADY",
        "headline": "OPEC+ oil producers set to keep output targets steady at Sunday meeting",
        "risk_score": 9.1,
        "gprk": 88.0,
        "meta": {"opec_policy": "Hold Quotas", "crude_impact": "Neutral-Bullish"}
    }
]

print("================================================================================")
print(" 📡 INGESTIA DE COMUNICADOS M82_WIRE WORKSPACE // NODO CHARALLAVE")
print("================================================================================")

for sig in news_signals:
    # Registramos en macro_dosier
    c.execute("""
        INSERT INTO macro_dosier (source, category, headline, gprk_index, yield_10y_delta, oil_spread_impact, risk_score, metadata_json)
        VALUES (?, ?, ?, ?, 0.04, 1.20, ?, ?)
    """, (sig["daemon"], sig["category"], sig["headline"], sig["gprk"], sig["risk_score"], json.dumps(sig["meta"])))
    
    rec_id = c.lastrowid
    
    # Registramos en el multi-stream
    c.execute("""
        INSERT OR IGNORE INTO m82_multi_stream (daemon_source, headline, status, timestamp)
        VALUES (?, ?, 'DISPATCHED', ?)
    """, (sig["daemon"], sig["headline"], now))
    
    print(f" 🚨 [RISK {sig['risk_score']}] {sig['desk']} -> {sig['category']}")
    print(f"    └─> {sig['headline']}")

conn.commit()

# 2. Render de la Card HUD Macro ($8T AI Defense Capex vs Alaska LNG $54B)
plt.style.use('dark_background')
fig, ax = plt.subplots(figsize=(10, 5.5), dpi=200)
fig.patch.set_facecolor('#0a0d12')
ax.set_facecolor('#0f141d')

categories = ['Alaska LNG Deal', 'OPEC+ Target', 'AI Credit Risk', 'US Defense Capex']
amounts = [54.0, 120.0, 450.0, 8000.0]  # En $B USD

y_pos = np.arange(len(categories))
bars = ax.barh(y_pos, amounts, color='#ff1744', edgecolor='#76ff03', alpha=0.85, height=0.6)

ax.set_yticks(y_pos)
ax.set_yticklabels(categories, fontsize=9, fontweight='bold', color='#e0e0e0')
ax.set_xscale('log')  # Escala logarítmica por la magnitud del Capex
ax.set_xlabel('Escala de Impacto Monetario USD ($B USD Log Scale)', fontsize=10, fontweight='bold', color='#00e5ff')
ax.set_title('M82 MACRO DOSIER // TELEMETRÍA DE IMPACTO NOTICIOSO M82_WIRE', fontsize=11, fontweight='bold', color='#76ff03', pad=12)

for bar in bars:
    w = bar.get_width()
    ax.text(w * 1.15, bar.get_y() + bar.get_height()/2, f'${w:,.0f}B', va='center', ha='left', fontsize=8, fontweight='bold', color='#ffffff')

ax.grid(True, which="both", linestyle='--', alpha=0.2, color='#00e5ff')
plt.tight_layout()

hud_news_path = os.path.join(BASE_DIR, "hud_news_frontpage_refinitiv.png")
plt.savefig(hud_news_path, facecolor=fig.get_facecolor(), edgecolor='none')
plt.close()

conn.close()

print("\n  ✓ HUD Card 'hud_news_frontpage_refinitiv.png' generada exitosamente.")
print("  ✓ Base de datos SQLite y Multi-stream actualizados.")
print("================================================================================")
