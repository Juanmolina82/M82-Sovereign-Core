#!/bin/bash
# ==============================================================================
# M82 V60.6.0 PRIME :: DAILY 08:00 VET AUTOMATED DISPATCH ENGINE
# ==============================================================================

echo "🌅 [$(date)] Iniciando ciclo de compilación matutino 08:00 VET (BLK Level)..."

# 1. Inyectar telemetría y benchmarks
python3 ~/M82/m82_blk_earnings_q3_inject.py >> ~/M82/daily_dispatch.log 2>&1
python3 ~/M82/m82_refinitiv_esg_pdf_inject.py >> ~/M82/daily_dispatch.log 2>&1
python3 ~/M82/m82_citi_rerating_model.py >> ~/M82/daily_dispatch.log 2>&1

# 2. Generar interfaces e informes ejecutivos
python3 ~/M82/m82_caracas_dashboard_v6033_builder.py >> ~/M82/daily_dispatch.log 2>&1
python3 ~/M82/m82_lpl_pitch_builder.py >> ~/M82/daily_dispatch.log 2>&1
python3 ~/M82/m82_lpl_daily_reporter.py >> ~/M82/daily_dispatch.log 2>&1

echo "✨ [$(date)] Reporte diario LPL 08:00 VET listo en http://localhost:8080/lpl_daily_report_latest.html"
