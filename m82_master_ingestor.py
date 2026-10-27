import json
import sqlite3
import hashlib
from datetime import datetime
from core_ingestor import ingest_signal

m82_macro_signals = [
    # 1. Telemetría de Commodities y Curvas Spreads (Imagen 18)
    {
        "source": "M82 Wire/COMMODITIES",
        "category": "ENERGIA_COMMODITIES",
        "asset_class": "BRENT_WTI_HENRYHUB",
        "risk_score": 8.5,
        "headline": "Curvas de volatilidad y spreads en BRENT, WTI y Henry Hub impactan márgenes NAV regional",
        "payload": {
            "entity": "Energy Benchmarks",
            "drivers": ["Brent Crude", "NYMEX Light Sweet", "Henry Hub Gas"],
            "impact": "HIGH_VOLATILITY"
        }
    },
    # 2. Proyecto Gas Offshore Eni / Repsol Venezuela (Imágenes 18, 19)
    {
        "source": "M82 Wire/ENI_REPSOL",
        "category": "GAS_ENERGIA",
        "asset_class": "CARDON_IV_VEN",
        "risk_score": 8.7,
        "headline": "Eni y Repsol consolidan exportación offshore de gas natural del campo Perla a 550 MMcf/d",
        "payload": {
            "entity": "ENI S.p.A. / Repsol S.A.",
            "field": "Perla (Cardón IV)",
            "output": "550 MMcf/d",
            "impact": "HIGH_STRATEGIC_ASSET"
        }
    },
    # 3. Transacciones Offshore Globales M&A (Imagen 19 - Ithaca / Delek / Suncor)
    {
        "source": "M82 Wire/ITHACA_DELEK",
        "category": "MA_ENERGIA",
        "asset_class": "OFFSHORE_GLOBAL",
        "risk_score": 7.9,
        "headline": "Ithaca Energy / Delek adquiren portafolio offshore convencional de Suncor en $1.0B+",
        "payload": {
            "buyer": "Ithaca Energy / Delek Group",
            "seller": "Suncor Energy Inc",
            "deal_value_usd": "1.0 Billion+",
            "type": "Offshore Conventional Assets"
        }
    },
    # 4. Proyección Petrobras y Refinación US (Imagen 19 - Marathon Petroleum)
    {
        "source": "M82 Wire/MACRO_LATAM",
        "category": "PETROLEO_REFINACION",
        "asset_class": "LATAM_US_CRUDE",
        "risk_score": 7.5,
        "headline": "Petrobras amplía meta pre-salt a 2028 mientras Marathon Petroleum ajusta capacidad de refinación",
        "payload": {
            "entities": ["Petrobras", "Marathon Petroleum"],
            "trend": "Upstream Expansion & Midstream Margin Focus",
            "impact": "BALANCED"
        }
    }
]

def run_m82_integration():
    print("==================================================")
    print("   M82 DOSSIER MACRO ENGINE - INGESTA DE TELEMETRÍA")
    print("==================================================")
    for signal in m82_macro_signals:
        ingest_signal(
            source=signal["source"],
            category=signal["category"],
            asset_class=signal["asset_class"],
            risk_score=signal["risk_score"],
            headline=signal["headline"],
            payload_dict=signal["payload"]
        )
    print("\n[M82 INTEGRACIÓN] Ingesta máster finalizada con éxito.")

if __name__ == "__main__":
    run_m82_integration()
