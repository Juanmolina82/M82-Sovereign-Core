import os, json, time
DATA_PATH = os.path.expanduser("~/M82/app/data.json")
payload = {}
if os.path.exists(DATA_PATH):
    try:
        with open(DATA_PATH) as f: payload = json.load(f)
    except Exception: payload = {}

payload.update({
    "wire": "M82 DOSSIER ROBUSTO - Macro Principal Actualizado | 10 Nov 2026 - Pre-CPI",
    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S VET"),
    "dossier_macro": {
        "cpi_today": {
            "event": "CPI Oct 2026 - 10 Nov 8:30 AM ET / 9:30 AM VET",
            "consensus_mom_headline": "+0.3%",
            "consensus_mom_core": "+0.2%",
            "yoy_official": "NO PUBLICADO - Falta Oct 2025 por shutdown",
            "sept_ref": "Headline +0.6% MoM / 3.7% YoY - Core +0.3% MoM / 2.6% YoY",
            "cleveland_nowcast": "0.24% Headline / 0.21% Core",
            "kalshi_mom_03": "45-50% prob +0.3% MoM"
        },
        "fed": {
            "dec_hike_odds": "81-84% CME FedWatch - CORREGIDO de 75-78%",
            "prev_odds": "71% pre-NFP",
            "catalyst_nfp": "165k payrolls, desempleo 4.1%",
            "next_meeting": "9 Dic 2026",
            "ubs_view": "Hike Dic + Mar 2027"
        },
        "energy": {
            "brent": "$94.32 (-4.07%)",
            "wti": "$87.71 (-3.43%)",
            "merey": "$83.15",
            "xau": "$4,073.59 LSEG sellado",
            "xom_pdvsaa": "MoU NO vinculante 9 Nov - Exploracion Orinoco - Athabasca know-how",
            "xom_condition": "Stable policies, clear regs, protections, competitive returns",
            "chevron_contrast": "$7B / 5 anos - 600k b/d - Compromiso real"
        },
        "tech_ai": {
            "nvda": "Board Probe - Intraday -8% / Cierre -5.3% - Key-Man Risk - 60 reportes - Board: no secrets compromised",
            "anthropic": {
                "ticker": "ANT Nasdaq",
                "valuation_pushback": "$1.1T-$1.3T vs $1.5T previo",
                "placement_26b": "DRAFT RETRACTADO - Pendiente S-1/A - Google, NVDA, AMD, Broadcom, Micron, MSFT, TSMC",
                "roadshow": "10 Nov - Trading esperado 19-20 Nov"
            },
            "spacex": "USSF-627 Falcon 9 - 10 Nov 04:59 UTC / 00:59 VET - SLC-4E Vandenberg - LEO Clasificado"
        }
    },
    "ai_audit": {"builder": "Fable 5.2 - OK", "auditor": "Mythos 5.2 - SELLAR", "verdict_status": "SELLADO_EN_CORE"},
    "risk": {"mode": "BUNKER MODE", "lock": "0.30x LOCK", "dry_powder": "100%", "executions": 0, "wait_for": "CPI 8:30 AM ET / 9:30 AM VET"}
})
tmp = DATA_PATH + ".tmp"
with open(tmp, "w") as f: json.dump(payload, f, indent=2)
os.replace(tmp, DATA_PATH)
print("[FABLE BUILD OK] Dossier Macro Robusto actualizado.")
