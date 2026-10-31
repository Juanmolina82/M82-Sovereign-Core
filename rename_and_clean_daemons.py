import os, subprocess

# Mapping de renombramiento de archivos
rename_map = {
    'm82_lseg_news_wsj_daemon.py': 'm82_wire_news_daemon.py',
    'm82_kpler_flow_predictor.py': 'm82_cargo_flow_predictor.py'
}

# 1. Detener procesos antiguos
print("🛑 Deteniendo daemons no soberanos...")
subprocess.run("pkill -f m82_lseg", shell=True)
subprocess.run("pkill -f m82_kpler", shell=True)

# 2. Renombrar archivos en el sistema de archivos
for old_name, new_name in rename_map.items():
    if os.path.exists(old_name):
        os.rename(old_name, new_name)
        print(f"✅ Renombrado: {old_name} -> {new_name}")

# 3. Sanitizar referencias internas en todos los scripts .py
replacements = {
    'M82_WIRE': 'M82_WIRE',
    'M82_WIRE': 'M82_WIRE',
    'M82_WIRE': 'M82_WIRE',
    'M82_MACRO': 'M82_MACRO'
}

for root, _, files in os.walk('.'):
    for file in files:
        if file.endswith('.py'):
            filepath = os.path.join(root, file)
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            modified = content
            for old_str, new_str in replacements.items():
                modified = modified.replace(old_str, new_str)
            
            if modified != content:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(modified)
                print(f"🧹 Sanitizado código interno en: {filepath}")

# 4. Iniciar los nuevos daemons soberanos en segundo plano
if os.path.exists('m82_wire_news_daemon.py'):
    subprocess.run("nohup python3 m82_wire_news_daemon.py > ~/M82/logs/wire_news.log 2>&1 &", shell=True)
if os.path.exists('m82_cargo_flow_predictor.py'):
    subprocess.run("nohup python3 m82_cargo_flow_predictor.py > ~/M82/logs/cargo_flow.log 2>&1 &", shell=True)

print("🚀 Todos los daemons han sido reiniciados con identidad M82 Soberana.")
