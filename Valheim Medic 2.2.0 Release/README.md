=====================================================
VALHEIM MOD MEDIC v2.2.0
A diagnostic tool for Valheim modders to identify "Pink Texture" issues, shader incompatibilities, and AssetBundle errors.

[ DIAGNOSTIC CHECKS ]
Aggressive Shader Scan: Scans all files and DLLs for incompatible binary shader data that cause "Pink" models.

Texture Dimension Check: Identifies textures that are NOT 'Power of Two' (e.g., 256, 512, 1024), which cause blurry or pink textures in Unity.

Missing Manifests: Checks if AssetBundles are missing their required .manifest file.

JSON & Path Detection: Automatically detects the mod's JSON configuration and directory structure to ensure valid installation paths.

[ HOW TO USE ]
This project uses uv to ensure all users run the tool with the correct library versions.

Install uv (one-time setup):
Run this in PowerShell:

PowerShell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
Run the Tool:
In your terminal, navigate to the folder and run:

PowerShell
uv run valheim_medic.py
Start Diagnosis: Browse to your Valheim plugins folder and click 'Start Diagnosis'.

