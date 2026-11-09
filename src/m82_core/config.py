import os
from pathlib import Path
from dotenv import load_dotenv

# Bóveda institucional
ENV_PATH = Path.home() / ".m82_secrets" / "m82.env"
load_dotenv(dotenv_path=ENV_PATH, override=True)

# M82_WIRE
M82_WIRE_APP_KEY = os.getenv("M82_WIRE_APP_KEY")
M82_WIRE_CLIENT_ID = os.getenv("M82_WIRE_CLIENT_ID")
M82_WIRE_CLIENT_M82_MACRORET = os.getenv("M82_WIRE_CLIENT_M82_MACRORET")
SXS_BRIDGE_URL = os.getenv("SXS_BRIDGE_URL", "http://127.0.0.1:8080")
GATEWAY_URL = os.getenv("GATEWAY_URL", "http://127.0.0.1:8081")

# Telegram - unifica ambas convenciones
BOT_TOKEN = os.getenv("M82_BOT_TOKEN") or os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("M82_CHAIRMAN_ID") or os.getenv("TELEGRAM_CHAT_ID")

# Institucional
INSTITUTION = "Molina Holdings LLC / Molina Global LLC"
NODE = "CARACAS"
RUNTIME = Path.home() / "M82" / "runtime"
