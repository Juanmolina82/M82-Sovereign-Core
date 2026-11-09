# M82 V63.0.01-A :: AI ROUTING - FABLE 5.2 (Builder) + MYTHOS 5.2 (Auditor)
# Regla: Fable construye, Mythos audita, check.py decide, Chairman manda.

AI_CONFIG = {
    "core": "app/data.json - UNICO CORE - No tocar directo",
    "fable_5_2": {
        "role": "BUILDER",
        "tasks": ["orch.py", "patch_*.py", "PWA 8000", "OBS overlay", "Tarjetas HD 1000x1250", "check.py maintenance"],
        "rule": "Nunca cambia postura de riesgo. Nunca inventa precios LSEG.",
        "output": "Codigo + parche atomico listo para check.py"
    },
    "mythos_5_2": {
        "role": "AUDITOR - ACCESO LIMITADO",
        "tasks": ["Auditar ingesta LSEG", "Validar tesis Brent/WTI/Merey", "Detectar contradiccion CPI", "Veredicto SELLAR / NO SELLAR / ESPERAR"],
        "rule": "Si hay duda, veredicto = ESPERAR. Nunca ejecuta.",
        "output": "Auditoria + veredicto + riesgo"
    },
    "governance": {
        "risk": "BUNKER MODE / 0.30x LOCK - 100% Dry Powder",
        "decider": "Chairman Juan M. Molina - jmmp@molina82.com",
        "verifier": "check.py [OK] obligatorio antes de git push",
        "channels": ["Telegram -1004335849125", "Ntfy M82-Molina-Alerts-v2"]
    }
}

if __name__ == "__main__":
    print("[M82 AI ROUTING OK] Fable=Builder / Mythos=Auditor / Chairman=Decider")
    print(f"Postura: {AI_CONFIG['governance']['risk']}")
