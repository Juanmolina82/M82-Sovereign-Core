import os, json, time

DATA_PATH = os.path.expanduser("~/M82/app/data.json")

payload = {}
if os.path.exists(DATA_PATH):
    try:
        with open(DATA_PATH, "r") as f:
            payload = json.load(f)
    except Exception:
        payload = {}

patch = {
    "wire": "M82 WIRE: NVDA Korea UPDATE 1 (9 Nov) — 10K GPUs delivered, 2026 contracted lots unaffected despite Huang probe",
    "nvda_huang_dossier": {
        "timestamp": time.strftime("%H:%M:%S VET"),
        "event": "NVIDIA_HUANG_PROBE_KOREA_UPDATE1",
        "source": "REUTERS_SEOUL_NVIDIA-PROBE/CEO-SOUTHKOREA_UPDATE1",
        "korea_statement": "Contracted GPU production/delivery unaffected",
        "gpus_delivered_2025": "10,000 GPUs delivered via 2025 supplementary budget, in use",
        "gpus_2026": "Contracted, expected delivery 2026, in use this year per ministry",
        "official": "Vice Minister Ryu Je-myeong, Ministry of Science and ICT",
        "board_position": "No reason to believe US national security or NVDA confidential info leaked",
        "jensen_position": "Full cooperation with independent investigation",
        "madison_huang": "Cancelled Korea visit",
        "nvidia_ai_day_seoul": "Proceeding as planned, ~2,000 participants, Physical AI / Agentic AI / Infra",
        "status": "NVDA_INVESTIGATION_OPEN_SUPPLY_UNAFFECTED_KOREA"
    }
}

payload.update(patch)
payload["timestamp"] = time.strftime("%H:%M:%S VET")

tmp = DATA_PATH + ".tmp"
with open(tmp, "w") as f:
    json.dump(payload, f, indent=2)
os.replace(tmp, DATA_PATH)
print("[MERGE OK] Vector NVDA Korea UPDATE 1 inyectado sin tocar OBS.")
