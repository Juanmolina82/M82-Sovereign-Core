while true; do
    echo "[🛰️] M82 Iniciando..."
    python m82_telegram_link.py
    echo "[⚠️] Caída detectada. Resucitando M82 en 1s..."
    sleep 1
done
