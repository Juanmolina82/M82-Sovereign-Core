import getpass
import hashlib

class M82Security:
    def __init__(self):
        # Hash de la llave maestra (Simulado para la demo)
        self.master_key_hash = "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8"

    def authenticate(self):
        print("\n" + "="*40)
        print("  M82 SECURE ACCESS - MOLINA HOLDINGS")
        print("="*40)
        pin = getpass.getpass("Introduzca PIN de Acceso Institucional: ")
        
        # Verificando contra el estándar de encriptación
        check_hash = hashlib.sha256(pin.encode()).hexdigest()
        
        if check_hash == self.master_key_hash:
            print("\n[ACCESO CONCEDIDO] Bienvenido, Chairman.")
            return True
        else:
            print("\n[ERROR] Credenciales Inválidas. Bloqueo preventivo activado.")
            return False

if __name__ == "__main__":
    gate = M82Security()
    if gate.authenticate():
        print("[SISTEMA] Inicializando M82 AI Core...")
        # Aquí se invocaría el Dashboard final
