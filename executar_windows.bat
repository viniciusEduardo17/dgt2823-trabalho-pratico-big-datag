@echo off
setlocal
cd /d "%~dp0"
echo =====================================================
echo DGT2823 - Trabalho Pratico - Execucao automatica
echo =====================================================
if exist ".venv\Scripts\python.exe" goto instalar
where py >nul 2>&1
if not errorlevel 1 (
    py -3 -m venv .venv
) else (
    python -m venv .venv
)
if errorlevel 1 goto erro
:instalar
echo Instalando/verificando Pandas...
".venv\Scripts\python.exe" -m pip install "pandas>=2.0,<3.0"
if errorlevel 1 goto erro
echo Executando limpeza dos dados...
".venv\Scripts\python.exe" main.py
if errorlevel 1 goto erro
echo CONCLUIDO: confira os arquivos na pasta resultados.
pause
exit /b 0
:erro
echo ERRO: verifique a instalacao do Python.
pause
exit /b 1
