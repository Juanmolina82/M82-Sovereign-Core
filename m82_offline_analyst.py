#!/usr/bin/env python3
"""
M82 SOVEREIGN OFFLINE ANALYST (100% AIR-GAPPED / ZERO-GOOGLE)
Lee m82_database.db (WAL) -> Streaming directo desde llama-completion (-t 4)
"""
import sys
import shutil
import sqlite3
import subprocess
from pathlib import Path

DB_PATH = Path.home() / "M82" / "m82_database.db"
LLAMA_BIN = shutil.which("llama-completion") or "/data/data/com.termux/files/usr/bin/llama-cli"
MODEL_PATH = str(Path.home() / "M82" / "sovereign_llm" / "models" / "qwen2.5-1.5b-instruct-q4_k_m.gguf")

def fetch_m82_context(limit_dossier=3):
    con = sqlite3.connect(str(DB_PATH), timeout=60.0)
    con.execute("PRAGMA journal_mode=WAL;")
    con.execute("PRAGMA busy_timeout=60000;")
    cur = con.cursor()
    dossier = cur.execute("""
        SELECT desk_cluster, risk_score, alpha_score, headline
        FROM macro_dossier
        ORDER BY rowid DESC LIMIT ?
    """, (limit_dossier,)).fetchall()
    con.close()

    lines = [
        "GOBERNANZA: BUNKER MODE / CUSTODIA PASIVA 0.30x LOCK | Exposicion: 0.22x | VaR: 1.68% | Warsh Spread: +102.0 bps."
    ]
    for desk, risk, alpha, hl in dossier:
        lines.append(f"[{desk} | R={risk} | A={alpha}] {hl[:140]}")
    return "\n".join(lines)

def ask_offline(question: str):
    ctx = fetch_m82_context()
    prompt = (
        "<|im_start|>system\n"
        "Eres el Analista Cuantitativo Institucional del Nodo Charallave L4/L5 Edge para el Chairman Juan M. Molina. "
        "Responde en espanol ejecutivo y breve (maximo 5 lineas) basandote solo en m82_database.db y respetando BUNKER MODE 0.30x LOCK.\n\n"
        f"{ctx}<|im_end|>\n"
        f"<|im_start|>user\n{question}<|im_end|>\n"
        "<|im_start|>assistant\n"
    )

    cmd = [
        LLAMA_BIN,
        "-m", MODEL_PATH,
        "-p", prompt,
        "-no-cnv",
        "--no-display-prompt",
        "--no-warmup",
        "-c", "768",
        "-n", "140",
        "-t", "4",
        "--temp", "0.15",
        "--log-disable", "--no-perf"
    ]

    print("\n" + "═"*64)
    print("🏛️  M82 SOVEREIGN OFFLINE ANALYST (100% AIR-GAPPED / WAL DB)")
    print("═"*64)
    sys.stdout.flush()
    subprocess.run(cmd, stdin=subprocess.DEVNULL)
    print("\n" + "═"*64 + "\n")

if __name__ == "__main__":
    q = " ".join(sys.argv[1:]).strip() or "Resume los ultimos vectores de macro_dossier y nuestra postura bajo Bunker Mode 0.30x."
    ask_offline(q)
