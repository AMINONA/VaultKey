
@echo off

echo suppression...
timeout /t 2 > nul

del VaultKey.exe

echo renommage...
ren VaultKey_new.exe VaultKey.exe

echo lancement...
start "" VaultKey.exe

pause
del "%~f0"
