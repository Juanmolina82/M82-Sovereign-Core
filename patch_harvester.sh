#!/usr/bin/env bash
cd ~/M82 || exit 1

echo "========================================================================="
echo "   M82 SOVEREIGN CORE v63.0.01-A :: HARVESTER NORMALIZATION PARCHE BASH  "
echo "========================================================================="

# Backup de seguridad previo al parcheo de escala
cp m82_universal_daily_harvester.py m82_universal_daily_harvester.py.bak

# Inyección del Parche de Escala Normalizada en Python/Bash
python3 - << 'PYEOF'
import pathlib

p = pathlib.Path("m82_universal_daily_harvester.py")
txt = p.read_text()

old_code = "        val_a = spot if spot != 0 else 1.0"
new_code = """        # M82 PARCHE CRÍTICO v63.0.01-A - Normalización Dimensional de Vector
        # Se prohíbe el uso de precio nominal para evitar distorsión de escala
        if fcf_yield and float(fcf_yield) > 0:
            val_a = float(fcf_yield)
        elif ticker in ("XAU", "GOLD", "GC"):
            val_a = 7.79  # Gold/Silver Ratio (77.90 / 10)
        elif ticker in ("WTI", "BRENT", "CL"):
            val_a = 2.78  # Crack Spread normalizado
        elif ticker in ("HG", "COPPER"):
            val_a = 3.25  # Momentum Cobre normalizado
        elif fwd_pe and float(fwd_pe) > 0:
            val_a = 100.0 / float(fwd_pe)  # Earnings Yield Equivalent
        else:
            val_a = 2.78"""

if old_code in txt:
    txt = txt.replace(old_code, new_code)
    p.write_text(txt)
    print("\n[M82_BASH_PATCH] -> SUCCESS: Parche de Normalización 'val_a' aplicado con éxito.")
else:
    print("\n[M82_BASH_PATCH] -> WARNING: No se encontró la firma exacta. Verificando estado del archivo...")
PYEOF

chmod +x ~/M82/m82_universal_daily_harvester.py

echo -e "\n[VERIFICACIÓN BASH] -> Comprobación de líneas parcheadas en m82_universal_daily_harvester.py:"
grep -n -C 5 "val_a =" ~/M82/m82_universal_daily_harvester.py
