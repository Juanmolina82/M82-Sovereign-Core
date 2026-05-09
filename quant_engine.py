import pandas as pd

print("\n--- M82 SOVEREIGN CORE: QUANT ENGINE v6.0 ---")
try:
    df = pd.read_csv('intel_data.csv')
    print("\n[DATOS DE INTEL CARGADOS]")
    print(df.tail(1))
    target = 80.73
    current = df['Close'].iloc[-1]
    diff = target - current
    print(f"\nPROYECCIÓN: $80.73")
    print(f"ESTADO: {'ALCANZADO' if diff <= 0 else 'EN PROGRESO'}")
    print("-" * 45)
except Exception as e:
    print(f"Error en motor: {e}")
