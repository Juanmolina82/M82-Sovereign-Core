import os, json, time

DATA_PATH = os.path.expanduser("~/M82/app/data.json")

# 1. Lectura defensiva
payload = {}
if os.path.exists(DATA_PATH):
    try:
        with open(DATA_PATH, "r") as f:
            payload = json.load(f)
    except Exception:
        payload = {}

# 2. Patch MERGE - Japan Yen Intervention - CONFIRMED MOF
patch = {
    "japan_yen_intervention": {
        "id": "JAPAN_YEN_2026_11_09",
        "timestamp": time.strftime("%H:%M:%S VET"),
        "status": "FX_INTERVENTION_CONFIRMED",
        "verification": "CONFIRMED - Dato oficial MOF Japon - Datos trimestrales publicados 9 Nov - Confirmacion retrospectiva, NO intervencion en vivo hoy",
        "source": "Reuters LSEG - Makiko Yamazaki - 9 Nov 2026 - go.refinitiv.com/news?id=urn:newsml:newswire.refinitiv.com:20261108:nQ8N42X02U:1 - JAPAN-YEN URGENT",
        "datos_mof": {
            "intervencion_dias": "3 dias - 30 Jul al 3 Ago 2026",
            "record_30_jul": "7.98 trillones yen = $50.36B vendidos en dolares para comprar yen - Record historico diario",
            "record_previo": "6.28 trillones yen el 30 Abr - Superado por 30 Jul",
            "serie_mof": "Data desde 1991",
            "fx_cable": "$1 = 158.4500 yen"
        },
        "m82_impact": {
            "carry_trade": "Yen debil = carry barato - Intervencion $50B encarece carry, riesgo desarme - Golpea todos activos riesgo al mismo tiempo - NVDA, AI, petroleo, emergentes",
            "energia_japon": "Japon importa casi todo petroleo / LNG - Yen desplomado amenaza importaciones energia - MOF frena caida para proteger costo energia",
            "timing": "30 Jul - 3 Ago - En pleno risk-on AI - Japon frena caida yen aunque cueste reservas",
            "classification": "FX_INTERVENTION_CONFIRMED - Senal estres sistemico - NO disparador compra - Justifica BUNKER"
        },
        "m82_dictamen": {
            "postura": "BUNKER MODE / 0.30x LOCK - SIN CAMBIO - 100% DRY POWDER - 0 ejecuciones - REFORZADO por estres FX",
            "regla": "Solo se re-evalua si MOF interviene de nuevo en vivo + USD/JPY rompe niveles clave + desarme carry confirmado - Hasta entonces, vigilancia",
            "relacionado": "APEC_SHENZHEN_2026_11_18_19 - WATCHLIST_ACTIVE / TRUMP_AI_GUARDRAILS - POLICY_SIGNAL / NVDA_HUANG - INVESTIGATION_OPEN"
        }
    },
    "wire": "M82 WIRE: Japan Yen Intervention - CONFIRMED MOF (9 Nov) - $50.36B record 30 Jul - Carry trade en riesgo",
    "last_patch": "JAPAN_YEN_2026_11_09 - FX_INTERVENTION_CONFIRMED - MERGE OK"
}

payload.update(patch)
payload["timestamp"] = time.strftime("%H:%M:%S VET")

# 3. Escritura staged con reemplazo atomico
tmp = DATA_PATH + ".tmp"
with open(tmp, "w") as f:
    json.dump(payload, f, indent=2)
os.replace(tmp, DATA_PATH)
print("[MERGE OK] Japan Yen Intervention inyectado al Bus sin tocar OBS.")
