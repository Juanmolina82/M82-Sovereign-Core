#!/bin/bash
set -e
VPS_IP=$1
PG_PASS=${2:-M82QuantumSecure2026!}

if [ -z "$VPS_IP" ]; then
    echo "❌ Error: Falta la IP del VPS. Uso: bash migrate.sh <IP_VPS> [PASSWORD_PG]"
    exit 1
fi

echo "🚀 Migrando M82 a $VPS_IP..."

# 1. Crear Dump de SQLite comprimido
sqlite3 ~/M82/m82_database.db .dump | gzip > $HOME/M82/tmp/m82.sql.gz
echo "📦 Dump local comprimido generado en $HOME/M82/tmp/m82.sql.gz"

# 2. Transferir al VPS
scp $HOME/M82/tmp/m82.sql.gz root@$VPS_IP:/tmp/

# 3. Restaurar en PostgreSQL dentro del contenedor Docker
ssh root@$VPS_IP "zcat $HOME/M82/tmp/m82.sql.gz | docker exec -i m82_postgres psql -U molina_admin -d m82_desk"

echo "✅ Base de datos M82 migrada exitosamente a PostgreSQL en el VPS."
