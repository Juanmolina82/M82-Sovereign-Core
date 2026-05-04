def calculate_stress(ebitda, debt, rate_increase_bps):
    print("🏛️ ANALIZADOR DE STRESS TEST M82 - MOLINA HOLDINGS")
    print("--------------------------------------------------")
    
    # Impacto en el servicio de la deuda
    additional_interest = debt * (rate_increase_bps / 10000)
    new_ebitda = ebitda * 0.88  # Factor de reducción por inflación energética
    free_cash_flow = new_ebitda - additional_interest
    
    print(f"📍 Reducción de EBITDA Est. (Energía): -12%")
    print(f"📍 Costo Adicional de Deuda: +${additional_interest:,.2f}")
    print(f"📍 Flujo de Caja Libre (Post-Stress): ${free_cash_flow:,.2f}")
    
    if free_cash_flow < (ebitda * 0.5):
        print("\n🚨 ALERTA ROJA: Riesgo de Liquidez. Activar SHIELD ASSETS.")
    else:
        print("\n✅ ESTADO: Resiliente. El búnker aguanta el impacto.")

# Ejemplo basado en estructura estándar (Ajustar valores según vault.json)
calculate_stress(ebitda=5000000, debt=15000000, rate_increase_bps=50)
