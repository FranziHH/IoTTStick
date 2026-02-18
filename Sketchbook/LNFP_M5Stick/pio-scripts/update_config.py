import os
import json
import sys
import subprocess

Import("env")

def update_and_build(target, source, env):
    # Pfade definieren
    project_dir = env.get("PROJECT_DIR")
    data_dir = os.path.join(project_dir, "data")
    
    # Pfad zur node.cfg
    config_file = os.path.join(data_dir, "configdata", "node.cfg")
    
    # 1. JSON-Wert ändern (devName)
    if os.path.exists(config_file):
        with open(config_file, "r", encoding='utf-8') as f:
            data = json.load(f)
        
        new_name = env.GetProjectOption("custom_dev_name", "IoTTStickM5")
        data["devName"] = new_name
        
        with open(config_file, "w", encoding='utf-8') as f:
            json.dump(data, f, indent=4)
        print(f"--- JSON: devName auf '{new_name}' gesetzt ---")

# Trigger: Wird ausgeführt, wenn du "Build Filesystem Image" drückst
env.AddPreAction("$BUILD_DIR/spiffs.bin", update_and_build)
env.AddPreAction("$BUILD_DIR/littlefs.bin", update_and_build)