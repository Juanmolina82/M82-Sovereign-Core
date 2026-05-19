import sys
import os

# Add the AI_ENGINE directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "AI_ENGINE"))

# Launch the M82 master server
import importlib.util

spec = importlib.util.spec_from_file_location(
    "m82_master",
    os.path.join(os.path.dirname(__file__), "AI_ENGINE", "m82_master.py")
)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
