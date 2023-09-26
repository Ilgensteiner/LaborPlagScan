#!/bin/bash

echo "Labor PlagScanner by Erik Ilgenstein"

# 1. Prüfe die Python Version
python --version | grep -q "^3\.[1-9]\.[0-9]$"
if [[ $? -eq 0 ]]; then
  echo "Die Python Version muss mindestens 3.10 sein."
  exit 1
fi

# 2. Aktiviere das venv
if [ ! -d .venv ]; then
  echo "Umgebung wird vorbereitet..."
  python -m venv .venv
fi
source .venv/bin/activate

# Restliche Schritte wie gehabt
python scripts/check_requirements.py requirements.txt
if [[ $? -eq 1 ]]; then
  echo "Fehlende Pakete werden installiert..."
  pip install -r requirements.txt
fi
start pythonw run.py
app.Activate()