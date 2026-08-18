@echo off
rem Run this after exporting new models from MagicaVoxel.
rem Gallery mode reads models/manifest.json, and a browser cannot list a folder
rem for itself, so the list has to be written down.
cd /D %~dp0
python make_manifest.py
echo.
pause
