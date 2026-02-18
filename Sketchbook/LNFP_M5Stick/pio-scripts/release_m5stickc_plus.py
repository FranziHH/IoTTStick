import os
import re
import shutil
import json
from SCons.Script import Import

Import("env")

destPath = "M5Update"
hwKey = "plus"

# Das PROJECT_DIR ist C:\GitHub\IoTTStick\Sketchbook\LNFP_M5Stick
project_dir = env.get("PROJECT_DIR")
project_dir = env.subst("$PROJECT_DIR")
build_dir = env.subst("$BUILD_DIR")

# Wir bauen den Pfad explizit zusammen
ino_path = os.path.join(project_dir, "LNFP_M5Stick.ino")

def get_version_from_ino(file_path):
    # Regex sucht nach: String BBVersion = "X.X.X";
    # Erklärt: Suche 'String BBVersion', dann optional Leerzeichen, 
    # ein '=', dann Anführungszeichen, fange den Inhalt ein, Ende Anführungszeichen.
    version_pattern = r'String\s+BBVersion\s*=\s*"([^"]+)"'
    
    if not os.path.exists(file_path):
        return "Unknown"

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        match = re.search(version_pattern, content)
        if match:
            return match.group(1) # Gibt z.B. 1.6.7 zurück
    return "Unknown"

def release_action(env, target, source):
    # 1. Projekt-Verzeichnis holen (C:\GitHub\IoTTStick\Sketchbook\LNFP_M5Stick)
    project_dir = env.subst("$PROJECT_DIR")
    
    # 2. Den echten Root-Pfad berechnen (Zwei Ebenen hoch zu C:\GitHub\IoTTStick)
    # Das erste ".." führt zu \Sketchbook, das zweite zu \IoTTStick
    root_dir = os.path.abspath(os.path.join(project_dir, "..", ".."))
    
    # 3. Version aus der .ino holen
    version = get_version_from_ino(ino_path) 

    # 4. Den Zielpfad im Root zusammenbauen
    output_dir = os.path.join(root_dir, "docs", "bin", f"V{version}", destPath)

    build_flags = env.get("BUILD_FLAGS", [])
    
    for flag in build_flags:
        if "RELEASE_NAME" in flag:
            match = re.search(r'\\"(.*?)\\"', flag)
            if match:
                release_name = match.group(1)
            break

    # 5. Verzeichnis erstellen, falls es fehlt
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"VERZEICHNIS IM ROOT ERSTELLT: {output_dir}")
    else:
        print(f"ROOT-VERZEICHNIS BEREITS VORHANDEN: {output_dir}")

    # 3. Quelldateien definieren
    boot_app0_src = os.path.join(project_dir, "bin", "boot_app0.bin")
    bootloader_src = os.path.join(project_dir, "bin", "m5stick_plus.bootloader.bin")
    partitions_src = os.path.join(build_dir, "partitions.bin")
    firmware_src = os.path.join(build_dir, "firmware.bin")
    filesystem_src = os.path.join(build_dir, "spiffs.bin") # Falls LittleFS, ggf. littlefs.bin prüfen
    full_bin_dir = os.path.join(project_dir, "build_output", "merge")
    full_bin_src = os.path.join(full_bin_dir, f"{version}_{release_name}_full.bin")

    # 4. Kopier-Vorgänge mit deinen Zielnamen
    # shutil.copy2 behält Metadaten wie Zeitstempel bei
    
    files_to_copy = [
        (boot_app0_src, "boot_app0.bin"),
        (firmware_src, "LNFP_M5Stick.ino.bin"),
        (bootloader_src, "LNFP_M5Stick.ino.bootloader.bin"),
        (partitions_src, "LNFP_M5Stick.ino.partitions.bin"),
        (filesystem_src, "LNFP_M5Stick.spiffs.bin"),
        (full_bin_src, "LNFP_M5Stick_Full.bin")
    ]

    for src, dest_name in files_to_copy:
        if os.path.exists(src):
            dest_path = os.path.join(output_dir, dest_name)
            shutil.copy2(src, dest_path)
            print(f"KOPIERT: {dest_name}")
        else:
            print(f"WARNUNG: Quelldatei nicht gefunden: {src}")

    json_path = os.path.join(root_dir, "docs", "versions.json")
    if os.path.exists(json_path):
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        updated = False
        # Definition der IDs für den Check
        full_id = f"V{version}/{destPath}/LNFP_M5Stick_Full.bin"
        app_id = f"V{version}/{destPath}/LNFP_M5Stick.ino.bin"

        # Check für FULL
        if os.path.exists(os.path.join(output_dir, "LNFP_M5Stick_Full.bin")):
            if not any(item['id'] == full_id for item in data[hwKey]["full"]):
                data[hwKey]["full"].insert(0, {"id": full_id, "name": f"v{version}", "offset": "0x0"})
                updated = True

        # Check für UPDATE (App)
        if os.path.exists(os.path.join(output_dir, "LNFP_M5Stick.ino.bin")):
            if not any(item['id'] == app_id for item in data[hwKey]["update"]):
                data[hwKey]["update"].insert(0, {"id": app_id, "name": f"v{version}", "offset": "0x10000"})
                updated = True

        if updated:
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
            print("JSON erfolgreich aktualisiert.")

# Registrierung des Scripts nach dem Build
env.AddPostAction("$BUILD_DIR/${PROGNAME}.bin", release_action)
