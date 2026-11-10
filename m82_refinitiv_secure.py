import os
from pathlib import Path
# Lee .env sin librerias externas
env_path = Path.home() / "M82" / ".env"
if env_path.exists():
    for line in env_path.read_text().splitlines():
        if "=" in line and not line.startswith("#"):
            k,v = line.split("=",1)
            os.environ.setdefault(k.strip(), v.strip())
print(f"[SECURE OK] RDP User: {os.environ.get('REFINITIV_USER')}")
print(f"[SECURE OK] AppKey presente: {'SI' if os.environ.get('REFINITIV_APP_KEY') else 'NO'} - Nunca en Git")
