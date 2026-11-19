#!/bin/bash
# M82 Wall Street Scanner - Silent - jmmp@molina82.com
# NO TOCA PID 10448 - Corre DESPUES de CPI

cd ~/M82
python3 << 'PYEOF'
import refinitiv.data as rd
import os

rd.open_session()

universo = [".SPX", ".VIX", ".DXY", "US10YT=RR", "ESc1", "USCPIC=ECI"]

data = rd.get_data(
    universe=universo,
    fields=["CF_LAST", "CF_OPEN", "CF_HIGH", "CF_LOW", "CF_VOLUME"]
)
print(data)
msg = f"M82 SCANNER\n{data.to_string(index=False)}"

# Telegram SILENCIOSO
import requests
requests.post(
    f"https://api.telegram.org/bot{os.getenv('TELEGRAM_BOT_TOKEN')}/sendMessage",
    json={"chat_id": os.getenv('TELEGRAM_CHAT_ID'), "text": msg, "disable_notification": True}
)
# ntfy SILENCIOSO
requests.post(
    "https://ntfy.sh/m82_molina",
    data=msg.encode('utf-8'),
    headers={"Priority": "default", "Title": "M82 Scanner"}
)
# Local SILENCIOSA
os.system(f"termux-notification --title 'M82 Scanner' --content 'SPX VIX DXY 10Y ES CPI listo' --priority low --alert-once")
rd.close_session()
PYEOF
