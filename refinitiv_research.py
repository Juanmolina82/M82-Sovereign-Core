from core_ingestor import ingest_signal

research_feed = [
    {
        "source": "M82 Wire/RESEARCH_JEFFERIES",
        "category": "EQUITY_RESEARCH",
        "asset_class": "GLOBAL_ENERGY",
        "risk_score": 7.7,
        "headline": "Jefferies actualiza cobertura del sector Oil & Gas Midstream / Refining y valoraciones de margen",
        "payload": {
            "analyst_firm": "Jefferies",
            "coverage": "Oil & Gas / Midstream",
            "date": "2026-10-05"
        }
    },
    {
        "source": "M82 Wire/RESEARCH_CIBC",
        "category": "MACRO_RESEARCH",
        "asset_class": "UTILITIES_ENERGY",
        "risk_score": 7.4,
        "headline": "CIBC Capital Markets emite notas de actualización sobre Pipelines & Utilities globales",
        "payload": {
            "analyst_firm": "CIBC Capital Markets",
            "focus": "Power & Utilities / Commodity Price Sensitivity",
            "date": "2026-10-05"
        }
    },
    {
        "source": "M82 Wire/RESEARCH_PRICETARGET",
        "category": "EQUITY_RESEARCH",
        "asset_class": "ENERGY_HOLDINGS",
        "risk_score": 7.2,
        "headline": "PriceTarget Research reporta ajustes en métricas de valoración y target price para Clean Energy Holdings",
        "payload": {
            "analyst_firm": "PriceTarget Research",
            "metric": "Equity Target Price Review",
            "date": "2026-10-05"
        }
    }
]

print("[INGESTOR] Procesando nuevo lote de Research Reports...")
for item in research_feed:
    ingest_signal(
        source=item["source"],
        category=item["category"],
        asset_class=item["asset_class"],
        risk_score=item["risk_score"],
        headline=item["headline"],
        payload_dict=item["payload"]
    )
