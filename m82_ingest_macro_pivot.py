#!/usr/bin/env python3
import os
import sys

sys.path.insert(0, os.path.expanduser("~/M82"))
from m82_dossier_engine import M82DossierEngine

engine = M82DossierEngine()

meta_pivot = {
    "operation": "ECONOMIC_OUTCAST",
    "us_policy": "PRICES_NOT_WAR",
    "target_asset": "MEREY_16",
    "target_price_bbl": 110.0,
    "citi_escrow_b": 200.0,
    "var": 1.68,
    "status": "BUNKER_MODE_030X_LOCK"
}

ok = engine.ingest_event(
    source="M82_SOVEREIGN_CORE",
    category="GEOPOLITICAL_ENERGY_PIVOT",
    headline="Operation Economic Outcast + #DealWithMCM: Atlantic Heavy Crude Substitution via MCM Witness Protocol",
    tag="v61.0.51-A-MACRO-PIVOT-20261105",
    event_trigger="M82_ATLANTIC_CRUDE_PIVOT_20261105",
    alpha_score=1.00,
    sentiment=0.99,
    asset_impact="MEREY16_PADD3_SUBSTITUTION",
    metadata=meta_pivot
)

print(f"PIVOT INGESTION -> {'SEALED' if ok else 'FAILED'}")
