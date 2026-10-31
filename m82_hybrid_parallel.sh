#!/usr/bin/env bash
set -e

M82_DIR="$HOME/M82"
DB_PATH="$M82_DIR/m82_database.db"
CARDS_DIR="$HOME/storage/shared/Pictures/M82_Cards"
if [ ! -d "$CARDS_DIR" ]; then
    CARDS_DIR="/sdcard/Pictures/M82_Cards"
fi

OUTPUT_TXT="$M82_DIR/m82_consolidated_summary.txt"

echo "=========================================================="
echo "    M82 SOVEREIGN EDGE :: MOTOR HÍBRIDO PARALELO (WAL)   "
echo "=========================================================="

# 1. Asegurar persistencia y CPU en background
termux-wake-lock 2>/dev/null || true

# 2. Generar utilitario de extracción desde SQLite WAL (Paralelo a la BD)
echo "📂 [1/3] Extrayendo streaming activo directo desde SQLite..."
sqlite3 "$DB_PATH" << EOF_SQL > "$OUTPUT_TXT"
.headers on
.mode column
PRAGMA busy_timeout=60000;

SELECT '========================================================' AS Header;
SELECT '   M82 CONSOLIDATED STREAMING DOSSIER (SQLITE WAL)     ' AS Header;
SELECT '========================================================' AS Header;

SELECT id, daemon_source, headline, status, created_at 
FROM m82_multi_stream 
ORDER BY id DESC 
LIMIT 150;
EOF_SQL

# 3. Generar el consolidador OCR para tarjetas HUD físicas (Paralelo a las Imágenes)
cat << 'PY_OCR' > "$M82_DIR/m82_ocr_extractor.py"
#!/usr/bin/env python3
import os, glob
from PIL import Image

try:
    import pytesseract
    HAS_OCR = True
except ImportError:
    HAS_OCR = False

CARDS_DIR = os.path.expanduser("/sdcard/Pictures/M82_Cards")
if not os.path.exists(CARDS_DIR):
    CARDS_DIR = os.path.expanduser("~/storage/shared/Pictures/M82_Cards")

OUTPUT_FILE = os.path.expanduser("~/M82/m82_cards_ocr_summary.txt")

images = glob.glob(os.path.join(CARDS_DIR, "*.png"))
print(f"🔍 [OCR Parallel] Analizando {len(images)} tarjetas HUD visuales...")

with open(OUTPUT_FILE, "w", encoding="utf-8") as out:
    out.write("========================================================\n")
    out.write("   M82 HUD CARDS OCR EXTRACTED DOSSIER                 \n")
    out.write("========================================================\n\n")
    
    for idx, img_path in enumerate(sorted(images, key=os.path.getmtime, reverse=True), 1):
        filename = os.path.basename(img_path)
        out.write(f"--- [CARD #{idx} :: {filename}] ---\n")
        if HAS_OCR:
            try:
                txt = pytesseract.image_to_string(Image.open(img_path))
                out.write(txt.strip() + "\n\n")
            except Exception as e:
                out.write(f"[Error procesando OCR: {e}]\n\n")
        else:
            out.write(f"[Imagen detectada en ruta: {img_path} | Tesseract no instalado]\n\n")

print(f"✅ Extracción de tarjetas completada en: {OUTPUT_FILE}")
PY_OCR

chmod +x "$M82_DIR/m82_ocr_extractor.py"

# 4. Ejecutar extractor de imágenes sin interrumpir daemons
echo "🖼️ [2/3] Procesando tarjetas PNG en paralelo..."
python3 "$M82_DIR/m82_ocr_extractor.py" || true

# 5. Generar archivo unificado listo para copiar
CAT_UNIFIED="$M82_DIR/M82_MACRO_MASTER_PACK.txt"
cat "$OUTPUT_TXT" "$M82_DIR/m82_cards_ocr_summary.txt" 2>/dev/null > "$CAT_UNIFIED"

echo "=========================================================="
echo "✅ INFRAESTRUCTURA MANTENIDA INTACCTA EN SEGUNDO PLANO."
echo "✅ ARCHIVO UNIFICADO GENERADO:"
echo "   📄 RUTA: $CAT_UNIFIED"
echo "=========================================================="
