@echo off
cd /d "%~dp0"


REM Set the default parameters here
set PARAMS= 


echo Starting with parameters: %PARAMS%
call venv\Scripts\activate.bat
python run.py %PARAMS%

pause