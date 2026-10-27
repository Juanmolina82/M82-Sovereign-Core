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
