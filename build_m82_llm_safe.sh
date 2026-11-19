#!/data/data/com.termux/files/usr/bin/bash
set -e

M82_DIR="$HOME/M82"
LLM_DIR="$M82_DIR/sovereign_llm"
MODELS_DIR="$LLM_DIR/models"
mkdir -p "$MODELS_DIR"

echo "=== [1/3] OBTENIENDO MOTOR llama-cli (PRECOMPILADO O BUILD -j2) ==="
if pkg install -y llama-cpp 2>/dev/null && command -v llama-cli >/dev/null 2>&1; then
    LLAMA_BIN="$(command -v llama-cli)"
    echo "[+] Binario precompilado instalado en: $LLAMA_BIN"
else
    cd "$LLM_DIR/llama.cpp"
    rm -rf build
    cmake -B build \
      -DGGML_NATIVE=ON \
      -DLLAMA_CURL=OFF \
      -DLLAMA_BUILD_TOOLS=ON \
      -DLLAMA_BUILD_TESTS=OFF \
      -DLLAMA_BUILD_EXAMPLES=OFF \
      -DLLAMA_BUILD_SERVER=OFF \
      -DCMAKE_UNITY_BUILD=OFF
    cmake --build build --config Release --target llama-cli -j2
    LLAMA_BIN="$LLM_DIR/llama.cpp/build/bin/llama-cli"
    echo "[+] Compilacion quirurgica completada: $LLAMA_BIN"
fi

echo "=== [2/3] AUDITANDO RAM Y DESCARGANDO MODELO GGUF ==="
free -h
AVAIL_MB=$(free -m | awk '/^Mem:/ {print $7}')
[ -z "$AVAIL_MB" ] && AVAIL_MB=$(free -m | awk '/^Mem:/ {print $4}')
echo "[+] RAM Disponible actual: ${AVAIL_MB} MB"

if [ "$AVAIL_MB" -ge 5500 ]; then
    MODEL_NAME="qwen2.5-3b-instruct-q4_k_m.gguf"
    MODEL_URL="https://huggingface.co/Qwen/Qwen2.5-3B-Instruct-GGUF/resolve/main/qwen2.5-3b-instruct-q4_k_m.gguf"
else
    MODEL_NAME="qwen2.5-1.5b-instruct-q4_k_m.gguf"
    MODEL_URL="https://huggingface.co/Qwen/Qwen2.5-1.5B-Instruct-GGUF/resolve/main/qwen2.5-1.5b-instruct-q4_k_m.gguf"
fi

MODEL_PATH="$MODELS_DIR/$MODEL_NAME"
if [ ! -f "$MODEL_PATH" ]; then
    echo "[+] Descargando $MODEL_NAME..."
    curl -L --progress-bar "$MODEL_URL" -o "$MODEL_PATH"
fi

echo "=== [3/3] VINCULANDO m82-ask CON m82_database.db (WAL MODE) ==="
cat << PY_AGENT > "$M82_DIR/m82_offline_analyst.py"
#!/usr/bin/env python3
import os, sys, sqlite3, subprocess
from pathlib import Path

DB_PATH = Path.home() / "M82" / "m82_database.db"
LLAMA_BIN = "$LLAMA_BIN"
MODEL_PATH = "$MODEL_PATH"

def fetch_m82_context(limit_dossier=8):
    con = sqlite3.connect(str(DB_PATH), timeout=60.0)
    con.execute("PRAGMA journal_mode=WAL;")
    con.execute("PRAGMA busy_timeout=60000;")
    cur = con.cursor()
    dossier = cur.execute("SELECT desk_cluster, risk_score, alpha_score, headline FROM macro_dossier ORDER BY rowid DESC LIMIT ?", (limit_dossier,)).fetchall()
    con.close()
    lines = ["GOBERNANZA: BUNKER MODE / CUSTODIA PASIVA 0.30x LOCK | Exposicion: 0.22x | VaR: 1.68% | Warsh Spread: +102.0 bps."]
    for desk, risk, alpha, hl in dossier:
        lines.append(f"[{desk} | Risk={risk} | Alpha={alpha}] {hl}")
    return "\n".join(lines)

def ask_offline(question: str):
    ctx = fetch_m82_context()
    prompt = (
        "<|im_start|>system\n"
        "Eres el Analista Cuantitativo Institucional del Nodo Charallave L4/L5 Edge para el Chairman Juan M. Molina. "
        "Responde en espanol tecnico basandote solo en m82_database.db y respetando BUNKER MODE 0.30x LOCK.\n\n"
        f"{ctx}<|im_end|>\n<|im_start|>user\n{question}<|im_end|>\n<|im_start|>assistant\n"
    )
    res = subprocess.run([
        LLAMA_BIN, "-m", MODEL_PATH, "-p", prompt,
        "-n", "400", "-c", "4096", "-t", str(max(2, (os.cpu_count() or 4) - 2)),
        "--temp", "0.15", "--no-display-prompt"
    ], capture_output=True, text=True)
    out = res.stdout.replace("<|im_end|>", "").strip()
    print("\n" + "═"*64 + "\n🏛️  M82 SOVEREIGN OFFLINE ANALYST (100% AIR-GAPPED)\n" + "═"*64)
    print(out)
    print("═"*64 + "\n")

if __name__ == "__main__":
    q = " ".join(sys.argv[1:]).strip() or "Resume los ultimos vectores de macro_dossier y nuestra postura bajo Bunker Mode 0.30x."
    ask_offline(q)
PY_AGENT

chmod +x "$M82_DIR/m82_offline_analyst.py"
ln -sf "$M82_DIR/m82_offline_analyst.py" "$PREFIX/bin/m82-ask"
echo "✅ LISTO. Ejecutando prueba offline sobre m82_database.db..."
m82-ask "Analiza los ultimos eventos de macro_dossier y confirma nuestra postura bajo Bunker Mode 0.30x."
