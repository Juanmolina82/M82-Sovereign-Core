#!/data/data/com.termux/files/usr/bin/bash
cd ~/M82
git add m82_database.db lseg_*.csv logs/*.log m82_*.py scripts/*.sh 2>/dev/null
git commit -m "M82 AUTO-BLINDAJE $(date -u +%Y-%m-%dT%H:%M:%SZ) — $20.12B 33ev PID 24606 — BUNKER 0.30x — Warsh 102bps" 2>/dev/null || true
git push origin main 2>/dev/null || true
