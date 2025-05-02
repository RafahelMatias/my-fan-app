@echo off
REM Muda para a pasta do script (garante paths relativos)
cd /d "%~dp0"

REM 1) Inicia o backend numa janela separada
start "Backend" cmd /k "call .venv\Scripts\Activate && uvicorn main:app --reload --host 0.0.0.0 --port 8000"

REM 2) Inicia o frontend
start "Frontend" cmd /k "npm run dev"

REM Fecha esta janela de controle
exit
