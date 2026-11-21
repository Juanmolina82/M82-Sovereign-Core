import os, json, time

DATA_PATH = os.path.expanduser("~/M82/app/data.json")

# 1. Lectura defensiva - Parche 1000288287
payload = {}
if os.path.exists(DATA_PATH):
    try:
        with open(DATA_PATH, "r") as f:
            payload = json.load(f)
    except Exception:
        payload = {}

# 2. Patch MERGE - Trump AI Guardrails - POLICY SIGNAL, NO REGULATION YET
patch = {
    "trump_ai_guardrails": {
        "id": "TRUMP_AI_GUARDRAILS_2026_11_08",
        "timestamp": time.strftime("%H:%M:%S VET"),
        "status": "POLICY_SIGNAL_NO_REGULATION_YET",
        "verification": "CONFIRMED Reuters LSEG 8 Nov - UPDATE 1 - USA-TRUMP/AI - Cambio de tono, NO cambio de politica - Sin ley, sin EO, sin fecha, sin nivel definido",
        "source": "Reuters LSEG Workspace - Jarrett Renshaw - 8 Nov 2026 - go.refinitiv.com/news?id=urn:newsml:newswire.refinitiv.com:20261109:nL2N46Q00A:1",
        "event": "USA-TRUMP/AI - CBS 60 Minutes - Ross Douthat",
        "quotes": {
            "guardrails": "I don't mind guardrails",
            "china_position": "No quiere regulaciones que pongan a EE.UU. en 'a deep second position' detras de China, que segun el no tiene tales restricciones",
            "democrats": "Apertura a trabajar con Democratas en safeguards",
            "risks": "Riesgos de IA son manejables"
        },
        "context_reuters": "Antes: Trump favorecia que empresas se auto-regulen, sin restricciones gubernamentales amplias - Ahora: apertura a safeguards, pero no esta claro a que nivel",
        "m82_impact": {
            "blackrock_ai_anchor": "NVDA, AAPL, MSFT, META, AMZN, GOOGL, AVGO, TSM, PLTR, ARM - Riesgo regulatorio sube en tono, NO en ley - Sin cambio de ponderacion",
            "china_link": "Preambulo APEC 18-19 Nov - Trump-Xi: IA / chips / control exportaciones",
            "congress": "Congreso democrata entrante post-midterms - Ventana para guardrails light, no sweeping regulation",
            "classification": "POLICY_SIGNAL - No disparador de capital - No cambio BUNKER"
        },
        "m82_dictamen": {
            "postura": "BUNKER MODE / 0.30x LOCK - SIN CAMBIO - 100% DRY POWDER - 0 ejecuciones",
            "regla": "Solo se re-evalua si hay bill / EO / texto oficial con nivel de regulacion definido - Hasta entonces, solo tono"
        }
    },
    "wire": "M82 WIRE: Trump AI Guardrails - POLICY_SIGNAL (8 Nov) - 'I don't mind guardrails' - Sin regulacion todavia",
    "last_patch": "TRUMP_AI_GUARDRAILS_2026_11_08 - POLICY_SIGNAL - MERGE OK"
}

payload.update(patch)
payload["timestamp"] = time.strftime("%H:%M:%S VET")

# 3. Escritura staged con reemplazo atomico
tmp = DATA_PATH + ".tmp"
with open(tmp, "w") as f:
    json.dump(payload, f, indent=2)
os.replace(tmp, DATA_PATH)
print("[MERGE OK] Trump AI Guardrails (POLICY_SIGNAL) inyectado al Bus sin tocar OBS.")
