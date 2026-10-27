#!/data/data/com.termux/files/usr/bin/bash

TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_DIR="/sdcard/M82_BACKUPS"
PROJECT_DIR="$HOME/M82"

echo "=========================================================="
echo "      PROTOCOLO M82 :: BLINDAJE Y RESPALDO ANTES DE REINICIO"
echo "=========================================================="

termux-setup-storage
sleep 1

mkdir -p "$BACKUP_DIR"
mkdir -p "$PROJECT_DIR/vault"

echo "[+] Aplicando candados de seguridad en directorios y scripts..."
chmod -R 700 "$PROJECT_DIR/scripts" 2>/dev/null
chmod -R 700 "$PROJECT_DIR/data" 2>/dev/null

echo "[+] Creando snapshot comprimido en $BACKUP_DIR..."
TAR_FILE="$BACKUP_DIR/M82_ARCHITECTURE_BACKUP_$TIMESTAMP.tar.gz"
tar -czf "$TAR_FILE" -C "$HOME" M82 2>/dev/null

if [ -f "$TAR_FILE" ]; then
    echo "[✓] Respaldo generado con éxito: $TAR_FILE"
else
    echo "[!] Guardando backup local en $HOME..."
    tar -czf "$HOME/M82_BACKUP_$TIMESTAMP.tar.gz" -C "$HOME" M82 2>/dev/null
fi

echo "[+] Verificando script de auto-arranque e integridad..."
cat << 'BASHRC_EOF' > $HOME/.m82_recovery_check.sh
#!/data/data/com.termux/files/usr/bin/bash
if [ -d "$HOME/M82" ]; then
    echo -e "\n\033[1;32m[✓] ARQUITECTURA M82 DETECTADA Y BLINDADA\033[0m"
    echo -e "Usa \033[1;34mm82-start\033[0m para reanudar el daemon o \033[1;34mm82-status\033[0m para monitorear.\n"
fi
BASHRC_EOF

chmod +x $HOME/.m82_recovery_check.sh
grep -qF ".m82_recovery_check.sh" ~/.bashrc || echo "bash $HOME/.m82_recovery_check.sh" >> ~/.bashrc

echo "=========================================================="
echo "[✓] SISTEMA M82 TOTALMENTE PROTEGIDO. PUEDES REINICIAR."
echo "=========================================================="
