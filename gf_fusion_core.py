import pandas as pd

def run_fusion():
    # Base de datos integrada de los reportes GuruFocus (Mayo 2026)
    fusion_data = {
        'Ticker': ['AAPL', 'INTC', 'AMD'],
        'GF_Score': [97, 71, 64],
        'Price': [293.32, 124.92, 455.19],
        'GF_Value': [260.07, 28.02, 114.50],
        'Overvaluation': ['12.8%', '345.8%', '297.5%'],
        'Insider_Signal': ['Venta Masiva ($95M)', 'Venta ($4M)', 'Venta Institucional']
    }
    
    df = pd.DataFrame(fusion_data)
    
    print("\n" + "="*60)
    print("   M82 HOLDINGS - GURUFOCUS CORE FUSION V1.0")
    print("="*60)
    print(df.to_string(index=False))
    print("-"*60)
    
    # Lógica de Decisión Sovereign
    print("ESTADO DEL MERCADO: EUFORIA TÉCNICA")
    for i, row in df.iterrows():
        if float(row['Overvaluation'].replace('%', '')) > 50:
            print(f"⚠️ ALERTA [{row['Ticker']}]: Burbuja detectada. No comprar.")
        else:
            print(f"✅ ESTABLE [{row['Ticker']}]: Mantener con cautela.")
    
    print("="*60 + "\n")

if __name__ == "__main__":
    run_fusion()
