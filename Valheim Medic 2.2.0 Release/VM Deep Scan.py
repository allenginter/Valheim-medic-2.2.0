import os
import threading
import json
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image

# Config pathing
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE = os.path.join(SCRIPT_DIR, "valheim_medic_config.json")

class UnityScannerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Valheim Mod Medic v2.6 - Binary Signature Scan")
        self.root.geometry("650x750")
        self.stop_event = threading.Event()

        # UI Setup
        tk.Label(root, text="Valheim Plugins / Mod Folder:", font=("Arial", 10, "bold")).pack(pady=10)
        self.path_var = tk.StringVar()
        self.load_config()

        p_frame = tk.Frame(root)
        p_frame.pack(padx=20, fill="x")
        tk.Entry(p_frame, textvariable=self.path_var, width=55).pack(side="left", padx=5)
        tk.Button(p_frame, text="Browse", command=self.browse).pack(side="left")

        # Diagnostic Filters
        f_frame = tk.LabelFrame(root, text="Diagnostic Checks", padx=10, pady=10)
        f_frame.pack(pady=10, padx=20, fill="x")
        
        self.check_dim = tk.BooleanVar(value=True)
        tk.Checkbutton(f_frame, text="Check Texture Dimensions (Power of Two)", variable=self.check_dim).pack(anchor="w")
        
        self.check_manifest = tk.BooleanVar(value=True)
        tk.Checkbutton(f_frame, text="Identify Missing .manifest files", variable=self.check_manifest).pack(anchor="w")
        
        self.check_shaders = tk.BooleanVar(value=True)
        tk.Checkbutton(f_frame, text="Binary Signature Scan (URP/ShaderGraph)", variable=self.check_shaders).pack(anchor="w")

        # Log Window
        self.log = tk.Text(root, height=15, state="disabled", font=("Consolas", 9), bg="#1e1e1e", fg="#00ff00")
        self.log.pack(pady=10, padx=20, fill="both", expand=True)

        self.progress = ttk.Progressbar(root, length=550, mode='determinate')
        self.progress.pack(pady=5)

        # Action Buttons
        b_frame = tk.Frame(root)
        b_frame.pack(pady=10)
        self.btn_run = tk.Button(b_frame, text="Start Diagnosis", bg="#4CAF50", fg="white", width=15, height=2, command=self.start_scan)
        self.btn_run.pack(side="left", padx=5)
        self.btn_stop = tk.Button(b_frame, text="Stop", bg="#F44336", fg="white", width=15, height=2, command=self.stop)
        self.btn_stop.pack(side="left", padx=5)

    def load_config(self):
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, "r") as f:
                    config = json.load(f)
                    path = config.get("last_path", "")
                    if os.path.exists(path) and path:
                        self.path_var.set(path)
            except: pass

    def save_config(self):
        config = {"last_path": self.path_var.get()}
        try:
            with open(CONFIG_FILE, "w") as f:
                json.dump(config, f)
        except: pass

    def browse(self):
        current = self.path_var.get()
        start_dir = current if os.path.exists(current) else None
        path = filedialog.askdirectory(initialdir=start_dir)
        if path: 
            self.path_var.set(path)
            self.save_config()

    def stop(self): self.stop_event.set()

    def update_log(self, msg):
        self.log.config(state="normal")
        self.log.insert(tk.END, msg + "\n")
        self.log.see(tk.END)
        self.log.config(state="disabled")

    def is_power_of_two(self, n):
        return (n & (n - 1) == 0) and n != 0

    def scan_thread(self, scan_path):
        files_to_check = []
        for root, _, files in os.walk(scan_path):
            for f in files:
                files_to_check.append(os.path.join(root, f))
        
        self.root.after(0, lambda: self.progress.config(maximum=len(files_to_check)))

        # These are specific binary strings found inside "Pink" AssetBundles
        # even when the word 'Standard' is removed.
        bad_signatures = [
            b"URP", 
            b"ShaderGraph",
            b"DOTS",
            b"SRP",
            b"UniversalRenderPipeline",
            b"HLSL",
            b"Shaderlab",
            b"UnityEditor.Rendering",
            b"SubProgram",
            b"GLES3",
            b"d3d11",
            b"StandardUnlit"
        ]

        total_scanned = 0

        for i, file_path in enumerate(files_to_check):
            if self.stop_event.is_set(): break
            
            ext = os.path.splitext(file_path)[1].lower()
            rel_path = os.path.relpath(file_path, scan_path)
            mod_folder = rel_path.split(os.sep)[0]
            total_scanned += 1

            # 1. Texture Check
            if self.check_dim.get() and ext in [".png", ".jpg", ".dds", ".tga"]:
                try:
                    with Image.open(file_path) as img:
                        w, h = img.size
                        if not (self.is_power_of_two(w) and self.is_power_of_two(h)):
                            self.root.after(0, self.update_log, f"[WARN] [{mod_folder}] {rel_path} is {w}x{h}")
                except: pass

            # 2. Binary Signature Scan
            # Checks AssetBundles and internal data files
            if self.check_shaders.get() and ext not in [".dll", ".json", ".txt", ".md", ".xml", ".pdb"]:
                try:
                    if os.path.getsize(file_path) < 400000000:
                        with open(file_path, "rb") as f:
                            content = f.read() 
                            for sig in bad_signatures:
                                if sig in content:
                                    self.root.after(0, self.update_log, f"[ALERT] [{mod_folder}] INCOMPATIBLE SIGNATURE: '{sig.decode()}' in {rel_path}")
                                    break 
                except: pass

            # 3. Missing Manifests
            if self.check_manifest.get() and ext in [".unity3d", ".bundle"]:
                if not os.path.exists(file_path + ".manifest"):
                    self.root.after(0, self.update_log, f"[INFO] [{mod_folder}] No .manifest for {rel_path}")

            if i % 10 == 0: self.root.after(0, lambda v=i: self.progress.config(value=v))

        self.root.after(0, lambda: self.update_log(f"\n>>> SCAN FINISHED. Files processed: {total_scanned}"))
        self.root.after(0, self.finish_ui)

    def start_scan(self):
        path = self.path_var.get()
        if not os.path.exists(path): 
            messagebox.showerror("Error", "Invalid Path")
            return
        self.save_config()
        self.stop_event.clear()
        self.log.config(state="normal"); self.log.delete('1.0', tk.END); self.log.config(state="disabled")
        self.btn_run.config(state="disabled")
        threading.Thread(target=self.scan_thread, args=(path,), daemon=True).start()

    def finish_ui(self):
        self.btn_run.config(state="normal")
        self.progress.config(value=0)
        messagebox.showinfo("Scan Complete", "Signature diagnosis finished.")

if __name__ == "__main__":
    root = tk.Tk()
    app = UnityScannerGUI(root)
    root.mainloop()