#!/data/data/com.termux/files/usr/bin/bash
# M82 GITHUB AUTO-SYNC :: HQ CARACAS ⊗ CHARALLAVE EDGE
set -e

CD_DIR="$HOME/M82"
cd "$CD_DIR"

git config user.name "Juan M. Molina"
git config user.email "chairman@m82.caracas.hq"

# 1. Documento Maestro README.md
cat > README.md << 'MD'
# M82 QUANTUM TERMINAL — SOVEREIGN EXECUTION CORE

**Executive Authority:** Chairman Juan M. Molina (Molina Holdings LLC)
**HQ Principal:** CARACAS — M82 SOVEREIGN CORE (BUNKER MODE 0.30x LOCK)
**Active Edge Node:** CHARALLAVE L4/L5 — Termux Sovereign Edge
**PID Context:** 4692 — LSEG Workspace / Refinitiv Telemetry
**Firmware:** `M82_DOSSIER_ROBUSTO_24OCT26`

---

## Topología & Risk Governance
- **Bunker Posture:** `0.30x LOCK` (Active Exposure: 0.22x | VaR Daily: 1.68% | Warsh Spread: +102.0 bps)
- **Database Engine:** SQLite3 WAL Mode (`PRAGMA busy_timeout=60000;`)
- **Telemetry Cadence:** 60s Dispatcher | Anti-Daneka Filter ($\text{Alpha Score} \ge 0.85$)
- **Endpoints:** PWA Surface `:8080` / WSGI API `:8083` (60 FPS Streaming)

---

## M82 Dossier Robusto — Master Synthesis (PID 4692)
1. **Monetario:** BCV $7.15BN YTD vs Binance P2P $5.9BN (83% liquidez real BCV).
2. **Petrolero (Auditoría Campo):** NABEP 115k bpd real vs 200k claim (42.5% inflado).
3. **Eléctrico:** Deficiencia estructural Derwick en Zulia/Maracaibo ($10-15BN requerimiento grid).
4. **Financiamiento:** Qatar $2BN Bridge → Pago Deuda BID → $2.5BN Nuevo Préstamo Grid.
5. **Geopolítica / Off-Hormuz Hedge:** Memo DNI Clayton (23 Oct). Plots letales Irán + Houthis Hormuz (20% crudo mundial). US requiere Merey $93.92 FOB Caribe off-Hormuz @ $30 Barbados.
6. **Gobernanza:** Oxígeno político 18M sin fecha electoral.

---
*Signature:* `M82_DOSSIER_ROBUSTO_24OCT26 — HQ CARACAS — Edge Charallave`
MD

cat > .gitignore << 'GI'
m82_database.db*
*.db-wal
*.db-shm
logs/
cards/*.png
.env
GI

# 2. Asentamiento Git Local & Push
if [ ! -d ".git" ]; then
    git init
    git branch -M main
fi

git add README.md .gitignore setup.sh boot.sh orch.py init_db.py 2>/dev/null || git add .
git commit -m "M82_DOSSIER_ROBUSTO_24OCT26 — HQ CARACAS ⊗ Edge Charallave — PID4692 — BUNKER 0.30x" || echo "Sin cambios para commitear."

echo "🚀 Sincronizando con GitHub (Juanmolina82/M82)..."
if command -v gh &> /dev/null && gh auth status &> /dev/null; then
    gh repo create M82 --public --source=. --remote=origin --push 2>/dev/null || git push -u origin main
else
    echo "⚠️ 'gh' no autenticado. Ejecute 'gh auth login' en Termux para vincular con github.com/Juanmolina82/M82."
fi

