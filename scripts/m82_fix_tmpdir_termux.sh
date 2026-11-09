#!/data/data/com.termux/files/usr/bin/bash
set -e
# FIX TERMUX TMPDIR — Standard para Android RO filesystem
# 1. Crear tmp en sandbox Termux — path escribible garantizado
mkdir -p $PREFIX/tmp
mkdir -p $HOME/M82/logs
chmod 700 $PREFIX/tmp

# 2. Exportar TMPDIR para sesión actual
export TMPDIR=$PREFIX/tmp
export TMP=$PREFIX/tmp
export TEMP=$PREFIX/tmp

# 3. Persistir en .bashrc + .zshrc + profile — para futuras sesiones
grep -q "TMPDIR=\$PREFIX/tmp" ~/.bashrc 2>/dev/null || echo 'export TMPDIR=$PREFIX/tmp' >> ~/.bashrc
grep -q "TMPDIR=\$PREFIX/tmp" ~/.bashrc 2>/dev/null || echo 'export TMP=$PREFIX/tmp' >> ~/.bashrc
grep -q "TMPDIR=\$PREFIX/tmp" ~/.bashrc 2>/dev/null || echo 'export TEMP=$PREFIX/tmp' >> ~/.bashrc

# 4. Persistir en Termux properties
echo "export TMPDIR=$PREFIX/tmp" > $HOME/.termux/tmpdir 2>/dev/null || true

# 5. Actualizar scripts M82 para usar TMPDIR en lugar de /tmp hardcodeado
sed -i "s|/tmp/m82_|${TMPDIR:-$PREFIX/tmp}/m82_|g" ~/M82/m82_supervisor.sh 2>/dev/null || true
sed -i "s|/data/data/com.termux/files/usr/tmp|${TMPDIR:-$PREFIX/tmp}|g" ~/M82/scripts/*.sh 2>/dev/null || true
sed -i "s|/data/data/com.termux/files/usr/tmp/cron|${TMPDIR:-$PREFIX/tmp}/cron|g" ~/M82/scripts/*.sh 2>/dev/null || true

# 6. Verificación
echo "TMPDIR=$TMPDIR"
echo "PREFIX/tmp exists: $(ls -ld $PREFIX/tmp)"
echo "M82 logs path: $HOME/M82/logs/cron.tmp"
ls -lh $PREFIX/tmp/ | tail -5
echo "crontab -l:"
crontab -l | grep -E "dual|earnings|github|weekly" || echo "crontab vacío — ejecutar fix cron earnings"
