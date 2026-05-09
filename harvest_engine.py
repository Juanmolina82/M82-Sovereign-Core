import pandas as pd

# Datos de la Operación
ticker = "INTC"
target_original = 80.73
precio_actual = 124.92
volumen_posicion = 1000 # Ajuste con sus acciones reales

print("\n" + "="*45)
print("   M82 HOLDINGS: PROTOCOLO DE COSECHA (HARVEST)")
print("="*45)

profit_per_share = precio_actual - target_original
total_profit = profit_per_share * volumen_posicion
rendimiento_extra = ((precio_actual / target_original) - 1) * 100

print(f"ACTIVO: {ticker}")
print(f"PRECIO ACTUAL: ${precio_actual}")
print(f"RENDIMIENTO SOBRE TARGET: {rendimiento_extra:.2f}%")
print(f"GANANCIA A ASEGURAR: ${total_profit:,.2f}")

print("\n[ESTRATEGIA DE SALIDA RECOMENDADA]")
print(f"1. Vender 60% (Cosecha): ${(total_profit * 0.6):,.2f}")
print(f"2. Stop-Loss Dinámico (Trailing): $115.50")
print(f"3. Destino de Capital: Mastercard ($MA) / Liquidez")

print("\n" + "="*45)
print("ESTADO: ESTRATEGIA DE RESPALDO LISTA")
print("="*45 + "\n")
