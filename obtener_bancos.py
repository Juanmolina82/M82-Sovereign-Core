import pandas as pd
from datetime import datetime

print("Iniciando ciclo de captura macro-financiera M82 [Bunker Mode 0.30x]...")

# Matriz de monitoreo sectorial bancario (Q3 2026 Core/Systemic)
bancos_data = [
    {"RIC": "JPM", "Nombre": "JPMorgan Chase & Co", "Pais": "United States", "Estado": "Ingestado (Q3 Print)"},
    {"RIC": "WFC", "Nombre": "Wells Fargo & Co", "Pais": "United States", "Estado": "Ingestado (Q3 Print)"},
    {"RIC": "BAC", "Nombre": "Bank of America Corp", "Pais": "United States", "Estado": "Monitoreo Activo"},
    {"RIC": "C", "Nombre": "Citigroup Inc", "Pais": "United States", "Estado": "Monitoreo Activo"},
    {"RIC": "GS", "Nombre": "Goldman Sachs Group Inc", "Pais": "United States", "Estado": "Monitoreo Activo"},
    {"RIC": "MS", "Nombre": "Morgan Stanley", "Pais": "United States", "Estado": "Monitoreo Activo"},
    {"RIC": "SAN.MC", "Nombre": "Banco Santander SA", "Pais": "Spain", "Estado": "Monitoreo Activo"},
    {"RIC": "BBVA.MC", "Nombre": "BBVA SA", "Pais": "Spain", "Estado": "Monitoreo Activo"}
]

df = pd.DataFrame(bancos_data)
df['Timestamp_VET'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

print("\n--- Cobertura Bancaria Actualizada ---")
print(df[["RIC", "Nombre", "Pais", "Estado"]])

df.to_csv("bancos_refinitiv.csv", index=False)
print("\n[OK] Archivo 'bancos_refinitiv.csv' generado exitosamente en el nodo L4.")
