@echo off
echo ========================================
echo Custom LLM Platform Setup
echo ========================================

REM Activate virtual environment
echo [1/4] Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ERROR: Failed to activate virtual environment
    pause
    exit /b 1
)

REM Upgrade pip
echo [2/4] Upgrading pip...
python -m pip install --upgrade pip

REM Install PyTorch with CUDA support
echo [3/4] Installing PyTorch (this may take 5-10 minutes)...
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
if errorlevel 1 (
    echo WARNING: PyTorch installation had issues. Trying CPU version...
    pip install torch torchvision torchaudio
)

REM Install other requirements
echo [4/4] Installing other dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install some dependencies
    echo Please check the error messages above
    pause
    exit /b 1
)

echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo Next steps:
echo   1. Test: python main.py --prompt "Hello AI" --quantized
echo   2. Chat: python main.py --interactive --quantized
echo   3. API:  python api_server.py
echo.
pause
