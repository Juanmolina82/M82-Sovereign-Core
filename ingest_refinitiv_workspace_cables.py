#!/usr/bin/env python3
import sqlite3, os, json, datetime

BASE_DIR = os.path.expanduser("~/M82")
DB_PATH = os.path.join(BASE_DIR, "m82_database.db")

def main():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    now = datetime.datetime.now().isoformat()

    # Listado de cables extraídos de M82 Wire Workspace (M82_MACRO)
    cables = [
        {
            "source": "M82_WIRE_WORKSPACE_M82_MACRO",
            "category": "VEN_BONDS_RALLY",
            "headline": "Venezuela debt rally sees eyes on higher recovery price",
            "gprk": 98.5,
            "risk_score": 9.2,
            "meta": {
                "entity": "REPUBLIC OF VENEZUELA",
                "duns": "003011988",
                "lei": "549300V988L3E4928A43",
                "topic": "Debt Recovery Price Increase"
            }
        },
        {
            "source": "M82_WIRE_WORKSPACE_M82_MACRO",
            "category": "VEN_DEBT_RESTRUCTURING",
            "headline": "Lazard offers Venezuela debt restructuring advice",
            "gprk": 97.8,
            "risk_score": 8.9,
            "meta": {
                "advisor": "Lazard",
                "target": "Sovereign & PDVSA Bonds",
                "status": "Proposal / Active Talks"
            }
        },
        {
            "source": "M82_WIRE_WORKSPACE_M82_MACRO",
            "category": "VEN_BONDS_SHORT_SQUEEZE",
            "headline": "Venezuela's default bonds rally on debt restructuring prospect",
            "gprk": 99.1,
            "risk_score": 9.8,
            "meta": {
                "catalyst": "Restructuring Prospect",
                "action": "Short Squeeze / Secondary Market Trading"
            }
        },
        {
            "source": "M82_WIRE_WORKSPACE_M82_MACRO",
            "category": "CVX_VENEZUELA_OPERATIONS",
            "headline": "Chevron / Venezuela Joint Ventures for Oil Investment & Production Continuity",
            "gprk": 96.4,
            "risk_score": 7.5,
            "meta": {
                "ticker": "CVX.N",
                "sector": "Integrated Oil & Gas",
                "joint_ventures": "Petropiar, Petroboscán",
                "status": "Operational Continuity"
            }
        },
        {
            "source": "M82_WIRE_WORKSPACE_M82_MACRO",
            "category": "VEN_DIPLOMACY_MINING",
            "headline": "Maduro confirma renovadas relaciones con EE.UU. en minería y reestructuración fiscal con Delcy Rodríguez",
            "gprk": 98.0,
            "risk_score": 9.0,
            "meta": {
                "key_figures": ["Nicolás Maduro", "Delcy Rodríguez"],
                "focus": "Mining & Debt Overhaul"
            }
        }
    ]

    print("================================================================================")
    print(" 🏛 INGESTA DE CABLES M82_WIRE WORKSPACE A M82 DATABASE")
    print("================================================================================")

    for item in cables:
        # Inserción en macro_dosier
        c.execute("""
            INSERT INTO macro_dosier (source, category, headline, gprk_index, yield_10y_delta, oil_spread_impact, risk_score, metadata_json)
            VALUES (?, ?, ?, ?, 0.02, 1.25, ?, ?)
        """, (
            item["source"],
            item["category"],
            item["headline"],
            item["gprk"],
            item["risk_score"],
            json.dumps(item["meta"])
        ))

        # Inserción en m82_multi_stream para despacho
        c.execute("""
            INSERT OR IGNORE INTO m82_multi_stream (daemon_source, headline, status, timestamp)
            VALUES (?, ?, 'DISPATCHED', ?)
        """, (
            "m82_refinitiv_workspace_daemon",
            f"[{item['category']}] {item['headline']}",
            now
        ))

        print(f" ✅ Processed: [{item['category']}] -> {item['headline'][:60]}...")

    conn.commit()
    conn.close()

    print("================================================================================")
    print(" 🚀 Todos los cables se registraron exitosamente en SQLite (m82_database.db).")
    print("================================================================================")

if __name__ == "__main__":
    main()
