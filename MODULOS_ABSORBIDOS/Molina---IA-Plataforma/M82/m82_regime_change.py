import time

def analyze_warsh_era():
    print("\033[95m[M82 MACRO DOSSIER] - ANALIZADOR DE RÉGIMEN POST-POWELL\033[0m")
    print("ESTATUS: Transición confirmada para el 15 de Mayo.")
    print("-" * 60)
    
    metrics = {
        "Balance Sheet": "AGRESSIVE SHRINKING (QT+)",
        "Market Role": "REDUCED INTERVENTION",
        "Transparency": "OPAQUE (Fewer speeches/pressers)",
        "Yield Curve": "STEEPENING BIAS"
    }
    
    for key, value in metrics.items():
        print(f"{key.ljust(20)}: \033[93m{value}\033[0m")
    
    print("-" * 60)
    print("\033[92mESTRATEGIA RECOMENDADA: Sobreponderar Crédito Privado y Real Estate Industrial.\033[0m")

if __name__ == "__main__":
    analyze_warsh_era()
