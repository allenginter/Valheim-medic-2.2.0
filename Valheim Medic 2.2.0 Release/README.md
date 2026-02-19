=====================================================
ValheimTextureMedic
A diagnostic tool for Valheim modders to identify "Pink Texture" issues, shader incompatibilities, and AssetBundle errors.

[ DIAGNOSTIC CHECKS ]
Aggressive Shader Scan: Scans all files and DLLs for incompatible binary shader data that cause "Pink" models.

Texture Dimension Check: Identifies textures that are NOT 'Power of Two' (e.g., 256, 512, 1024), which cause blurry or pink textures in Unity.

Missing Manifests: Checks if AssetBundles are missing their required .manifest file.

JSON & Path Detection: Automatically detects the mod's JSON configuration and directory structure to ensure valid installation paths.

This release contaisn  the EXE for users and the PY for modders. Modders can use either, but the PY allows for less concern 

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

Aplogies for the releasing of the PY and not the EXE file. I am new to the Thunderstore Format and got flustered and confused myself. There is a newer build that is in testing that will detect SRP and URP issues for modders.

