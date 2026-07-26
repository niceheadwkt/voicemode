@echo off
setlocal
set KOKORO_DIR=%USERPROFILE%\.voicemode\services\kokoro

if not exist "%KOKORO_DIR%" (
    echo [ERROR] Kokoro service directory not found at %KOKORO_DIR%
    pause
    exit /b 1
)

cd /d "%KOKORO_DIR%"

echo ==================================================
echo         Starting Local Kokoro TTS Service
echo ==================================================

set PYTHONUTF8=1
set PROJECT_ROOT=%KOKORO_DIR%
set USE_GPU=false
set USE_ONNX=false
set PYTHONPATH=%KOKORO_DIR%;%KOKORO_DIR%\api
set MODEL_DIR=src/models
set VOICES_DIR=src/voices/v1_0
set WEB_PLAYER_PATH=%KOKORO_DIR%\web

echo Installing/Syncing Kokoro CPU dependencies...
uv pip install -e ".[cpu]"

echo Checking Kokoro voice models...
uv run --no-sync python docker/scripts/download_model.py --output api/src/models/v1_0

echo --------------------------------------------------
echo Starting Kokoro FastAPI TTS server on port 8880 ...
echo --------------------------------------------------
uv run --no-sync uvicorn api.src.main:app --host 127.0.0.1 --port 8880

pause
