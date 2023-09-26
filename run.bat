@echo off

echo "Labor PlagScanner by Erik Ilgenstein"

rem 1. Prüfe die Python Version
python --version | findstr /i "3.[1-9]" > nul
if errorlevel 1 (
    echo "Die Python Version muss > 10 sein."
    pause
    exit /b 1
)

rem 2. Aktiviere das venv
if not exist .venv (
	echo "Umgebung wird vorbereitet..."
    python -m venv .venv
)
call .venv\Scripts\activate

rem Restliche Schritte wie gehabt
python scripts/check_requirements.py requirements.txt
if errorlevel 1 (
    echo Installing missing packages...
    pip install -r requirements.txt
)
start pythonw run.py
app.Activate()