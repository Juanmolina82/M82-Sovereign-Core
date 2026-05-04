from instagrapi import Client
import getpass

cl = Client()
user = input("M82 Instagram User: ")
password = getpass.getpass("M82 Instagram Password (no se verá al escribir): ")

print("\n--- Iniciando Handshake con Instagram ---")
try:
    cl.login(user, password)
    cl.dump_settings("session.json")
    print("--- ÉXITO: Sesión encriptada en session.json ---")
except Exception as e:
    print(f"--- ERROR: {e} ---")
