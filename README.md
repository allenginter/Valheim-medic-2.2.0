# Valheim Mod Medic v2.3

Updated and added DEEP_Scan3 to the file list. This scans for SRP and URP conflicts as well as contains all previous forms.
The EXE files does not have this feature as it is primarily a modders tool.

A diagnostic tool to find "Pink" shader errors and texture issues in Valheim mods.

## How to Run
This project uses **uv** to ensure all modders use the same library versions.

1. **Install uv** (one-time setup):
   Run this in PowerShell:
   ```powershell
   powershell -ExecutionPolicy ByPass -c "irm [https://astral.sh/uv/install.ps1](https://astral.sh/uv/install.ps1) | iex"
Launch the Tool:
Run this in the folder:

PowerShell
uv run valheim_medic.py
Diagnostic Checks
Aggressive Shader Scan: Scans all files and DLLs for incompatible binary shader data.

Texture Check: Identifies non-Power-of-Two textures that cause performance lag.

Manifest Check: Flags missing manifest files for Unity asset bundles.
