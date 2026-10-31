import json
from core_ingestor import ingest_signal

signals_feed = [
    {
        "source": "M82 Wire/PETROBRAS",
        "category": "PETROLEO_OPEC",
        "asset_class": "LATAM_CRUDE",
        "risk_score": 7.8,
        "headline": "Petrobras proyecta expansión de producción de crudo a 2028 impulsada por activos Pre-Salt",
        "payload": {
            "entity": "Petróleo Brasileiro S.A.",
            "metric": "Crude Output Projection 2028",
            "impact": "MEDIUM_HIGH"
        }
    },
    {
        "source": "M82 Wire/COMMODITIES",
        "category": "ENERGIA_COMMODITIES",
        "asset_class": "BRENT_WTI_HENRYHUB",
        "risk_score": 8.3,
        "headline": "Volatilidad de spreads entre WTI, Brent y Henry Hub impacta valoraciones de NAV en LatAm",
        "payload": {
            "entity": "Energy Benchmark Commodities",
            "drivers": ["Henry Hub Gas Futures", "Brent Crude", "NYMEX Light Sweet"],
            "impact": "HIGH_VOLATILITY"
        }
    }
]

print("[INGESTOR] Procesando telemetría de gráficos y commodities...")
for sig in signals_feed:
    ingest_signal(
        source=sig["source"],
        category=sig["category"],
        asset_class=sig["asset_class"],
        risk_score=sig["risk_score"],
        headline=sig["headline"],
        payload_dict=sig["payload"]
    )
