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

# 2. Patch MERGE - Puente APEC AI / Chips - PREAMBULO 60 MINUTES
patch = {
    "apec_ai_chips_bridge": {
        "id": "APEC_AI_CHIPS_BRIDGE_2026_11_08",
        "timestamp": time.strftime("%H:%M:%S VET"),
        "status": "BRIDGE_ACTIVE_PRE_APEC",
        "verification": "PUENTE LOGICO - NO ES ACUERDO - Preambulo 60 Minutes 8 Nov -> APEC 18-19 Nov - TODO UNCONFIRMED hasta comunicado oficial",
        "preambulo_8_nov": {
            "trump_60min": "I don't mind guardrails - No quiero EE.UU. en deep second position detras de China",
            "interpretacion_m82": "Trump prepara mercado: guardrails SI, freno a empresas NO - Acuerdo chips no se leera como venderse a China, sino como guardrails con control"
        },
        "mesa_apec_18_19": {
            "trump_xi": "Tregua comercial expira 10 Ene 2027 + Chips IA + Tierras raras + Soja / Energia",
            "china_pide": "Relajar controles exportacion chips avanzados - NVDA H200 / Blackwell, AMD MI - Acceso semiconductores para entrenar IA",
            "eeuu_pide": "Tierras raras, tregua extendida, compra soja / energia, freno fentanyl / controles",
            "xi_putin_18_nov": "Energia + Ucrania - Respaldo energetico para que China no dependa de EE.UU."
        },
        "escenarios_chips": {
            "A_solo_foto": {
                "probabilidad": "ALTA",
                "descripcion": "Nada de chips - Guardrails quedan en retorica",
                "accion_m82": "PHOTO_OP - BUNKER intacto - 0 ejecuciones - NVDA / AI sin disparador"
            },
            "B_tregua_chips_light": {
                "probabilidad": "MEDIA",
                "descripcion": "EE.UU. permite venta chips capados a China, China suelta tierras raras",
                "accion_m82": "Bullish corto NVDA / AVGO / TSM - Bearish largo ventaja EE.UU. - NO disparador compra BUNKER - Registrar como CHIPS_LIGHT_UNCONFIRMED hasta texto oficial"
            },
            "C_endurecimiento": {
                "probabilidad": "BAJA-MEDIA",
                "descripcion": "EE.UU. aprieta controles, China retalia tierras raras",
                "accion_m82": "Shock cadena AI - NVDA / TSM / AVGO caen por supply chain, no earnings - BUNKER protege - NO comprar dip sin confirmacion"
            }
        },
        "blackrock_ai_anchor_afectado": "NVDA, AVGO, TSM, ARM, PLTR, MSFT, META, GOOGL, AMZN, AAPL - Sin cambio ponderacion hasta documento oficial",
        "m82_dictamen": {
            "postura": "BUNKER MODE / 0.30x LOCK - SIN CAMBIO - 100% DRY POWDER - 0 ejecuciones",
            "regla": "NO operar sobre titulares APEC en vivo - Ruido 2h, correccion 6h - Solo texto oficial / documento firmado cambia postura",
            "relacionado": "TRUMP_AI_GUARDRAILS_2026_11_08 - POLICY_SIGNAL / APEC_SHENZHEN_2026_11_18_19 - WATCHLIST_ACTIVE"
        }
    },
    "wire": "M82 WIRE: Puente APEC AI / Chips - Preambulo 60 Minutes -> Shenzhen 18-19 Nov - BUNKER intacto",
    "last_patch": "APEC_AI_CHIPS_BRIDGE_2026_11_08 - BRIDGE_ACTIVE - MERGE OK"
}

payload.update(patch)
payload["timestamp"] = time.strftime("%H:%M:%S VET")

# 3. Escritura staged con reemplazo atomico
tmp = DATA_PATH + ".tmp"
with open(tmp, "w") as f:
    json.dump(payload, f, indent=2)
os.replace(tmp, DATA_PATH)
print("[MERGE OK] Puente APEC AI / Chips inyectado al Bus sin tocar OBS.")
