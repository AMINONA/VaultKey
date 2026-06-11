@echo off

py -3.13 -m PyInstaller ^
 --onefile ^
 --windowed ^
 --name "VaultKey" ^
 --collect-all cryptography ^
 --collect-all tkinter ^
 --add-data "index.html;." ^
 projet.py

pause