import os, json, time
DATA_PATH = os.path.expanduser("~/M82/app/data.json")
payload = {}
if os.path.exists(DATA_PATH):
    try:
        with open(DATA_PATH) as f: payload = json.load(f)
    except Exception: payload = {}

patch = {
    "wire": "M82 WIRE: NVDA UPDATE 6 (9 Nov) - Shares -8% Mon, ~$350B wiped, probe on Huang, Korea supply unaffected, earnings 17 Nov / House briefing 18 Nov",
    "nvda_huang_dossier": {
        "timestamp": time.strftime("%H:%M:%S VET"),
        "event": "NVIDIA_HUANG_PROBE_UPDATE6_MARKET_SHOCK",
        "source": "REUTERS_NVIDIA-PROBE/CEO_UPDATE6_PIX_TV_9NOV",
        "market_move": "NVDA -8% early trading Mon 9 Nov, multi-month lows, ~$350B market value loss",
        "prior_selloff": "Extends last week AI selloff",
        "asia_suppliers": "TSMC +4.7%, Samsung +0.6%, SK Hynix +0.4% Mon - supply chain decoupled from CEO risk",
        "huang_admission": "Told employees he was unfaithful to his wife, no details disclosed",
        "madison_huang": "Cancelled Seoul visit to Rebellions + Kakao Mobility Q&A, unavoidable internal circumstances",
        "nvidia_ai_day_seoul": "Proceeding, ~2,000 participants",
        "board_position": "Confidence in Huang, independent investigation open, no reason to believe US national security or NVDA secrets leaked",
        "huang_stake": "~3.6% NVDA, 5th largest shareholder, flat structure, no natural successor, no dual-class",
        "trump_position": "Fine person, honourable guy, briefed ~1 year ago, chose not to act",
        "musk_ackman": "Ackman: hoping simple affair not national security risk. Musk: agrees Jensen irreplaceable for US AI leadership but did something incredibly dumb",
        "china_position": "Guo Jiakun: groundless accusation, slander, smear",
        "analyst_risk": "NH Investment Ryu Young-ho: prolonged probe could delay NVDA investment decisions / launches, affect memory chip prices, AMD could gain short-term attention, NVDA products hard to replace",
        "korea_supply": "10,000 GPUs 2025 delivered and in use, 2026 contracted lots unaffected",
        "key_dates": "Earnings 17 Nov / House closed-door briefing 18 Nov / Huang RSVP due 11 Nov",
        "status": "NVDA_INVESTIGATION_OPEN_MARKET_SHOCK_MINUS8PCT"
    }
}
payload.update(patch)
payload["timestamp"] = time.strftime("%H:%M:%S VET")
tmp = DATA_PATH + ".tmp"
with open(tmp, "w") as f: json.dump(payload, f, indent=2)
os.replace(tmp, DATA_PATH)
print("[MERGE OK] NVDA UPDATE 6 inyectado.")
