def check_energy_threshold(current_brent):
    # Parámetros de la Proyección de Ayer
    TARGET_BRENT = 125.0
    ebitda_base = 5000000
    
    print(f"🏛️ ANALISIS DE SENSIBILIDAD BRENT: ${current_brent}")
    print("-" * 40)
    
    if current_brent >= 110:
        # A partir de $110, aplicamos el factor de castigo Molina
        shock_factor = 0.12 # 12% de reducción operativa
        impacto = ebitda_base * shock_factor
        ebitda_proyectado = ebitda_base - impacto
        
        print(f"⚠️ ESTADO: UMBRAL CRITICO ALCANZADO")
        print(f"📉 IMPACTO EN CAJA: -${impacto:,.2f}")
        print(f"💰 EBITDA PROYECTADO: ${ebitda_proyectado:,.2f}")
    else:
        print("✅ ESTADO: MARGENES ESTABLES")

# Valor actual reportado en su terminal: $124.00
check_energy_threshold(124.00)
