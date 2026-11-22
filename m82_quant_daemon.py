import os, time, subprocess
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["OPENBLAS_NUM_THREADS"] = "1"

M82_DIR = os.path.expanduser("~/M82")

while True:
    try:
        subprocess.run(["python3", os.path.join(M82_DIR, "m82_pythagoras_thorp_orchestrator.py")], check=False)
        subprocess.run(["python3", os.path.join(M82_DIR, "thorp_dynamic_frontier_l7.py")], check=False)
        subprocess.run(["python3", os.path.join(M82_DIR, "thorp_execution_friction_l9.py")], check=False)
        subprocess.run(["python3", os.path.join(M82_DIR, "thorp_bayesian_regime_l10.py")], check=False)
        subprocess.run(["python3", os.path.join(M82_DIR, "m82_sunday_open_sentinel.py")], check=False)
        subprocess.run(["python3", os.path.join(M82_DIR, "m82_quant_hud_renderer.py")], check=False)
        subprocess.run(["bash", os.path.join(M82_DIR, "m82_github_vault_backup.sh")], check=False)
    except Exception as e:
        print(f"[QUANT DAEMON ERR] {e}")
    time.sleep(900)
