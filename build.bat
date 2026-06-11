py -3.13 -m PyInstaller ^
--onefile ^
--windowed ^
--icon=icon.ico ^
--name VaultKey ^
--add-data "index.html;." ^
--collect-all cryptography ^
--collect-all requests ^
--collect-all webview ^
projet.py