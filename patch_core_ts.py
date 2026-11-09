import os

path = os.path.expanduser("~/M82/m82_caracas_master_core.py")
if os.path.exists(path):
    with open(path, "r") as f:
        content = f.read()
    
    # Asegurar que se inserte created_at explícitamente con CURRENT_TIMESTAMP
    old_stmt = "INSERT INTO m82_multi_stream (daemon_source, headline, headline_hash, desk, status, alpha_score, asset_impact)"
    new_stmt = "INSERT INTO m82_multi_stream (daemon_source, headline, headline_hash, desk, status, alpha_score, asset_impact, created_at)"
    
    old_vals = "VALUES (?, ?, ?, ?, 'VERIFIED', ?, ?)"
    new_vals = "VALUES (?, ?, ?, ?, 'VERIFIED', ?, ?, CURRENT_TIMESTAMP)"
    
    if old_stmt in content:
        content = content.replace(old_stmt, new_stmt).replace(old_vals, new_vals)
        with open(path, "w") as f:
            f.write(content)
        print("✅ Parche de timestamp automático aplicado a m82_caracas_master_core.py.")
