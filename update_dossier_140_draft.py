#!/usr/bin/env python3
import json, os
from datetime import datetime

BASE_DIR = os.path.expanduser("~/M82")
DRAFT_FILE = os.path.join(BASE_DIR, "dossier_140_draft.json")

dossier_140_updated = {
    "dossier_id": 140,
    "status": "RESERVED_PENDING_G20_CONFIRMATION",
    "timestamp_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "topic": "STRUCTURAL_ENERGY_RENTS_OFFSHORE_DRAIN",
    "target_asset": "CVG Venalum / Bauxilum / Guri Energy Matrix",
    "risk_score": 8.5,
    "architectural_framework": "Structured Commercial Credit & Offtake Discount (Vicepresidencia / Min. Economía y Finanzas)",
    "thesis_core": {
        "mechanism": "Arbitraje de Estructura Contractual (Tolling Offshore vs. Retención Onshore)",
        "entity_counterparty": "Mercuria Energy Group Ltd (Dubai) / Heeney Capital JV",
        "value_capture_flow": [
            "1. Pre-financiamiento offshore de insumos críticos (alúmina, ánodos, coke) + CAPEX de celdas",
            "2. Estructuración de deuda comercial registrada como pasivo para la estatal (Venalum)",
            "3. Offtake fijado con descuento masivo sobre LME (15-30%) + Fee de estructuración offshore",
            "4. Absorción de la energía hundida del Guri (~$5-10/MWh) consumida localmente, valor monetizado en SPV Dubái/Zug",
            "5. Liquidación neta residual hacia el Tesoro Nacional (TGN) / Renta descontada en origen"
        ],
        "fiscal_impact": "Operación contable a pérdida/breakeven nacional; margen capturado fuera de jurisdicción SENIAT/TGN",
        "analog_vector": "Dossier #138 (Merey 16 STS Offtake) & ID 33 (Mercuria Refinitiv Dubai Validation)"
    },
    "houston_g20_policy_lever": "Exigencia de cláusula de reversión de margen onshore para condicionar licenciamiento/operatividad",
    "trigger_event": "Confirmation of 15,000 ton shipment or MOU disclosure at G20 Energy Summit Houston"
}

with open(DRAFT_FILE, "w") as f:
    json.dump(dossier_140_updated, f, indent=4)

print("================================================================================")
print(" 📝 DOSSIER #140 UPDATED IN LOCAL DRAFT (JSON ONLY)")
print("================================================================================")
print(f" 📂 File: {DRAFT_FILE}")
print(" 🔒 Database Status: m82_database.db INTACT / UNTOUCHED (IDs 28-33 Sealed)")
print("================================================================================")
