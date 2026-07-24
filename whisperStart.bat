@echo off
setlocal enabledelayedexpansion

set BASE_DIR=C:\Users\ch26788\.voicemode\services\whisper
set SERVICE_DIR=!BASE_DIR!\Release
set MODEL_DIR=!BASE_DIR!\models
set MODEL_PATH=!MODEL_DIR!\ggml-base.bin

set PY_EXE=python
if exist "C:\aiTest\voicemode\.venv\Scripts\python.exe" (
    set PY_EXE=C:\aiTest\voicemode\.venv\Scripts\python.exe
)

if not exist "!BASE_DIR!" mkdir "!BASE_DIR!"
if not exist "!MODEL_DIR!" mkdir "!MODEL_DIR!"

echo ==================================================
echo          Local Whisper Service Status Check
echo ==================================================

rem Check if any executable exists in !SERVICE_DIR!
set EXE_EXISTS=0
if exist "!SERVICE_DIR!\server.exe" set EXE_EXISTS=1
if exist "!SERVICE_DIR!\whisper-server.exe" set EXE_EXISTS=1
if exist "!SERVICE_DIR!\main.exe" set EXE_EXISTS=1

if !EXE_EXISTS! neq 0 goto :skip_download_exe

echo [INFO] Whisper server executable not found in !SERVICE_DIR!.
echo Downloading Windows CPU precompiled whisper-server ...
!PY_EXE! -c "import urllib.request, ssl; ssl._create_default_https_context = ssl._create_unverified_context; urllib.request.urlretrieve('https://github.com/ggml-org/whisper.cpp/releases/download/v1.9.1/whisper-blas-bin-x64.zip', r'!BASE_DIR!\whisper.zip')"

if not exist "!BASE_DIR!\whisper.zip" goto :download_exe_failed

echo Unpacking whisper.zip ...
powershell -Command "Expand-Archive -Path '!BASE_DIR!\whisper.zip' -DestinationPath '!BASE_DIR!' -Force"
del "!BASE_DIR!\whisper.zip"

rem Verify again after unpack
if exist "!SERVICE_DIR!\server.exe" set EXE_EXISTS=1
if exist "!SERVICE_DIR!\whisper-server.exe" set EXE_EXISTS=1
if exist "!SERVICE_DIR!\main.exe" set EXE_EXISTS=1

if !EXE_EXISTS! neq 0 goto :skip_download_exe
goto :download_exe_failed

:download_exe_failed
echo [ERROR] Download failed. Please download whisper-blas-bin-x64.zip manually from:
echo https://github.com/ggml-org/whisper.cpp/releases/tag/v1.9.1
echo and unpack its files into: !SERVICE_DIR!
pause
exit /b 1

:skip_download_exe


if exist "!MODEL_PATH!" goto :skip_download_model

echo [INFO] ggml-base.bin model not found.
echo Downloading ggml-base.bin model (approx. 142MB) ...
!PY_EXE! -c "import urllib.request, ssl; ssl._create_default_https_context = ssl._create_unverified_context; urllib.request.urlretrieve('https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-base.bin', r'!MODEL_PATH!')"

if exist "!MODEL_PATH!" goto :skip_download_model

echo [ERROR] Model download failed. Please download it manually and put it into !MODEL_DIR!:
echo https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-base.bin
pause
exit /b 1

:skip_download_model


echo --------------------------------------------------
echo Starting local Whisper server on port 2022 ...
echo --------------------------------------------------
cd /d "!SERVICE_DIR!"

if exist "whisper-server.exe" goto :run_whisper_server
if exist "server.exe" goto :run_server
if exist "main.exe" goto :run_main

echo [ERROR] Cannot find any executable, startup failed.
pause
exit /b 1

:run_whisper_server
whisper-server.exe -m "!MODEL_PATH!" --port 2022 --host 127.0.0.1 --inference-path "/v1/audio/transcriptions"
goto :end

:run_server
server.exe -m "!MODEL_PATH!" --port 2022 --host 127.0.0.1 --inference-path "/v1/audio/transcriptions"
goto :end

:run_main
main.exe -m "!MODEL_PATH!" --port 2022 --host 127.0.0.1 --inference-path "/v1/audio/transcriptions"
goto :end

:end
pause
