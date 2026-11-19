#!/data/data/com.termux/files/usr/bin/bash
set -e

M82_DIR="$HOME/M82"
LLM_DIR="$M82_DIR/sovereign_llm"
MODELS_DIR="$LLM_DIR/models"
mkdir -p "$MODELS_DIR" "$M82_DIR/logs"

echo "=== [1/4] AUDITANDO MEMORIA RAM DEL NODO CHARALLAVE L4/L5 EDGE ==="
free -h
AVAIL_MB=$(free -m | awk '/^Mem:/ {print $7}')
[ -z "$AVAIL_MB" ] && AVAIL_MB=$(free -m | awk '/^Mem:/ {print $4}')
echo "[+] RAM Disponible detectada: ${AVAIL_MB} MB"

if [ "$AVAIL_MB" -ge 6000 ]; then
    MODEL_NAME="qwen2.5-7b-instruct-q4_k_m.gguf"
    MODEL_URL="https://huggingface.co/Qwen/Qwen2.5-7B-Instruct-GGUF/resolve/main/qwen2.5-7b-instruct-q4_k_m.gguf"
elif [ "$AVAIL_MB" -ge 3200 ]; then
    MODEL_NAME="qwen2.5-3b-instruct-q4_k_m.gguf"
    MODEL_URL="https://huggingface.co/Qwen/Qwen2.5-3B-Instruct-GGUF/resolve/main/qwen2.5-3b-instruct-q4_k_m.gguf"
else
    MODEL_NAME="qwen2.5-1.5b-instruct-q4_k_m.gguf"
    MODEL_URL="https://huggingface.co/Qwen/Qwen2.5-1.5B-Instruct-GGUF/resolve/main/qwen2.5-1.5b-instruct-q4_k_m.gguf"
fi

echo "[+] Perfil seleccionado: $MODEL_NAME"

echo "=== [2/4] INSTALANDO DEPENDENCIAS Y COMPILANDO llama.cpp (ARM64) ==="
pkg update -y && pkg install -y git cmake clang make curl python

if [ ! -d "$LLM_DIR/llama.cpp" ]; then
    git clone --depth 1 https://github.com/ggml-org/llama.cpp.git "$LLM_DIR/llama.cpp"
fi

cd "$LLM_DIR/llama.cpp"
cmake -B build -DGGML_NATIVE=ON -DLLAMA_CURL=OFF
cmake --build build --config Release -j$(nproc)

echo "=== [3/4] DESCARGANDO MODELO CUANTIZADO GGUF ==="
MODEL_PATH="$MODELS_DIR/$MODEL_NAME"
if [ ! -f "$MODEL_PATH" ]; then
    curl -L --progress-bar "$MODEL_URL" -o "$MODEL_PATH"
fi

echo "=== [4/4] CREANDO ORQUESTADOR OFFLINE CONECTADO A m82_database.db ==="
cat << PY_AGENT > "$M82_DIR/m82_offline_analyst.py"
#!/usr/bin/env python3
"""
M82 SOVEREIGN OFFLINE ANALYST (ZERO-INTERNET / ZERO-GOOGLE)
Consulta SQLite WAL (m82_database.db) + Inferencia Local llama.cpp
"""
import os
import sys
import sqlite3
import subprocess
from pathlib import Path

M82_DIR = Path.home() / "M82"
DB_PATH = M82_DIR / "m82_database.db"
LLAMA_BIN = M82_DIR / "sovereign_llm" / "llama.cpp" / "build" / "bin" / "llama-cli"
MODEL_PATH = Path("$MODEL_PATH")

def fetch_m82_context(limit_dossier=8):
    con = sqlite3.connect(str(DB_PATH), timeout=60.0)
    con.execute("PRAGMA journal_mode=WAL;")
    con.execute("PRAGMA busy_timeout=60000;")
    cur = con.cursor()

    dossier = cur.execute("""
        SELECT desk_cluster, risk_score, alpha_score, headline
        FROM macro_dossier
        ORDER BY rowid DESC LIMIT ?
    """, (limit_dossier,)).fetchall()

    quotes = []
    try:
        quotes = cur.execute("""
            SELECT symbol, price, change_pct, updated_at
            FROM m82_live_market_quotes
            ORDER BY updated_at DESC LIMIT 12
        """).fetchall()
    except Exception:
        pass

    con.close()

    ctx_lines = [
        "GOBERNANZA ACTIVA: BUNKER MODE / CUSTODIA PASIVA 0.30x LOCK | Exposicion: 0.22x | VaR Diario: 1.68% | Warsh Spread: +102.0 bps.",
        "--- ULTIMOS VECTORES EN macro_dossier ---"
    ]
    for desk, risk, alpha, hl in dossier:
        ctx_lines.append(f"[{desk} | Risk={risk} | Alpha={alpha}] {hl}")

    if quotes:
        ctx_lines.append("--- COTIZACIONES LSEG EN VIVO ---")
        for sym, px, chg, ts in quotes:
            ctx_lines.append(f"{sym}: {px} ({chg:+.2f}%) [{ts}]")

    return "\n".join(ctx_lines)

def ask_offline(question: str):
    context = fetch_m82_context()
    prompt = (
        "<|im_start|>system\n"
        "Eres el Analista Cuantitativo Institucional del Nodo Charallave L4/L5 Edge para el Chairman Juan M. Molina. "
        "Responde en espanol tecnico y ejecutivo basandote EXCLUSIVAMENTE en los datos reales extraidos de m82_database.db. "
        "Manten siempre la disciplina de BUNKER MODE / CUSTODIA PASIVA 0.30x LOCK.\n\n"
        f"CONTEXTO ACTUAL DE BASE DE DATOS M82:\n{context}<|im_end|>\n"
        f"<|im_start|>user\n{question}<|im_end|>\n"
        "<|im_start|>assistant\n"
    )

    cmd = [
        str(LLAMA_BIN),
        "-m", str(MODEL_PATH),
        "-p", prompt,
        "-n", "450",
        "-c", "4096",
        "-t", str(max(2, (os.cpu_count() or 4) - 2)),
        "--temp", "0.15",
        "--no-display-prompt"
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    output = res.stdout.replace("<|im_end|>", "").strip()
    print("\n" + "═"*68)
    print("🏛️  M82 SOVEREIGN OFFLINE ANALYST (100% LOCAL / AIR-GAPPED)")
    print("═"*68)
    print(output)
    print("═"*68 + "\n")

if __name__ == "__main__":
    query = " ".join(sys.argv[1:]).strip() or "Resume los ultimos vectores de riesgo en macro_dossier y nuestra postura bajo Bunker Mode 0.30x."
    ask_offline(query)
PY_AGENT

chmod +x "$M82_DIR/m82_offline_analyst.py"
ln -sf "$M82_DIR/m82_offline_analyst.py" "$PREFIX/bin/m82-ask"
echo "✅ INSTALACION COMPLETA. Ejecute en cualquier momento (incluso en modo avion):"
echo "   m82-ask \"¿Cual es el impacto actual de Nvidia, Anthropic y las tasas de Warsh en nuestra cartera?\""
