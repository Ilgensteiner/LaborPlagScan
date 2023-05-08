#!/bin/bash
python scripts/check_requirements.py requirements.txt
if [ $? -eq 1 ]
then
    echo Installing missing packages...
    pip install -r requirements.txt
fi
nohup python3 main.py &
