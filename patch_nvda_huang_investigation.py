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

# 2. Patch MERGE - NVDA Huang Investigation - CONFIRMED affair + ALLEGED spy - NO PROOF compromise
patch = {
    "nvda_huang_investigation": {
        "id": "NVDA_HUANG_2026_11_08",
        "timestamp": time.strftime("%H:%M:%S VET"),
        "status": "INVESTIGATION_OPEN",
        "verification": "CONFIRMED: Huang admite affair + Board abre investigacion independiente + Trump defiende - ALEGADO, NO PROBADO: Alice Huang espia PRC, compromiso secretos Nvidia - Board: no reason to believe secrets compromised - Sin evidencia publica de filtracion",
        "source": "Reuters 8-9 Nov / CNN 8 Nov / NYT 29 Oct / FT / Nvidia Board Statement 8 Nov",
        "confirmed": {
            "huang_memo_8_nov": "I was unfaithful to my wife. My actions hurt her and our children. There is no excuse. I am deeply sorry. - NO nombra a otra persona",
            "board_8_nov": "Investigacion independiente - Comite directores independientes + outside counsel - Huang sigue CEO sin interrupcion - No reason to believe national security or NVIDIA secrets compromised - Will examine all available information",
            "trump_8_nov": "I think he's an honorable guy - I have not spoken to him about it - I just know he's a fine person, but you never know - I think he probably has an excuse, you have to hear it - Amazing job for our country - No confirma si lo lleva a Asia",
            "rubio_8_nov": "I just can't comment because of the nature of it",
            "congress_5_nov": "3 chairmen GOP - Foreign Affairs, CCP, Intelligence - Carta a Huang pidiendo briefing conjunto a puerta cerrada sobre Alice Huang y protocolos seguridad Nvidia"
        },
        "alleged_not_proven": {
            "alice_huang": "Ciudadana china, ex-reportera TV China, ejecutiva top Megaspeed Singapur - NO relacionada con Jensen - Inteligencia EE.UU. cree reclutada por Ministerio Seguridad Estado China para aprender chips IA y posiblemente influir a Jensen",
            "megaspeed": "Data centers Singapur - Uno de mayores clientes Nvidia SEA - Compro chips desde 2024 - Sospechosa bulk para revender / contrabandear a China o correr datacenters para usuarios chinos",
            "memo_primavera": "Memo supervisado por Rubio circulo entre top policymakers Trump - Trump briefed ano pasado / antes visita China mayo - No actuo",
            "china_response": "Embajada China: groundless smears"
        },
        "m82_impact": {
            "apec_chips_bridge": "Escenario B Tregua + Chips Light BAJA de MEDIA a BAJA - Politicamente toxico - Escenario C Endurecimiento SUBE - Congreso exigira mas controles, no menos",
            "nvda": "Riesgo reputacional + regulatorio + liderazgo, NO earnings todavia - Volatilidad por investigacion abierta - Sin cambio ponderacion BUNKER",
            "classification": "INVESTIGATION_OPEN - No disparador compra / venta - Solo vigilancia"
        },
        "m82_dictamen": {
            "postura": "BUNKER MODE / 0.30x LOCK - SIN CAMBIO - 100% DRY POWDER - 0 ejecuciones",
            "regla": "Solo cambia si Board / Congreso / DOJ publican hallazgo de compromiso de secretos - Hasta entonces, affair = personal CONFIRMED, espionaje = ALLEGED",
            "relacionado": "APEC_AI_CHIPS_BRIDGE_2026_11_08 - BRIDGE_ACTIVE / TRUMP_AI_GUARDRAILS_2026_11_08 - POLICY_SIGNAL"
        }
    },
    "wire": "M82 WIRE: NVDA Huang - INVESTIGATION_OPEN (8 Nov) - Affair CONFIRMED, espionaje ALLEGED - APEC Chips Light baja a BAJA",
    "last_patch": "NVDA_HUANG_2026_11_08 - INVESTIGATION_OPEN - MERGE OK"
}

payload.update(patch)
payload["timestamp"] = time.strftime("%H:%M:%S VET")

# 3. Escritura staged con reemplazo atomico
tmp = DATA_PATH + ".tmp"
with open(tmp, "w") as f:
    json.dump(payload, f, indent=2)
os.replace(tmp, DATA_PATH)
print("[MERGE OK] NVDA Huang Investigation inyectado al Bus sin tocar OBS.")
