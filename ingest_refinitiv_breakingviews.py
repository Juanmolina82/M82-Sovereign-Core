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

breakingviews_signals = [
    {
        "daemon": "m82_sovereign_debt_risk_daemon.py",
        "desk": "MACRO_DESK",
        "category": "CHINA_DEBT_EXPORT_1.5T",
        "headline": "China's next big export could be 1.5 trillion USD of debt",
        "risk_score": 9.7,
        "gprk": 96.8,
        "meta": {"amount_usd_t": 1.5, "origin": "China", "type": "Sovereign/Corporate Debt"}
    },
    {
        "daemon": "m82_vc_ai_unicorns_daemon.py",
        "desk": "TECH_DESK",
        "category": "ANTHROPIC_2T_MOONSHOT",
        "headline": "Anthropic's 2 trillion USD goal is AI's biggest moonshot",
        "risk_score": 9.8,
        "gprk": 94.2,
        "meta": {"target_valuation_usd_t": 2.0, "sector": "Frontier AI", "player": "Anthropic"}
    },
    {
        "daemon": "m82_sovereign_debt_risk_daemon.py",
        "desk": "BANKING_DESK",
        "category": "UBS_SWITZERLAND_EXIT_RISK",
        "headline": "How and why UBS could leave Switzerland amid capital requirements pressure",
        "risk_score": 9.5,
        "gprk": 91.0,
        "meta": {"entity": "UBS", "jurisdiction_risk": "Switzerland", "driver": "Capital Rules"}
    },
    {
        "daemon": "m82_pe_megafunds_daemon.py",
        "desk": "PE_DESK",
        "category": "NUBANK_MONZO_FINTECH_MA",
        "headline": "Why a NuBank-Monzo deal could make financial sense for global expansion",
        "risk_score": 9.1,
        "gprk": 85.5,
        "meta": {"targets": ["NuBank", "Monzo"], "sector": "Neobanking M&A"}
    }
]

print("================================================================================")
print(" 📡 INGESTIA BREAKINGVIEWS M82_WIRE WORKSPACE // NODO CHARALLAVE")
print("================================================================================")

for sig in breakingviews_signals:
    c.execute("""
        INSERT INTO macro_dosier (source, category, headline, gprk_index, yield_10y_delta, oil_spread_impact, risk_score, metadata_json)
        VALUES (?, ?, ?, ?, 0.03, 0.90, ?, ?)
    """, (sig["daemon"], sig["category"], sig["headline"], sig["gprk"], sig["risk_score"], json.dumps(sig["meta"])))

    c.execute("""
        INSERT OR IGNORE INTO m82_multi_stream (daemon_source, headline, status, timestamp)
        VALUES (?, ?, 'DISPATCHED', ?)
    """, (sig["daemon"], sig["headline"], now))

    print(f" 🚨 [RISK {sig['risk_score']}] {sig['desk']} -> {sig['category']}")
    print(f"    └─> {sig['headline']}")

conn.commit()

# Render de Tarjeta HUD específica: China $1.5T Debt vs Anthropic $2T Target
plt.style.use('dark_background')
fig, ax = plt.subplots(figsize=(10, 5.5), dpi=200)
fig.patch.set_facecolor('#0a0d12')
ax.set_facecolor('#0f141d')

metrics = ['UBS Swiss Assets', 'China Export Debt', 'Anthropic Target', 'PE Dry Powder Global']
values = [1600.0, 1500.0, 2000.0, 2008.2]  # USD $B

y_pos = np.arange(len(metrics))
bars = ax.barh(y_pos, values, color='#00e5ff', edgecolor='#76ff03', alpha=0.85, height=0.6)

ax.set_yticks(y_pos)
ax.set_yticklabels(metrics, fontsize=9, fontweight='bold', color='#e0e0e0')
ax.set_xlabel('Magnitud Financiera ($B USD)', fontsize=10, fontweight='bold', color='#00e5ff')
ax.set_title('M82 MACRO DOSIER // BREAKINGVIEWS CONVERGENCE ANALYSIS', fontsize=11, fontweight='bold', color='#76ff03', pad=12)

for bar in bars:
    w = bar.get_width()
    ax.text(w + 25.0, bar.get_y() + bar.get_height()/2, f'${w:,.1f}B', va='center', ha='left', fontsize=8, fontweight='bold', color='#ffffff')

ax.set_xlim(0, 2500)
ax.grid(True, linestyle='--', alpha=0.2, color='#00e5ff')
plt.tight_layout()

hud_bv_path = os.path.join(BASE_DIR, "hud_breakingviews_analysis.png")
plt.savefig(hud_bv_path, facecolor=fig.get_facecolor(), edgecolor='none')
plt.close()

conn.close()

print("\n  ✓ HUD Card 'hud_breakingviews_analysis.png' renderizada exitosamente.")
print("  ✓ RegistroSQLite y Multi-stream blindados.")
print("================================================================================")
