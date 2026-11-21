import json
import sqlite3
import hashlib
from datetime import datetime
from core_ingestor import ingest_signal

signals_feed = [
    {
        "source": "M82 Wire/ENI.MI",
        "category": "GAS_ENERGIA",
        "asset_class": "CARDON_IV_VEN",
        "risk_score": 8.7,
        "headline": "Eni y Repsol consideran exportar gas natural del campo Perla costa afuera de Venezuela",
        "payload": {
            "entity": "ENI S.p.A. / Repsol",
            "field": "Perla (Cardón IV)",
            "action": "Gas Export Consideration",
            "market_impact": "HIGH_LIQUIDITY"
        }
    },
    {
        "source": "M82 Wire/ENI.MI",
        "category": "MACRO_FINANZAS",
        "asset_class": "EQUITY_LATAM",
        "risk_score": 7.4,
        "headline": "Eni consolida créditos de suministros y compensación de deudas operativas en LatAm",
        "payload": {
            "entity": "ENI S.p.A.",
            "region": "LATAM / VEN",
            "type": "Debt Offset / Receivables",
            "impact": "MEDIUM"
        }
    },
    {
        "source": "M82 Wire/YPF",
        "category": "LITIGIO_SOBERANO",
        "asset_class": "ARGENTINA_SOVEREIGN",
        "risk_score": 9.2,
        "headline": "Corte de EE.UU. mantiene sentencia contra Argentina por USD 16.100 millones en el caso YPF",
        "payload": {
            "entity": "República Argentina / YPF S.A.",
            "court": "US Court of Appeals",
            "amount_usd_bn": 16.1,
            "impact": "CRITICAL_SOVEREIGN_RISK"
        }
    },
    {
        "source": "M82 Wire/REP.MC",
        "category": "GAS_ENERGIA",
        "asset_class": "VENEZUELA_GAS",
        "risk_score": 8.1,
        "headline": "Proyecto de gas offshore de Repsol en Venezuela mantiene producción de 550 MMcfd",
        "payload": {
            "entity": "Repsol S.A.",
            "production_capacity": "550 MMcf/d",
            "field": "Perla",
            "impact": "STABLE_OUTPUT"
        }
    }
]

def process_refinitiv_feed():
    print("[M82_WIRE INGESTOR] Procesando lote extendido de telemetría...")
    for sig in signals_feed:
        ingest_signal(
            source=sig["source"],
            category=sig["category"],
            asset_class=sig["asset_class"],
            risk_score=sig["risk_score"],
            headline=sig["headline"],
            payload_dict=sig["payload"]
        )

if __name__ == "__main__":
    process_refinitiv_feed()
