#!/data/data/com.termux/files/usr/bin/bash
export TMPDIR=$PREFIX/tmp
python3 ~/M82/scripts/m82_wallstreet_master.py >> ~/M82/logs/wallstreet.log 2>&1
bash ~/M82/scripts/m82_github_blindaje.sh >> ~/M82/logs/github.log 2>&1
LATEST=$(ls -t ~/M82/m82_wallstreet_master_*.xlsx 2>/dev/null | head -1)
echo "M82 WALLSTREET DAEMON $(date -u +%Y-%m-%dT%H:%M:%SZ) — 10 equities — AAPL $222.91 Target $245.50 — File $(basename $LATEST) — BUNKER 0.30x LOCK" | bash ~/M82/scripts/ntfy_dedup_wrapper.sh
