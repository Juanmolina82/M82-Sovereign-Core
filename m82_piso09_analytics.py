#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MOLINA HOLDINGS & GLOBAL LLC - M82 SYSTEMS
Módulo: m82_piso09_analytics.py
Versión: 5.7.4-WEIGHTS
Propósito: Extraer el PISO_09 del JSON Maestro M82 y calcular las métricas 
           de peso relativo e indexación táctica de BLK, BAC y BT.L.
"""

import json
import os

def analizar_piso_09():
    archivo_json = "m82_master_architecture.json"
    
    if not os.path.exists(archivo_json):
        print(f"[ERROR] No se encuentra el monolito base '{archivo_json}'. Ejecuta primero el core v5.7.3-BT.")
        return

    with open(archivo_json, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Extraer nodos asignados al Piso 09 en la Capa Financiera
    capa_financiera = data["PISO_3_OPERATIONAL_MATRIX_LSEG"]["CAPA_2_FINANCIERA_PLUMBING"]
    nodos_piso_09 = capa_financiera["nodos"].get("PISO_09_ASSET_MANAGEMENT", [])

    if not nodos_piso_09:
        print("[WARNING] No se detectaron nodos activos en el PISO_09_ASSET_MANAGEMENT.")
        return

    print("==================================================================")
    print(" M82 ANALYTICS: EVALUACIÓN DE PESOS RELATIVOS - PISO 09           ")
    print("==================================================================")
    
    total_yield = 0.0
    parsed_nodes = []
    
    # Asignación de score táctico según estatus interno del fondo
    status_weights = {
        "ANCHOR": 1.5,
        "STRATEGIC_WATCH": 1.2,
        "HOLD": 1.0,
        "BUY": 1.1,
        "STRONG_BUY": 1.4
    }

    for nodo in nodos_piso_09:
        ticker = nodo["ticker"]
        # Limpiar el string del yield (ej: "5.0%" -> 5.0)
        yield_val = float(nodo["dividend_yield"].replace("%", ""))
        status = nodo["fund_internal_status"]
        score = status_weights.get(status, 1.0)
        
        total_yield += yield_val
        parsed_nodes.append({
            "ticker": ticker,
            "yield": yield_val,
            "status": status,
            "score": score
        })

    print(f"[*] Matriz Detectada : {[n['ticker'] for n in parsed_nodes]}")
    print(f"[*] Rendimiento Agregado del Piso: {total_yield:.2f}%\n")
    print(f"{'TICKER':<10} | {'YIELD INDIV.':<12} | {'CONTRIB. YIELD':<16} | {'STATUS SCORE':<15}")
    print("-" * 65)

    for n in parsed_nodes:
        # Contribución relativa al flujo total de dividendos del piso
        contrib_yield = (n["yield"] / total_yield) * 100 if total_yield > 0 else 0
        print(f"{n['ticker']:<10} | {n['yield']:>10.2f}% | {contrib_yield:>14.2f}% | {n['score']:>12.1f}x")

    print("-" * 65)
    
    # Aislamiento específico del vector de rentabilidad regulada UK
    bt_data = next((x for x in parsed_nodes if x["ticker"] == "BT.L"), None)
    if bt_data:
        bt_contrib = (bt_data["yield"] / total_yield) * 100
        print(f"[⚡] ALERTA SOBERANA: BT.L domina el {bt_contrib:.1f}% del flujo de renta del Piso 09.")
        print(f"    Escrutinio regulatorio NSI Act y exposición Bharti monitoreados en CAPA_2.")
    
    print("==================================================================")

if __name__ == "__main__":
    analizar_piso_09()
