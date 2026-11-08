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

# 2. Patch MERGE - Iran Stalemate Talks Open - 8 Nov
patch = {
    "iran_stalemate_8nov": {
        "id": "IRAN_STALEMATE_2026_11_08",
        "timestamp": time.strftime("%H:%M:%S VET"),
        "status": "IRAN_STALEMATE_TALKS_OPEN",
        "verification": "CONFIRMED Reuters LSEG WRAPUP 3 - 8 Nov - Trump highly unlikely strikes si talks avanzan - Rubio: no breakthrough inminente - Hormuz: buque EE.UU. deshabilitado CONFIRMADO, 2-3 tanqueros minas REPORTADO IRAN, NO confirmado Reuters - Qeshm: Tasnim 2 misiles, NI Iran NI EE.UU. comentan",
        "source": "Reuters LSEG - go.refinitiv.com/news?id=urn:newsml:newswire.refinitiv.com:20261108:nL6N46P069:3 - IRAN-CRISIS WRAPUP 3",
        "trump_cnn_8_nov": {
            "strikes": "It depends on whether or not they sign a very strong agreement - Highly unlikely it's going to be necessary",
            "threat": "38 bridges that we can knock down in literally one hour - Si strikes reanudan, targets infraestructura ya identificados",
            "nota": "CNN no especifica pregunta exacta - Reuters lo marca",
            "truth_social": "Task Force Iron Gate is in full force and effect - Crackdown armas avanzadas + material sancionado - Fronteras terrestres + Mar Caspio",
            "vance": "A lot of people did not like Vance's comments on Iran - Vance habia dicho: The reason we lost is the war"
        },
        "rubio_8_nov": {
            "midterms": "Se niega a comentar link guerra-elecciones - Defiende: president identified very real threat and addressed it",
            "diplomacy": "No cree breakthrough inminente - Right now hasn't been very productive because Iranian demands are simply not just unacceptable, but in some cases outrageous and ridiculous and really not realistic"
        },
        "hormuz_8_nov": {
            "eeuu_confirmado": "Sabado noche USAF disparo a popa buque comercial Golfo Oman, deshabilitado intentando romper bloqueo",
            "iran_reportado_no_confirmado": "2 petroleros chocan minas ruta no autorizada Hormuz, se incendian - 3er tanquero explota y se incendia Fars - Reuters NO pudo confirmar",
            "qeshm": "Tasnim: 2 misiles Qeshm Island - TV estatal Iran: no confirmados strikes misiles, sugiere actividad militar irani propia - NI Iran NI EE.UU. comentan reporte Tasnim - EE.UU. 2 Nov dijo strike limitado defensivo Qeshm vs SAM iranies",
            "ukmto": "Incidente bulk carrier + fuerzas militares Golfo Oman, 18mn este Khor Fakkan UAE - Dano desconocido - No claro si mismo ataque EE.UU.",
            "houthi_saudi": "Domingo Ministerio Energia Saudita: edificio administrativo Aramco Riyadh danado por debris tras intento ataque - Sin heridos / muertos - Conflicto Houthi-Saudita escalando este mes"
        },
        "negociacion": {
            "qatar": "Qatar nego reportes de que EE.UU.-Iran fallaron deal - PM qatari: ambas partes siguen trabajando hacia acuerdo",
            "propuesta_iran_jueves": "Iran entrego propuesta nuclear via Qatar - EE.UU. revisando - Discusiones dependen Washington primero cumpliendo 7 demandas Iran: alivio sanciones, acceso activos congelados, reparaciones guerra",
            "eeuu_posicion": "Temas nucleares deben estar en conversaciones iniciales",
            "contexto": "Ataques EE.UU.-Israel desde febrero - Bloqueo EE.UU. puertos iranies desde abril - Hormuz restringido - Motor gas +50% desde enero que costo midterms"
        },
        "m82_impact": {
            "gas_petroleo": "Sin desbloqueo Hormuz, no hay alivio estructural gas - BUNKER protege",
            "apec": "Trump no quiere strikes antes APEC 18-19 Nov - Pausa tactica con bloqueo activo - Iran no en agenda formal APEC, pero energia si en Xi-Putin-Trump",
            "sucesion": "Rubio vs Vance vs Trump - Inestabilidad sucesion, no estabilidad politica exterior",
            "classification": "IRAN_STALEMATE_TALKS_OPEN - No paz, no escalada mayor - Pausa tactica con bloqueo activo"
        },
        "m82_dictamen": {
            "postura": "BUNKER MODE / 0.30x LOCK - SIN CAMBIO - 100% DRY POWDER - 0 ejecuciones",
            "regla": "Solo cambia si hay acuerdo firmado / desbloqueo Hormuz verificado / strikes mayores confirmados - Hasta entonces, stalemate",
            "relacionado": "TRUMP_60MIN_MIDTERMS - CONFIRMED / APEC_SHENZHEN_2026_11_18_19 - WATCHLIST_ACTIVE"
        }
    },
    "wire": "M82 WIRE: Iran Stalemate Talks Open (8 Nov) - Trump highly unlikely strikes si talks avanzan - Rubio: no breakthrough - Hormuz bloqueo activo",
    "last_patch": "IRAN_STALEMATE_2026_11_08 - STALEMATE_TALKS_OPEN - MERGE OK"
}

payload.update(patch)
payload["timestamp"] = time.strftime("%H:%M:%S VET")

# 3. Escritura staged con reemplazo atomico
tmp = DATA_PATH + ".tmp"
with open(tmp, "w") as f:
    json.dump(payload, f, indent=2)
os.replace(tmp, DATA_PATH)
print("[MERGE OK] Iran Stalemate inyectado al Bus sin tocar OBS.")
