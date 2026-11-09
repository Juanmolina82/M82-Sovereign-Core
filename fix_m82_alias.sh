#!/usr/bin/env bash
unalias m82 2>/dev/null || true
echo "alias m82='python3 ~/M82/m82_dossier.py'" >> ~/.bashrc
echo "alias m82='python3 ~/M82/m82_dossier.py'" >> ~/.zshrc 2>/dev/null || true
source ~/.bashrc 2>/dev/null || true
chmod +x ~/M82/m82_dossier.py
echo "[M82 ALIAS OK] Alias 'm82' re-vinculado directamente a python3 ~/M82/m82_dossier.py."
