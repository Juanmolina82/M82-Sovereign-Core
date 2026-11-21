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

# 2. Patch MERGE - Gold ROI Russell - OPINION + WGC DATA
patch = {
    "gold_roi_russell": {
        "id": "GOLD_ROI_2026_11_09",
        "timestamp": time.strftime("%H:%M:%S VET"),
        "status": "GOLD_OPINION_WGC_DATA",
        "verification": "COLUMNA OPINION - NO NOTICIA - Datos WGC CONFIRMED, tesis Russell OPINION - No mezclar - Reuters ROI Clyde Russell 9 Nov",
        "source": "Reuters LSEG - Clyde Russell - 9 Nov 2026 - go.refinitiv.com/news?id=urn:newsml:newswire.refinitiv.com:20261108:nL2N46P06N:1 - GOLD-OUTLOOK COLUMN-RUSSELL ROI",
        "precio": {
            "spot_6_nov": "$4,065.63 XAU=",
            "min_ano_30_oct": "$3,869.85",
            "record_29_ene": "$5,594.82",
            "correccion_23_mar": "$4,097.99 tras profit-taking",
            "piso": "$4,000 psicologico - Julio y Octubre por debajo, recupero - Ahora finding floor"
        },
        "datos_wgc_confirmados": {
            "bancos_centrales_q3": "321.2 toneladas - Sube de 296.3 Q2 - Mayor desde Q4 2024",
            "bancos_centrales_q1": "57.7 toneladas - Cuando precio en record - Demanda sensible a precio - Caida bajo $4,000 probablemente anima compras Q4",
            "etf_oct": "+19 toneladas inflows",
            "etf_q3": "+211.2 toneladas - Revierte -47.3 toneladas Q2",
            "joyeria_india_q3": "99.9 toneladas - Mayor desde Q4 ano pasado - Traders reportan mas interes por festivales",
            "joyeria_china_q3": "71.9 toneladas - Sube de 55.7 Q2",
            "joyeria_china_india": "Casi 2/3 demanda global joyeria"
        },
        "tesis_russell_opinion": {
            "rol_oro": "Perdio rol tradicional hedge inflacion / geopolitica - Ahora mas trading especulativo - Froth / hot money lavado en meses recientes",
            "corto_plazo": "En limbo, vulnerable swings ambas direcciones - Riesgo: debilidad equities por cuestionamiento boom AI + victoria Democratas midterms cuestionan data centers hambrientos energia - Si equities caen, liquidan oro para cubrir - Patron historico",
            "medio_plazo": "Debilidad equities puede ser positivo si se extiende a economia real - Debilidad equities + caida crudo por esperanzas fin Iran -> dial monetario vuelve neutral, posiblemente recortes proximo ano",
            "largo_plazo": "Bullish - Diversificacion ante deficit fiscal EE.UU. insostenible + montana deuda comiendo revenue para servicio + demanda joyeria India / China",
            "causa_sufrimiento_desde_ene": "Shift expectativas monetarias EE.UU. a tasas probablemente mas altas"
        },
        "m82_impact": {
            "cadena_midterms": "Democratas cuestionan data centers -> golpea NVDA / AI -> golpea equities -> golpea oro corto plazo por liquidacion",
            "cadena_iran": "Esperanza fin Iran -> crudo cae -> expectativa tasas baja -> oro sube medio plazo",
            "cadena_yen": "Desarme carry trade -> liquidacion oro tambien en cadena",
            "classification": "GOLD_OPINION_WGC_DATA - Datos WGC CONFIRMED, tesis OPINION - No cambia ponderacion oro BUNKER"
        },
        "m82_dictamen": {
            "postura": "BUNKER MODE / 0.30x LOCK - SIN CAMBIO - 100% DRY POWDER - 0 ejecuciones",
            "regla": "Oro en BUNKER es hedge fiscal, no trade - Solo se re-evalua si WGC Q4 confirma compras centrales masivas + Fed cambia a recortes - Hasta entonces, vigilancia",
            "relacionado": "TRUMP_60MIN_MIDTERMS / IRAN_STALEMATE_2026_11_08 / JAPAN_YEN_2026_11_09"
        }
    },
    "wire": "M82 WIRE: Gold ROI Russell - OPINION + WGC DATA (9 Nov) - Piso $4,000 - Largo plazo bullish fiscal, corto plazo rehen equities",
    "last_patch": "GOLD_ROI_2026_11_09 - GOLD_OPINION_WGC_DATA - MERGE OK"
}

payload.update(patch)
payload["timestamp"] = time.strftime("%H:%M:%S VET")

# 3. Escritura staged con reemplazo atomico
tmp = DATA_PATH + ".tmp"
with open(tmp, "w") as f:
    json.dump(payload, f, indent=2)
os.replace(tmp, DATA_PATH)
print("[MERGE OK] Gold ROI Russell inyectado al Bus sin tocar OBS.")
