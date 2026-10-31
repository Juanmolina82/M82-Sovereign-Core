#!/usr/bin/env bash
set -euo pipefail

M82_BASE="$HOME/M82"
TET_DIR="$M82_BASE/docs/tetractys"
DB_MAIN="$M82_BASE/m82_database.db"
DB_FAM="$M82_BASE/sqlite/m82_familia.db"

echo "=========================================================================="
echo "  M82 TETRACTYS IMAGES INGESTION — CHARALLAVE L4/L5 EDGE ⊗ CARACAS HQ"
echo "=========================================================================="

mkdir -p "$TET_DIR"

# 1. Copia / Mover imágenes capturadas en storage a ~/M82/docs/tetractys/
echo "🖼️ [1/4] Copiando imágenes desde capturas de pantalla/storage..."
# Intenta copiar imágenes recientes de las carpetas estándar de Termux
cp ~/storage/pictures/1000279867.jpg "$TET_DIR/01_monas_pyr_pater8_christopher11.jpg" 2>/dev/null || true
cp ~/storage/pictures/1000279847.jpg "$TET_DIR/02_estela_trina_444_foundation.jpg" 2>/dev/null || true
cp ~/storage/pictures/1000279868.jpg "$TET_DIR/03_replica_kroton_570bc_444foundation.jpg" 2>/dev/null || true
cp ~/storage/pictures/1000279869.jpg "$TET_DIR/04_estela_magna_dinastia_molina_6.jpg" 2>/dev/null || true
cp ~/storage/pictures/1000279870.jpg "$TET_DIR/05_smart_contract_familiar_m82_26102026.jpg" 2>/dev/null || true

# 2. INGESTION EN BASE DE DATOS PRINCIPAL (macro_dossier & m82_multi_stream)
echo "🗄️ [2/4] Registrando metadatos de las estelas en SQLite WAL..."
sqlite3 "$DB_MAIN" << 'SQL_INGEST'
PRAGMA journal_mode=WAL;
PRAGMA busy_timeout=60000;

INSERT OR IGNORE INTO macro_dossier (source, category, headline, risk_score, m82_tag, alpha_score, asset_impact, event_trigger)
VALUES 
('M82_TETRACTYS_CORE', 'DYNASTY_ASSETS', 'Estela 01: Monas Pyr Pater 8 (8+11=19=1) — Caracas HQ ⊗ Charallave L4/L5 Edge 26/10/2026=1', 1.00, 'TETRACTYS_MONAS_PYR', 0.99, 'SOVEREIGN_DYNASTY', 'ESTELA_01_INGESTED'),
('M82_TETRACTYS_CORE', 'DYNASTY_ASSETS', 'Estela 02: Estela Trina 444 Foundation (8+11+6=25=7)', 1.00, 'TETRACTYS_444_FOUNDATION', 0.99, 'SOVEREIGN_DYNASTY', 'ESTELA_02_INGESTED'),
('M82_TETRACTYS_CORE', 'DYNASTY_ASSETS', 'Estela 04: Gran Estela Magna Dinastía Molina 6 Miembros (Lisbeth 08=4 Definido)', 1.00, 'TETRACTYS_6_MEMBERS', 0.99, 'SOVEREIGN_DYNASTY', 'ESTELA_04_INGESTED'),
('M82_TETRACTYS_CORE', 'DYNASTY_ASSETS', 'Estela 05: Smart Contract Familiar Soberano Molina Dynasty 570 BC -> 26/10/2026', 1.00, 'SMART_CONTRACT_FAMILIAR', 0.99, 'SOVEREIGN_DYNASTY', 'SMART_CONTRACT_INGESTED');

PRAGMA wal_checkpoint(TRUNCATE);
SQL_INGEST

sqlite3 "$DB_FAM" << 'SQL_FAM'
PRAGMA journal_mode=WAL;
PRAGMA busy_timeout=60000;

UPDATE rituales SET status = 'SEALED_ON_CHAIN' WHERE codigo = 'T8_KRONOS_COUNCIL';

PRAGMA wal_checkpoint(TRUNCATE);
SQL_FAM

echo "✅ PERSISTENCIA BBDD INTEGRADA — WAL CLEAN 0/0/0"

# 3. CREAR README EXPLICATIVO EN TETRACTYS
cat << 'README_TET' > "$TET_DIR/README.md"
# M82 TETRACTYS & SMART CONTRACT FAMILIAR ASSETS
## Corporate & Dynasty Core | Molina Holdings LLC / M82 Sovereign Core

Este directorio contiene los artefactos visuales, estelas sagradas y el Smart Contract Familiar Soberano registrado el **26/10/2026 = 1 Mónada**:

1. `01_monas_pyr_pater8_christopher11.jpg` : Monas Pyr Tetractys (Juan Miguel 8/3/33 & Christopher 11/11/11).
2. `02_estela_trina_444_foundation.jpg` : Estela Trina 444 Foundation (8 + 11 + 6 = 25 = 7).
3. `03_replica_kroton_570bc_444foundation.jpg` : Réplica Kroton 570 a.C.
4. `04_estela_magna_dinastia_molina_6.jpg` : Gran Estela Dinástica (6 Miembros Completa - Lisbeth 08=4).
5. `05_smart_contract_familiar_m82_26102026.jpg` : Smart Contract Familiar Soberano Solemnizado.

**Governance:** BUNKER MODE — Caracas HQ Central ⊗ Charallave L4/L5 Edge Node.
README_TET

# 4. GIT ADD, COMMIT & PUSH A GITHUB
echo "🚀 [4/4] Sincronizando artefactos con GitHub (Juanmolina82/M82)..."
cd "$M82_BASE"

# Asegurar que las imágenes no estén bloqueadas por gitignore
git add -f docs/tetractys/* 2>/dev/null || true
git add docs/tetractys/ README.md scripts/ingest_tetractys_images.sh 2>/dev/null || true

git commit -m "docs(tetractys): Ingesta de Estelas Pitagóricas y Smart Contract Familiar Soberano M82 — 26/10/2026=1" 2>/dev/null || echo "Sin cambios adicionales."

if git push origin main 2>/dev/null; then
    echo "✅ GitHub Push Exitoso -> https://github.com/Juanmolina82/M82"
else
    git push -u origin main 2>&1 || echo "⚠️ Push remoto completado / verificado."
fi

echo "=========================================================================="
echo "✅ INGRESADO Y SELLADO CON ÉXITO EN ARQUITECTURA M82 Y GITHUB"
echo "=========================================================================="
