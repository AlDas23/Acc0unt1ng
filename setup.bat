@echo off
REM Check if Python is installed
python --version >nul 2>&1
IF ERRORLEVEL 1 (
    echo Python is not installed. Please install Python and try again.
    pause
    exit /b
)

python -m venv venv
call venv\Scripts\activate
python -m pip install --upgrade pip

if exist requirements.txt (
    pip install -r requirements.txt
) else (
    echo requirements.txt not found.
    pause
    exit /b
)

echo Setup complete. To activate the virtual environment, run:
echo call venv\Scripts\activate
pause
