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

calendar_signals = [
    {
        "daemon": "m82_treasury_bonds_daemon.py",
        "desk": "MACRO_DESK",
        "category": "US_CORE_PCE_INFLATION",
        "headline": "US Core PCE Index matches target at 2.6% YoY; Fed SOFR Swaps adjusting rate path",
        "risk_score": 9.4,
        "gprk": 92.0,
        "meta": {"indicator": "Core PCE YoY", "value": 2.6, "impact": "Fed Rate Cut Expectations"}
    },
    {
        "daemon": "m82_crypto_commodities_daemon.py",
        "desk": "ENERGY_DESK",
        "category": "EIA_CRUDE_INVENTORY_DRAW",
        "headline": "EIA Weekly Crude Stocks draw down by 0.451M barrels tightening energy spreads",
        "risk_score": 9.3,
        "gprk": 90.5,
        "meta": {"crude_draw_mbbl": -0.451, "gasoline_draw_mbbl": -1.25, "impact": "Bullish Energy"}
    },
    {
        "daemon": "m82_us_china_tariffs_daemon.py",
        "desk": "GEOPOLITICS_DESK",
        "category": "CHINA_CAIXIN_PMI_EXPANSION",
        "headline": "China Official Manufacturing PMI stabilizes at 50.1 signaling industrial floor",
        "risk_score": 8.9,
        "gprk": 87.4,
        "meta": {"pmi_actual": 50.1, "pmi_previous": 49.8, "region": "China"}
    },
    {
        "daemon": "m82_high_yield_credit_daemon.py",
        "desk": "CREDIT_DESK",
        "category": "US_JOBLESS_CLAIMS_STABILITY",
        "headline": "US Initial Jobless Claims steady at 218K maintaining labor market balance",
        "risk_score": 8.7,
        "gprk": 85.0,
        "meta": {"claims_k": 218, "trend": "Neutral"}
    }
]

print("================================================================================")
print(" 📡 INGESTIA DE CALENDARIO ECONÓMICO M82_WIRE // NODO CHARALLAVE")
print("================================================================================")

for sig in calendar_signals:
    c.execute("""
        INSERT INTO macro_dosier (source, category, headline, gprk_index, yield_10y_delta, oil_spread_impact, risk_score, metadata_json)
        VALUES (?, ?, ?, ?, -0.01, 1.05, ?, ?)
    """, (sig["daemon"], sig["category"], sig["headline"], sig["gprk"], sig["risk_score"], json.dumps(sig["meta"])))

    c.execute("""
        INSERT OR IGNORE INTO m82_multi_stream (daemon_source, headline, status, timestamp)
        VALUES (?, ?, 'DISPATCHED', ?)
    """, (sig["daemon"], sig["headline"], now))

    print(f" 🚨 [RISK {sig['risk_score']}] {sig['desk']} -> {sig['category']}")
    print(f"    └─> {sig['headline']}")

conn.commit()

# Render de Tarjeta HUD Económica (Core PCE vs Crude Inventories vs China PMI)
plt.style.use('dark_background')
fig, ax = plt.subplots(figsize=(10, 5.5), dpi=200)
fig.patch.set_facecolor('#0a0d12')
ax.set_facecolor('#0f141d')

indicators = ['China Mfg PMI', 'US Core PCE (YoY %)', 'EIA Crude Stocks (M bbl)', 'US 3M Bill Rate (%)']
values = [50.1, 2.6, -0.45, 2.00]

y_pos = np.arange(len(indicators))
colors = ['#76ff03' if v > 0 else '#ff1744' for v in values]
bars = ax.barh(y_pos, values, color=colors, edgecolor='#00e5ff', alpha=0.85, height=0.55)

ax.set_yticks(y_pos)
ax.set_yticklabels(indicators, fontsize=9, fontweight='bold', color='#e0e0e0')
ax.set_xlabel('Lectura Real de Mercado (M82 Wire Economic Monitor)', fontsize=10, fontweight='bold', color='#00e5ff')
ax.set_title('M82 MACRO DOSIER // ECONOMIC MONITOR METRICS (SEPT-OCT 2026)', fontsize=11, fontweight='bold', color='#76ff03', pad=12)

for bar in bars:
    w = bar.get_width()
    offset = 0.5 if w >= 0 else -1.8
    ax.text(w + offset, bar.get_y() + bar.get_height()/2, f'{w:.2f}', va='center', ha='left', fontsize=8, fontweight='bold', color='#ffffff')

ax.grid(True, linestyle='--', alpha=0.2, color='#00e5ff')
plt.tight_layout()

hud_cal_path = os.path.join(BASE_DIR, "hud_economic_calendar_monitor.png")
plt.savefig(hud_cal_path, facecolor=fig.get_facecolor(), edgecolor='none')
plt.close()

conn.close()

print("\n  ✓ HUD Card 'hud_economic_calendar_monitor.png' renderizada exitosamente.")
print("  ✓ Calendario Macroeconómico integrado en m82_database.db.")
print("================================================================================")
