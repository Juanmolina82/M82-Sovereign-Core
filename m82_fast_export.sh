#!/usr/bin/env bash
DB_PATH="$HOME/M82/m82_database.db"
OUTPUT_PACK="$HOME/M82/M82_MACRO_MASTER_PACK.txt"

echo "=========================================================="
echo "   M82 INSTANT SQL EXPORT :: DOSSIER REFINITIV / LSEG     "
echo "=========================================================="

sqlite3 "$DB_PATH" << 'EOF' > "$OUTPUT_PACK"
.headers on
.mode column
PRAGMA busy_timeout=60000;

SELECT '========================================================' AS Header;
SELECT '   M82 CONSOLIDATED STREAMING DOSSIER (ULTIMOS 200)    ' AS Header;
SELECT '========================================================' AS Header;

SELECT id, daemon_source, headline, status, created_at 
FROM m82_multi_stream 
ORDER BY id DESC 
LIMIT 200;

SELECT '========================================================' AS Header;
SELECT '   MACRO DOSSIER AUDIT TRAIL                           ' AS Header;
SELECT '========================================================' AS Header;

SELECT id, source, headline, risk_score, timestamp 
FROM macro_dossier 
ORDER BY id DESC 
LIMIT 100;
EOF

echo "✅ ARCHIVO GENERADO EN 1 SEGUNDO: $OUTPUT_PACK"
echo "=========================================================="
