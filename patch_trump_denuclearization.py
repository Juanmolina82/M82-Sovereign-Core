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

# 2. Patch MERGE - Trump Denuclearization Talks - NEGOTIATION / UNCONFIRMED
patch = {
    "trump_denuclearization_talks": {
        "id": "TRUMP_DENUC_2026_11_08",
        "timestamp": time.strftime("%H:%M:%S VET"),
        "status": "NEGOTIATION_UNCONFIRMED",
        "verification": "NO ES ACUERDO - ES PROPUESTA EN NEGOCIACION - NO USAR COMO HECHO",
        "source": "AP / Reuters / Arms Control Association - 19 Oct - 8 Nov 2026",
        "actors": {
            "trump": "Propone cumbre trilateral EE.UU. - Rusia - China sobre armas nucleares / denuclearization. Frase 19 Oct: 'We would have it to talk about nuclear weapons and denuclearisation' / 'If President Xi wants to have it, I'd have it'",
            "putin": "Propuso cumbre el 9 Oct en llamada con Trump - enfoque original: guerra en Ucrania sin Kyiv en mesa",
            "xi": "Anfitrion APEC Shenzhen - No ha dicho si definitivo - 4 Nov Beijing: 'in communication with relevant parties' - sin fecha, agenda ni formato confirmado"
        },
        "proposed_venue": "Al margen APEC Shenzhen, China - 18-19 Nov 2026 - TENTATIVO, SIN CONFIRMAR",
        "positions": {
            "us": "Control de armas / denuclearization - Trump: EE.UU. #1, Rusia #2, China #3 pero alcanzando en ~5 anos",
            "russia": "Ucrania como tema central - Kremlin 3 Nov: trabajando en organizarla - 8 Nov: agenda en discusion",
            "china": "RECHAZO FORMATO TRILATERAL 16 Oct - MFA: 'neither fair, reasonable nor realistic to ask China to join so-called trilateral nuclear disarmament negotiations at this stage' - 30 Oct Xi a Steinmeier: no ve preparativos para cumbre sobre Ucrania"
        },
        "context": {
            "new_start": "EXPIRADO 2026 - Sin tratado vigente EE.UU.-Rusia que limite arsenales estrategicos",
            "p5_process": "5 potencias nucleares NPT se reunieron semana 5 Oct en NY - Sin contenido publico",
            "us_china_private": "WSJ 24 Sep: EE.UU. hablando en privado con China sobre expansion arsenal + acusacion explosion 10 toneladas Jun 2020 - CNN 6 Oct: visitas reciprocas a sitios de prueba / laboratorios en discusion",
            "analyst_view": "AP: intereses tan opuestos - lo mas probable es 'carefully staged photo more than any agreement'"
        },
        "m82_dictamen": {
            "postura": "BUNKER MODE / 0.30x LOCK - SIN CAMBIO",
            "accion": "NO DISPARADOR - Solo vigilancia - 0 ejecuciones",
            "vigilar": ["10-11 Nov: conversaciones Ucrania-Rusia-EE.UU. Abu Dhabi", "18-19 Nov: confirmacion o no de trilateral en Shenzhen APEC"],
            "riesgo_contaminacion": "NO inyectar como SYNCED / HECHO - Solo como NEGOTIATION_UNCONFIRMED hasta que haya comunicado conjunto oficial"
        }
    },
    "wire": "M82 WIRE: Trump Denuclearization Talks - NEGOTIATION_UNCONFIRMED (8 Nov) - Propuesta trilateral, sin acuerdo",
    "last_patch": "TRUMP_DENUC_2026_11_08 - NEGOTIATION_UNCONFIRMED - MERGE OK"
}

payload.update(patch)
payload["timestamp"] = time.strftime("%H:%M:%S VET")

# 3. Escritura staged con reemplazo atomico
tmp = DATA_PATH + ".tmp"
with open(tmp, "w") as f:
    json.dump(payload, f, indent=2)
os.replace(tmp, DATA_PATH)
print("[MERGE OK] Trump Denuclearization Talks (NEGOTIATION_UNCONFIRMED) inyectado al Bus sin tocar OBS.")
