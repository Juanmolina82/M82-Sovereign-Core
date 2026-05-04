import os

def check():
    print("\n" + "="*30)
    print(" AUDITORIA DE SISTEMAS MOLINA")
    print("="*30)
    
    # 1. Verificar archivos críticos
    archivos = ['ia_engine.py', 'molina_terminal.py']
    for f in archivos:
        if os.path.exists(f):
            print(f"[OK] Archivo encontrado: {f}")
        else:
            print(f"[!] FALTA: {f}")

    # 2. Verificar el Motor e Informe Banco Mundial
    try:
        from ia_engine import fetch_world_bank_data, Asset
        print("[OK] Motor ia_engine cargado.")
        
        val, date = fetch_world_bank_data()
        if val is None:
            print("[!] STATUS: VENEZUELA ES ISLA ESTADISTICA (Confirmado)")
        else:
            print(f"[OK] DATA BM: Conectado. PIB: {val}%")
            
    except Exception as e:
        print(f"[ERR] Error en motor: {e}")

if __name__ == "__main__":
    check()
