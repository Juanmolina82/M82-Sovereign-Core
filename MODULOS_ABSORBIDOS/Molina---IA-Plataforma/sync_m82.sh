#!/bin/bash
echo "--- M82 CLOUD SYNC ---"
git add .
git commit -m "M82-SYNC: Núcleo actualizado con licencia y alertas LSEG"
git push origin main
echo "--- SINCRONIZACIÓN COMPLETADA ---"
