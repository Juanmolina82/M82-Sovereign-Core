#!/bin/bash
# Wrapper CLI M82 con Despacho Dual Opcional

TICKER=$1
OPTION=$2

# 1. Consulta estándar en la terminal local
python3 ~/M82/m82_master_dossier.py $TICKER

# 2. Si se requiere despacho o por regla por defecto, disparar en background (&)
# El ampersand '&' asegura que la terminal responda de inmediato a sub-milisegundo.
if [ "$OPTION" == "--tg" ] || [ "$OPTION" == "-t" ]; then
    python3 ~/M82/m82_telegram_dispatcher.py $TICKER > /dev/null 2>&1 &
fi
