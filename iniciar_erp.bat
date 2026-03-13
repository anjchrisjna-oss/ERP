@echo off
setlocal
set ROOT=%~dp0
cd /d %ROOT%
if "%1"=="" (
  set PORT=8765
) else (
  set PORT=%1
)

if "%2"=="" (
  set DB=var\erp.sqlite3
) else (
  set DB=%2
)

echo Iniciando ERP local en http://127.0.0.1:%PORT%
python app\start_erp.py %PORT% %DB%
