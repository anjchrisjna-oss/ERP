@echo off
setlocal
set ROOT=%~dp0..\..
cd /d %ROOT%
if not exist var mkdir var
bash scripts/run_local_erp.sh ./var/erp.sqlite3 8765
