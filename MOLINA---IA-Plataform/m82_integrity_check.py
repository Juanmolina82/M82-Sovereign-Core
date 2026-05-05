import os
import json

def run_audit():
    print("\n🔍 --- M82 DATA INTEGRITY REPORT ---")
    files = [f for f in os.listdir('.') if f.endswith('.json')]
    
    if not files:
        print("⚠️ Alerta: No se encontraron archivos de datos .json.")
        return

    for file in files:
        try:
            with open(file, 'r', encoding='utf-8') as f:
                json.load(f)
                size = os.path.getsize(file)
                print(f"✅ {file.ljust(25)} | STATUS: OK | SIZE: {size} bytes")
        except Exception as e:
            print(f"❌ {file.ljust(25)} | STATUS: CORRUPT | ERROR: {str(e)}")
    print("------------------------------------\n")

if __name__ == "__main__":
    run_audit()
