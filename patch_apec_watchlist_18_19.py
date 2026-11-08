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

# 2. Patch MERGE - APEC Watchlist 18-19 Nov 2026 - PRE-CARGADO
patch = {
    "apec_2026_watchlist": {
        "id": "APEC_SHENZHEN_2026_11_18_19",
        "timestamp": time.strftime("%H:%M:%S VET"),
        "status": "WATCHLIST_ACTIVE",
        "verification": "VENTANA CALIENTE - NADA CONFIRMADO COMO HECHO - TODO UNCONFIRMED HASTA COMUNICADO OFICIAL",
        "venue": "APEC Economic Leaders Meeting - Shenzhen, China - 21 economias",
        "calendar": {
            "16_nov": "Trump en Manila - ASEAN - antes de seguir a China",
            "17_18_nov": "APEC CEO Summit - Shenzhen",
            "18_19_nov": "APEC Leaders Meeting - Shenzhen",
            "18_nov_tentativo": "Xi-Putin bilateral esperada - enfoque relacion bilateral / energia / Ucrania sin Kyiv"
        },
        "events_to_watch": {
            "1_trump_xi_bilateral": {
                "probabilidad": "ALTA - Tercera reunion del ano",
                "tema_real": "Tregua comercial EE.UU.-China EXPIRA 10 Ene 2027 - Extender / Endurecer / Dejar morir",
                "status": "PENDING_18_19_NOV",
                "m82_result": None
            },
            "2_xi_putin_bilateral": {
                "probabilidad": "ALTA - Casi segura 18 Nov",
                "tema_real": "Relacion bilateral, energia, Ucrania sin Kyiv - Beijing: Ucrania NO en su agenda trilateral",
                "status": "PENDING_18_19_NOV",
                "m82_result": None
            },
            "3_trilateral_xi_trump_putin": {
                "probabilidad": "MEDIA - Primera vez los tres juntos, si se da",
                "tema_real": "Trump: desnuclearizacion / Putin: Ucrania / Xi: imagen anfitrion sin compromisos",
                "confirmacion": "China 4 Nov Mao Ning: 'in communication with relevant parties' - SIN fecha/agenda/formato - Kremlin 3 Nov: trabajando en organizarla - Ushakov 25 Oct: 'in principle ready, preparations begun' - NO es anuncio conjunto",
                "analyst_view": "AP: 'carefully staged photo more than any agreement' - intereses opuestos",
                "status": "PENDING_18_19_NOV",
                "m82_result": None
            }
        },
        "scenarios": {
            "A_solo_foto": {
                "probabilidad": "ALTA",
                "descripcion": "Solo foto + comunicados vagos - Sin acuerdo",
                "accion_m82": "Registrar como PHOTO_OP / NO_AGREEMENT - BUNKER intacto - 0 ejecuciones"
            },
            "B_tregua_extendida": {
                "probabilidad": "MEDIA",
                "descripcion": "Tregua comercial Trump-Xi extendida",
                "accion_m82": "Vigilancia - NO disparador de compra - Registrar como TRADE_TRUCE_EXTENDED_UNCONFIRMED hasta texto oficial"
            },
            "C_acuerdo_real": {
                "probabilidad": "BAJA",
                "descripcion": "Acuerdo real nuclear o Ucrania con comunicado conjunto firmado",
                "accion_m82": "Solo ahi se re-evalua postura - Hasta entonces, nada - Requiere documento oficial, no titular"
            }
        },
        "m82_dictamen": {
            "postura": "BUNKER MODE / 0.30x LOCK - SIN CAMBIO - 100% DRY POWDER",
            "regla_oro_18_19": "NO operar sobre titulares en vivo - Ruido primeras 2h, correccion siguientes 6h - Todo UNCONFIRMED hasta documento oficial",
            "webhooks": "DISABLED_BUNKER - 0 ejecuciones",
            "relacionado": "TRUMP_DENUC_2026_11_08 - NEGOTIATION_UNCONFIRMED"
        }
    },
    "wire": "M82 WIRE: APEC Shenzhen 18-19 Nov - WATCHLIST ACTIVE - 3 eventos en vigilancia - BUNKER 0.30x LOCK",
    "last_patch": "APEC_SHENZHEN_2026_11_18_19 - WATCHLIST_ACTIVE - MERGE OK"
}

payload.update(patch)
payload["timestamp"] = time.strftime("%H:%M:%S VET")

# 3. Escritura staged con reemplazo atomico
tmp = DATA_PATH + ".tmp"
with open(tmp, "w") as f:
    json.dump(payload, f, indent=2)
os.replace(tmp, DATA_PATH)
print("[MERGE OK] APEC Watchlist 18-19 Nov pre-cargada - BUNKER 0.30x LOCK - sin tocar OBS.")
