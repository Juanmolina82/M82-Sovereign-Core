#!/usr/bin/env bash
cd ~/M82_Backups && ls -t M82_Master_Dossier_*.tar.gz 2>/dev/null | tail -n +3 | xargs rm -f
