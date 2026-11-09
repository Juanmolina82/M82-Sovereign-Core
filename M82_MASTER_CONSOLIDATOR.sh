#!/usr/bin/env bash
set -e

BASE_DIR="$HOME/M82"
BACKUP_DIR="$BASE_DIR/backups"
DB_PATH="$BASE_DIR/m82_database.db"
DOSSIER_PATH="$BASE_DIR/dossier_140_master.json"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")

echo "================================================================================"
echo " 🛡️ INICIANDO CONSOLIDACIÓN MAESTRA Y BLINDAJE DE ARQUITECTURA M82"
echo "================================================================================"

# 1. Crear directorio de backups de alta redundancia
mkdir -p "$BACKUP_DIR"

# 2. Checkpoint SQLite WAL para forzar el volcado de memoria a disco
echo " [1/4] Ejecutando Checkpoint SQLite WAL en m82_database.db..."
sqlite3 "$DB_PATH" "PRAGMA wal_checkpoint(FULL);"

# 3. Generar respaldo físico comprimido de la BBDD y el entorno
echo " [2/4] Generando backup de alta integridad en ~/M82/backups/..."
cp "$DB_PATH" "$BACKUP_DIR/m82_database_backup_$TIMESTAMP.db"
sqlite3 "$DB_PATH" .dump > "$BACKUP_DIR/m82_database_dump_$TIMESTAMP.sql"

# 4. Consolidación de Dossier #140 en JSON Maestro
echo " [3/4] Generando Dossier #140 Master (Houston G20 + TSLA Tri-Vector)..."
cat << 'JSON_EOF' > "$DOSSIER_PATH"
{
    "dossier_metadata": {
        "dossier_id": 140,
        "classification": "RESERVED_MACRO_FINANCIAL_DOSSIER",
        "node_id": "Nodo Caracas (M82)",
        "created_at": "2026-10-07",
        "status": "ACTIVE_SURVEILLANCE_PRE_FOMC"
    },
    "core_thesis_venalum_fuga_fiscal": {
        "target_asset": "CVG Venalum / Bauxilum / Guri Energy Matrix",
        "risk_score": 8.5,
        "enabling_framework": "Marco Vicepresidencia / Min. Economía y Finanzas (L. Rodríguez)",
        "entity_counterparty": "Mercuria Energy Group Ltd (Dubai) / Heeney Capital JV",
        "mechanism": "Arbitraje de Estructura Contractual (Tolling Offshore vs. Retención Onshore)",
        "value_capture_flow": [
            "1. Pre-financiamiento offshore de insumos críticos (alúmina, ánodos, coke) + CAPEX celdas.",
            "2. Registro de pasivo comercial directo en balance contable de Venalum.",
            "3. Offtake fijado con descuento 15-30% bajo LME + Structuring Fee offshore.",
            "4. Subvención/Consumo de energía hundida del Guri (~$5-10/MWh); valor monetizado en SPV Dubái/Zug.",
            "5. Liquidación neta hacia el Tesoro Nacional (TGN) después de tolling; renta descontada en origen."
        ],
        "houston_g20_lever": "Cláusula de reversión de margen onshore obligatoria para licenciamiento/operatividad."
    },
    "market_surveillance_matrix": {
        "master_ticker": "TSLA",
        "role": "Nodo de Transmisión Tri-Vectorial (BTC / NVDA-TSM CAPEX / xAI-Musk Cross-Drain)",
        "leading_indicators": ["TSM", "NVDA"],
        "beta_control": "QQQ",
        "private_liquidity_proxy": "SPCX",
        "transmission_mechanics": {
            "vector_1_btc": "Mark-to-market directo en balance corporativo -> liquidez real.",
            "vector_2_ai_capex": "Demanda marginal FSD/Dojo. Sensible al costo de chips NVDA/TSM.",
            "vector_3_musk_ecosystem": "Competencia de wafers TSM entre xAI y TSLA + drenaje de capital privado."
        }
    },
    "macro_triggers_log": [
        {"id": 32, "ticker": "CARDON_FIRE_20261006", "impact": "Cardón CRP Outage -> Crisis Diésel / Red Térmica"},
        {"id": 33, "ticker": "MERCURIA_REFINITIV_ENTITY", "impact": "Entidad Dubái Validada en Refinitiv Workspace"},
        {"id": 34, "ticker": "GLOBAL_HAWKISH_PIVOT", "impact": "RBI Rate Hike (4y) + BOJ Dissenter Signal + US10Y Acceleration"},
        {"id": 35, "ticker": "ABN_AMRO_STATE_EXIT", "impact": "ABN AMRO (ABNd.AS) Desinversión Estatal / Liquidez Bancaria Europea"}
    ]
}
JSON_EOF

# 5. Hacer copias inmutables de protección (Read-Only permisos)
chmod 444 "$DOSSIER_PATH"
chmod 444 "$BACKUP_DIR/m82_database_backup_$TIMESTAMP.db"

echo " [4/4] Verificando tablas SQLite consolidadas..."
sqlite3 "$DB_PATH" "SELECT 'Manual Notes Count:', COUNT(*) FROM m82_manual_notes;"
sqlite3 "$DB_PATH" "SELECT 'Daemons Registry Count:', COUNT(*) FROM m82_daemons_registry;"

echo "================================================================================"
echo " ✅ CONSOLIDACIÓN COMPLETADA EXITOSAMENTE Y BLINDADA A PRUEBA DE BORRADO"
echo " 📂 Backup DB: $BACKUP_DIR/m82_database_backup_$TIMESTAMP.db"
echo " 📂 SQL Dump:  $BACKUP_DIR/m82_database_dump_$TIMESTAMP.sql"
echo " 📂 JSON Master: $DOSSIER_PATH (Permisos 444 Read-Only)"
echo "================================================================================"
