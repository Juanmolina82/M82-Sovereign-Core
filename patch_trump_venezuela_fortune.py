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

# 2. Patch MERGE - Trump Venezuela Fortune - CLAIM, NO VERIFICADO COMO GANANCIA NETA
patch = {
    "trump_venezuela_fortune_claim": {
        "id": "TRUMP_VEN_FORTUNE_2026_11_08",
        "timestamp": time.strftime("%H:%M:%S VET"),
        "status": "CLAIM_TRUMP",
        "verification": "CLAIM DE TRUMP - NO VERIFICADO COMO GANANCIA NETA EE.UU. - NO USAR PARA RECALIBRAR PRODUCCION NI PRECIOS - NO ES DATO EIA / OPEC / REUTERS / KPLER / LSEG",
        "source": "CBS 60 Minutes 6-8 Nov 2026 / Fox News 16 May 2026 / Politico 28 / Reuters / FT / Congreso EE.UU.",
        "versions_separadas": {
            "v1_60_minutes_nov": {
                "fecha": "6-8 Nov 2026 - CBS 60 Minutes - Ross Douthat",
                "frase_exacta": "We've won two wars. We've won Venezuela and taken out billions and billions and billions of dollars already, and we will be taking out many billions of dollars and get along very well. We won that war in less than one hour.",
                "nota": "NO dijo literal 'We made a fortune' en este corte - dijo 'billions and billions'"
            },
            "v2_fox_may": {
                "fecha": "16 May 2026 - Fox News",
                "frase_exacta": "We made a fortune from Venezuelan oil",
                "claim_adicional": "Venezuela gano mas de petroleo en 8 meses que en los 10 anos anteriores - SIN FUENTE, SIN AUDITORIA PUBLICA",
                "nota": "ESTA es la version literal 'made a fortune'"
            },
            "v3_politico": {
                "fecha": "Politico 28 - Entrevista Politico",
                "frase_exacta": "I've made a fortune for the United States by focusing [on Venezuela]",
                "nota": "Tercera version - mismo mensaje, distinto framing"
            }
        },
        "hechos_verificados": {
            "operacion_3_ene_2026": "Raid 48 minutos - Trump: '48 minutes and 13 seconds' - Captura Maduro + Cilia Flores - Detenidos",
            "orden_9_ene": "Ingresos petroleros = propiedad soberana Venezuela pero en custodia Tesoro EE.UU. - Rubio con autoridad aprobar / bloquear desembolsos",
            "primer_tramo": "~$500M venta inicial a Vitol / Trafigura - Fondos a cuenta controlada EE.UU. en Qatar - Riesgo embargo acreedores - Reuters: $300M repartidos entre 4 bancos venezolanos para vender dolares en mercado cambiario",
            "total_acumulado_prensa": "+$13,000M en ventas petroleo venezolano desde enero - ~150M barriles - Segun Trump / FT - BRUTO, NO GANANCIA NETA",
            "desembolsos_state_dept_abr": "~$3,000M para salarios gobierno + suministros petroleros en Venezuela",
            "investigacion_congreso": "House Oversight, Senate Finance / Banking - Wyden, Warren, Garcia, Casten - Piden trazabilidad - Bessent: no confirmo quien controla ni si fluye a personas EE.UU. - Auditoria KPMG mencionada, nunca compartida con Congreso ni publico",
            "sin_contabilidad_publica": "Cerca de $10B sin contabilidad publica completa segun calculo prensa - Falta transparencia, NO prueba de robo personal - NO hay evidencia en reporting serio de que Trump personalmente haya metido dinero en cuenta privada"
        },
        "m82_dictamen": {
            "postura": "BUNKER MODE / 0.30x LOCK - SIN CAMBIO - 100% DRY POWDER - 0 ejecuciones",
            "divergencia_venezuela_mantenida": "Reuters Oct 860K / OPEC Sep 1,206K comunicado / 1,150K secundarias / PDVSA Gobierno Oct 1,251K-1,252K claim / Merey 16 $93.92 last - Frase Trump NO resuelve divergencia - Es narrativa politica post-midterms, no dato",
            "relacionado": "TRUMP_60MIN_MIDTERMS - CONFIRMED - Guerra Iran + Gas = derrota midterms / TRUMP_DENUC_2026_11_08 - NEGOTIATION_UNCONFIRMED / APEC_SHENZHEN_2026_11_18_19 - WATCHLIST_ACTIVE",
            "regla": "Todo claim Trump sobre Venezuela va como CLAIM_TRUMP hasta auditoria publica / EIA / OPEC / Reuters / Kpler"
        }
    },
    "wire": "M82 WIRE: Trump Venezuela Fortune - CLAIM_TRUMP (8 Nov) - 3 versiones separadas - $13B bruto, no ganancia neta verificada",
    "last_patch": "TRUMP_VEN_FORTUNE_2026_11_08 - CLAIM_TRUMP - MERGE OK"
}

payload.update(patch)
payload["timestamp"] = time.strftime("%H:%M:%S VET")

# 3. Escritura staged con reemplazo atomico
tmp = DATA_PATH + ".tmp"
with open(tmp, "w") as f:
    json.dump(payload, f, indent=2)
os.replace(tmp, DATA_PATH)
print("[MERGE OK] Trump Venezuela Fortune (CLAIM_TRUMP) inyectado al Bus sin tocar OBS.")
