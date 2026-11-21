#!/usr/bin/env python3
import sys
sys.path.insert(0, "/home/m82/M82" if False else "/data/data/com.termux/files/home/M82")
# Ajuste automático de path Termux
import os
sys.path.insert(0, os.path.expanduser("~/M82"))
from m82_dossier_engine import M82DossierEngine

engine = M82DossierEngine()

events = [
    {
        "source": "LSEG_QCOM",
        "category": "EARNINGS_SEMICONDUCTOR",
        "headline": "Qualcomm Q4 FY26: Revenue 10.44B -7% YoY, EPS 2.17 -28%, Auto +89%, Data Center Target 5B FY27, AWS up to 60B 10Y",
        "tag": "v61.0.51-A-QCOM-Q4-20261105",
        "event_trigger": "QCOM_Q4_20261105",
        "alpha_score": 1.00,
        "sentiment": 0.45,
        "asset_impact": "QCOM_DATACENTER_AUTO",
        "metadata": {"revenue_b": 10.44, "eps": 2.17, "auto_q_b": 2.0, "auto_yoy": 0.89, "dc_target_fy27_b": 5.0, "aws_10y_b": 60.0, "cowen_target": 185, "after_hours": -0.065, "var": 1.68}
    },
    {
        "source": "LSEG_SPACEX",
        "category": "TELECOM_INFRASTRUCTURE",
        "headline": "SpaceX selects Qualcomm Dragonwing QRU100 QDU100 for Starlink Mobile 5G terrestrial, 64T64R, tens of thousands sites from 2027, spectrum 19.6B EchoStar",
        "tag": "v61.0.51-A-SPACEX-QCOM-5G-20261105",
        "event_trigger": "SPACEX_QCOM_5G_20261105",
        "alpha_score": 1.00,
        "sentiment": 0.72,
        "asset_impact": "SPACEX_QCOM_5G_INFRA",
        "metadata": {"spectrum_b": 19.6, "connectivity_q3_b": 5.2, "connectivity_yoy": 0.69, "op_margin": 0.45, "valuation_t": 1.85, "spcx_price": 133.52, "var": 1.68}
    },
    {
        "source": "LSEG_GOLDMAN",
        "category": "MARKET_SENTIMENT",
        "headline": "Goldman Sachs: AI Trade Sold to Death, Micro Fundamentals Strong, Positioning Healthier, Election Uncertainty Reduced",
        "tag": "v61.0.51-A-GOLDMAN-AI-SOLD-TO-DEATH-20261105",
        "event_trigger": "GOLDMAN_AI_SOLD_TO_DEATH_20261105",
        "alpha_score": 0.95,
        "sentiment": 0.60,
        "asset_impact": "AI_SENTIMENT_CLEANUP",
        "metadata": {"source": "Goldman Privorotsky", "var": 1.68}
    },
]

for e in events:
    ok = engine.ingest_event(
        source=e["source"],
        category=e["category"],
        headline=e["headline"],
        tag=e["tag"],
        event_trigger=e["event_trigger"],
        alpha_score=e["alpha_score"],
        sentiment=e["sentiment"],
        asset_impact=e["asset_impact"],
        metadata=e["metadata"]
    )
    print(f"{e['tag']} -> {'SEALED' if ok else 'FAILED'}")
