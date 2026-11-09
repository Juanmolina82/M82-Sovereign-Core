#!/usr/bin/env python3
# M82 DOSSIER MACRO ROBUSTO - V63.0.01-A
# Fable construye. Mythos audita. Caracas manda. Charallave ejecuta.

import os, sys, json, time

def limpiar():
    os.system('clear')

def titulo(texto):
    print("\n" + "=" * 60)
    print(f"  {texto}")
    print("=" * 60)

def pausa():
    input("\nPresione [ENTER] para continuar...")

def mostrar_tesis():
    limpiar()
    titulo("1. TESIS MADRE M82")
    print("Venezuela es el centro energético. USA tiene la caja.")
    print("Nosotros tenemos la auditoría.")
    print()
    print("No operamos titulares. Operamos estructura.")
    print("No operamos rumores. Operamos calendario + flujo + auditoría.")
    print()
    print("POSTURA SELLADA:")
    print("BUNKER MODE / 0.30x LOCK - 100% Dry Powder - 0 ejecuciones hasta CPI")
    print("Caracas manda. Charallave ejecuta.")
    pausa()

def mostrar_arquitectura():
    limpiar()
    titulo("2. ARQUITECTURA M82 - 3 CAPAS")
    print("CAPA 1: FABLE CONSTRUYE")
    print("- De un párrafo, diseña dispositivo completo, PCB 4 capas.")
    print("- Enclosure 3D, software, listo en <24h, funciona sin cambios.")
    print("- En M82: construye dossiers, scripts, códigos Termux, tablas.")
    print()
    print("CAPA 2: MYTHOS AUDITA")
    print("- De una imagen de molécula, sin internet, solo código.")
    print("- Traza arma completa en 30 min, verifica átomo por átomo.")
    print("- En M82: audita LSEG, busca contradicciones, da veredicto SELLAR/ESPERAR.")
    print()
    print("CAPA 3: CHAIRMAN DECIDE")
    print("- Juan M. Molina (jmmp@molina82.com).")
    print("- Solo tú apruebas, ejecutas o mantienes el búnker.")
    pausa()

def menu():
    while True:
        limpiar()
        titulo("M82 MACRO DOSSIER - SELECCIÓN DE MATRIZ")
        print(" 1. Ver Tesis Madre M82")
        print(" 2. Ver Arquitectura Dual (Fable / Mythos / Chairman)")
        print(" 3. Ver Estado del Búnker & Telemetría CORE")
        print(" 4. Salir")
        opcion = input("\nSeleccione opción [1-4]: ").strip()
        if opcion == '1':
            mostrar_tesis()
        elif opcion == '2':
            mostrar_arquitectura()
        elif opcion == '3':
            limpiar()
            titulo("3. TELEMETRÍA CORE & BUNKER")
            data_path = os.path.expanduser("~/M82/app/data.json")
            if os.path.exists(data_path):
                with open(data_path) as f:
                    print(json.dumps(json.load(f), indent=2))
            else:
                print("data.json no encontrado.")
            pausa()
        elif opcion == '4':
            print("\nCerrando Dossier M82. Caracas manda. Charallave ejecuta.")
            break

if __name__ == "__main__":
    menu()
