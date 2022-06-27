@echo off

call %~dp0venv\Scripts\activate
cd %~dp0

set TOKEN=token

python bot_main.py

pause
