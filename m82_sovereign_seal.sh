#!/usr/bin/env bash
# ==============================================================================
# M82 V60.3.1 CITADEL :: LEGAL IP SEAL & SOVEREIGN VAULT BINDING
# Molina Holdings | Caracas L4/L5 Sovereign Node
# ==============================================================================

set -e
M82_DIR="$HOME/M82"
cd "$M82_DIR"

echo "🛡 [M82 SOVEREIGN SEAL] Iniciando proceso de sellado de propiedad intelectual..."

# 1. Permisos estrictos de bóveda privada
chmod 700 "$M82_DIR"
[ -f "$M82_DIR/m82_database.db" ] && chmod 600 "$M82_DIR/m82_database.db"
[ -f "$M82_DIR/.m82_vault.json" ] && chmod 600 "$M82_DIR/.m82_vault.json"

# 2. Generar Sello SHA-256 Inmutable
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
HASH_SEAL=$(sha256sum "$M82_DIR/orch.py" "$M82_DIR/m82_verifier.py" 2>/dev/null | sha256sum | awk '{print $1}')

echo "M82 V60.3.1 CITADEL GRADE - HASH: $HASH_SEAL - $TIMESTAMP - Molina Holdings Caracas L5" > "$M82_DIR/.m82_ip_seal.txt"
chmod 400 "$M82_DIR/.m82_ip_seal.txt"

# 3. Inicializar / Actualizar Git Repositorio Local de Autoría
if [ ! -d "$M82_DIR/.git" ]; then
    git init "$M82_DIR" > /dev/null 2>&1
    git -C "$M82_DIR" config user.name "Molina Holdings"
    git -C "$M82_DIR" config user.email "sovereign@molinaholdings.local"
fi

git -C "$M82_DIR" add orch.py m82_verifier.py .m82_ip_seal.txt > /dev/null 2>&1 || true
git -C "$M82_DIR" commit -m "M82 V60.3.1 CITADEL GRADE - Sello Soberano IP - $TIMESTAMP" > /dev/null 2>&1 || true

# 4. Generar Certificado Propietario en Disco
cat << EOF_LIC > "$M82_DIR/LICENSE_M82_PROPIETARIA"
==============================================================================
M82 QUANTUM TERMINAL - PROPIEDAD INTELECTUAL PRIVADA
==============================================================================
Titular de Autoría : Molina Holdings / Nodo Caracas L4/L5
Versión Core       : V60.3.1 CITADEL GRADE
Fecha de Certificado: $TIMESTAMP
Ubicación Hardware : Edge Node Caracas, Miranda, Venezuela
Estado Legal       : USO PRIVADO SOBERANO - Prohibida distribución/reproducción
Sello Criptográfico: $HASH_SEAL
==============================================================================
EOF_LIC

chmod 400 "$M82_DIR/LICENSE_M82_PROPIETARIA"

echo "✅ [SELLO COMPLETADO] Tu propiedad intelectual ha sido blindada."
echo "📜 Sello Criptográfico: $HASH_SEAL"
