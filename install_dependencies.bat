@echo off
echo ========================================
echo Installing Core ML Dependencies
echo ========================================

REM Activate virtual environment
call venv\Scripts\activate.bat

echo.
echo [1/4] Installing PyTorch (this may take a while)...
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

echo.
echo [2/4] Installing Transformers and ML libraries...
pip install transformers accelerate datasets bitsandbytes

echo.
echo [3/4] Installing API framework...
pip install fastapi uvicorn pydantic python-multipart

echo.
echo [4/4] Verifying installation...
python -c "import torch; print(f'PyTorch {torch.__version__} installed successfully')"
python -c "import transformers; print(f'Transformers {transformers.__version__} installed successfully')"
python -c "import fastapi; print(f'FastAPI installed successfully')"

echo.
echo ========================================
echo Installation Complete!
echo ========================================
echo.
echo You can now run:
echo   python main.py --interactive --quantized
echo   python api_server.py
echo.
pause
