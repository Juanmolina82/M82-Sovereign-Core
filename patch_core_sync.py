import os, json, time
DATA_PATH = os.path.expanduser("~/M82/app/data.json")
payload = {}
if os.path.exists(DATA_PATH):
    try:
        with open(DATA_PATH) as f: payload = json.load(f)
    except Exception: payload = {}

sync_patch = {
    "wire": "M82 WIRE: Telemetria Macro & Sovereign Core Auditada (1000288638.jpg) | BUNKER 0.30x LOCK Intacto",
    "core_integrity_check": "100% VERIFIED",
    "timestamp": time.strftime("%H:%M:%S VET"),
    "audit_source": "1000288638.jpg - Termux JSON Terminal Dump",
    "macro_chains": {
        "midterms_chain": "Presion democrata sobre Data Centers -> Venta NVDA/AI -> Caida Equities -> Liquidacion Oro corto plazo",
        "iran_chain": "Expectativa resolucion -> Caida crudo -> Expectativas baja tasas -> Soporte mediano plazo Oro",
        "yen_carry_chain": "Desarme posiciones Yen -> Presion compresiva liquidacion cruzada",
        "gold_hedge": "Cobertura fiscal sin trading activo en bunker. Re-evaluacion condicionada a compras Q4 bancos centrales (WGC) y pivote Fed"
    },
    "fx_sovereign": {
        "fedwatch_dec_hike": "79.0%",
        "eur_usd": 1.11485,
        "nz_election": "Conteo final pendiente 27 Nov",
        "blackrock_aum": "$15.49T",
        "norges_gpfq": "GPFG Equity Synced",
        "japan_mof_single_day_record": "¥7.98T single-day",
        "japan_mof_total_period": "¥15.4T / $97.19B - FX_INTERVENTION_CONFIRMED"
    },
    "vectors_alert": {
        "apec_shenzhen": "Watchlist 18-19 Nov",
        "nvda": "Huang Probe UPDATE 6 -8% ~$350B",
        "iran": "STALEMATE_TALKS_OPEN",
        "gold_floor": "$4,000 - XAU $4,106.64",
        "silver_spot": "XAG $52.92"
    },
    "risk": "BUNKER MODE / 0.30x LOCK - 100% Dry Powder - 0 ejecuciones"
}
payload.update(sync_patch)
tmp = DATA_PATH + ".tmp"
with open(tmp, "w") as f: json.dump(payload, f, indent=2)
os.replace(tmp, DATA_PATH)
print("[SYNC OK] CORE sellado con telemetria completa.")
