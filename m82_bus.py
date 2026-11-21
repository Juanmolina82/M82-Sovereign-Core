import os
import json
import time

DATA_PATH = os.path.expanduser("~/M82/app/data.json")

def broadcast(patch):
    # 1. Leer sin fallar — parche 1000288287
    payload = {}
    if os.path.exists(DATA_PATH):
        try:
            with open(DATA_PATH, "r") as f:
                payload = json.load(f)
        except Exception:
            payload = {}
    # 2. MERGE — nunca overwrite
    payload.update(patch)
    payload["timestamp"] = time.strftime("%H:%M:%S VET")
    # 3. Atómico .tmp -> os.replace
    tmp = DATA_PATH + ".tmp"
    with open(tmp, "w") as f:
        json.dump(payload, f, indent=2)
    os.replace(tmp, DATA_PATH)
    print(f"[BUS ATOMICO MASTER] Merge OK: {time.strftime('%H:%M:%S')} - CORE preservado")

if __name__ == "__main__":
    patch = {
        "source": "M82 Data Core V63.0.01-A (Macro Dossier Robusto)",
        "wire": "M82 WIRE: Refinitiv Vesper WS + Saudi Aramco Sovereignty + Earnings Q3 Consolidated",
        "equities": {
            "BRENT": {"last": 97.76, "settle": 98.32, "markets_today": 98.08, "change_today_pct": -0.21},
            "MEREY16": {"last": 93.92, "opec_sep_avg": 93.75, "status": "recalibracion_pasiva"},
            "WTI": {"last": 90.67, "settle": 90.83, "markets_today": 90.65, "change_today_pct": 0.14, "change_w": -12.8},
            "SPCX": {"last": 134.19, "change_1m": -15.6},
            "GOLD": {"last": 4065.51, "change_today_pct": -0.53}
        },
        "saudi_aramco_dossier": {
            "ticker": "2222.SE",
            "ownership": "State & PIF Dominant (>90%)",
            "green_revenue_pct": "0.7%",
            "debt_maturity_profile": "Well-staggered / Low Short-Term Refinancing Risk",
            "status": "REFINITIV_ARAMCO_SYNCED"
        },
        "refinitiv_vesper_workspace": {"status": "REFINITIV_VESPER_WS_SYNCED", "yield_spread_trend": "Divergencia curva Tesoro vs Commods", "destination_brent": "$97.76 / $98.32"},
        "refinitiv_earnings_q3": {"blackrock_aum_trillion": "15.49", "blackrock_net_flows_q3_b": "205", "auto_europe_china_risk": "VW & European OEMs Capex Cut / Weak China Sales", "tech_cloud_driver": "AWS & Azure Revenue Expansion intact"},
        "inside_debt_4_brazil_asia": {"brazil": {"gov_gdp_2027_pct": 2.46, "bradesco_2027_pct": 0.4, "xp_2027_pct": 0.3, "trade_oct_b": 9.318}, "india_cpi": {"oct_expected_pct": 5.93, "sep_pct": 5.54}, "thailand_cpi": {"headline_oct_yoy_pct": 3.90, "core_yoy_pct": 1.58}, "asia_watch": {"china_ppi_oct_exp_pct": 5.3, "china_cpi_yoy_exp_pct": 0.8}},
        "inside_debt_3_markets_today": {"treasuries": {"us10y": "4.86%", "us30y": "5.26%", "us2y": "4.51%"}, "forex": {"dxy": "102.32", "usd_jpy": "158.48", "eur_usd": "1.1142", "gbp_usd": "1.3351"}, "stocks": {"sp500": "7376.92", "nasdaq": "24579.43", "dji": "51286.21"}, "mexico_inflation": {"headline_oct_pct": 3.64, "core_oct_pct": 3.78}},
        "inside_debt_2_boj_uk_tech": {"boj_ueda": {"inflation_target_pct": 2, "risk": "Some upside risks", "gdp_q3_annualised_pct": 0.3}, "uk_housing_lloyds": {"yoy_oct_pct": -1.2, "mom_oct_pct": -0.6}},
        "inside_debt_1_jobs_fed_ecb": {"us_jobs_oct": {"payrolls": 165000, "consensus": 65000, "beat": 100000, "unemployment_pct": 4.1}, "fed": "Jobs fuerte refuerza hikes - En camino a subir en diciembre"},
        "morning_news_call_2026_11_06": {"top": "Dems AI bills flood + Tesla Cybertruck wind down mid-2027 -> Cybercab", "before_bell": {"sp500_wipeout_trln": 3, "nasdaq_correction": True}, "earnings": {"ABNB": {"rev_q3_b": 4.87, "eps": 3.16}, "DVN": {"adj_eps": 1.42}, "EOG": {"adj_eps": 4.87, "realized_usd": 86.72}, "MP": {"adj_eps": 0.04, "gov_total_m": 120}}},
        "refinery_filing_2026_11_07": {"refinery": "FHR Corpus Christi West Refinery", "type": "EMISSIONS EVENT", "unit": "Udex Unit", "cause": "Leak from temporary decommissioning pump during planned maintenance", "fence_line": {"LEL": 0, "VOC_ppm": 0, "H2S_ppm": 0, "CO_ppm": 0, "SO2_ppm": 0, "Benzene_ppm": 0}, "severity": "Baja - Contenido - Sin shutdown unidad"},
        "venezuela": {"opec_sep_kbd": 1206, "secondary_kbd": 1150, "reuters_oct_kbd": 860, "pdvsa_claim_kbd": 1252},
        "natgas": {"bcf": 3801, "injection": 77, "vs_5y": 54},
        "colombia": {"oil_bpd": 729593, "oil_yoy": -2.92, "gas_mmcfd": 705, "gas_yoy": -13.39},
        "risk": {"mode": "BUNKER", "lock": "0.30x", "dry_powder": "100%", "exposure": "0.22x", "var": "1.68%", "executions": 0},
        "breaking": "DOSSIER ROBUSTO M82 INTEGRADO - SAUDI ARAMCO + REFINITIV + BUNKER 0.30x LOCK",
        "alerts": ["NO DISPARAR - Webhooks inactivos en BUNKER - estado esperado"]
    }
    while True:
        broadcast(patch)
        time.sleep(60)
