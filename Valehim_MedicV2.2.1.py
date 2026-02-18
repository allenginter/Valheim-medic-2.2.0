import os
import json
import threading
from PIL import Image

# Configuration setup
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE = os.path.join(SCRIPT_DIR, "valheim_medic_config.json")

class ValheimMedicConsole:
    def __init__(self):
        self.path = ""
        self.bad_shaders = [
            b"Standard", 
            b"Hidden/InternalErrorShader", 
            b"Standard (Specular setup)",
            b"Particles/Standard Unlit2",
            b"Custom/Creature",
            b"StandardUnlit2"
        ]

    def load_config(self):
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, "r") as f:
                    config = json.load(f)
                    path = config.get("last_path", "")
                    if os.path.exists(path):
                        self.path = path
            except:
                pass

    def save_config(self, path):
        config = {"last_path": path}
        try:
            with open(CONFIG_FILE, "w") as f:
                json.dump(config, f)
        except:
            pass

    def is_power_of_two(self, n):
        return (n & (n - 1) == 0) and n != 0

    def scan(self, scan_path):
        print(f"\n--- Starting Aggressive Scan: {scan_path} ---")
        files_to_check = []
        for root, _, files in os.walk(scan_path):
            for f in files:
                files_to_check.append(os.path.join(root, f))

        total_files = len(files_to_check)
        
        for i, file_path in enumerate(files_to_check):
            ext = os.path.splitext(file_path)[1].lower()
            rel_path = os.path.relpath(file_path, scan_path)
            mod_folder = rel_path.split(os.sep)[0]

            # 1. Texture Check
            if ext in [".png", ".jpg", ".dds", ".tga"]:
                try:
                    with Image.open(file_path) as img:
                        w, h = img.size
                        if not (self.is_power_of_two(w) and self.is_power_of_two(h)):
                            print(f"[WARN] [{mod_folder}] {rel_path} is {w}x{h}")
                except:
                    pass

            # 2. Aggressive Shader Search
            try:
                if os.path.getsize(file_path) < 200000000:
                    with open(file_path, "rb") as f:
                        content = f.read()
                        for shader in self.bad_shaders:
                            if shader in content:
                                print(f"[ALERT] [{mod_folder}] Incompatible Shader: '{shader.decode()}' in {rel_path}")
                                break
            except:
                pass

            # 3. Missing Manifests
            if ext in [".unity3d", ".bundle"]:
                if not os.path.exists(file_path + ".manifest"):
                    print(f"[INFO] [{mod_folder}] No .manifest for {rel_path}")

        print("\n--- Scan Complete ---")

    def run(self):
        self.load_config()
        print("Valheim Mod Medic v2.3 (Console Edition)")
        
        if self.path:
            print(f"Default folder: {self.path}")
            use_last = input("Use default folder? (y/n): ").lower()
            if use_last != 'y':
                self.path = input("Enter full path to Valheim plugins folder: ").strip('"')
        else:
            self.path = input("Enter full path to Valheim plugins folder: ").strip('"')

        if os.path.exists(self.path):
            self.save_config(self.path)
            self.scan(self.path)
        else:
            print("Invalid path. Exiting.")

if __name__ == "__main__":
    medic = ValheimMedicConsole()
    medic.run()
    input("\nPress Enter to close...")