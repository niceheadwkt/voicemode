import os
import sys
import time
import requests
import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import subprocess
import ctypes
import ssl

# Bypass SSL check for request
ssl._create_default_https_context = ssl._create_unverified_context

def copy_and_paste(text):
    # 1. Set clipboard value safely via PowerShell
    escaped_text = text.replace("'", "''")
    subprocess.run(["powershell", "-Command", f"Set-Clipboard -Value '{escaped_text}'"], shell=True)
    
    # 2. Simulate Ctrl+V to paste
    KEYEVENTF_KEYUP = 0x0002
    ctypes.windll.user32.keybd_event(0x11, 0, 0, 0) # Ctrl down
    ctypes.windll.user32.keybd_event(0x56, 0, 0, 0) # V down
    time.sleep(0.05)
    ctypes.windll.user32.keybd_event(0x56, 0, KEYEVENTF_KEYUP, 0) # V up
    ctypes.windll.user32.keybd_event(0x11, 0, KEYEVENTF_KEYUP, 0) # Ctrl up
    print("✓ Text pasted to active window!")

def record_audio(duration=6, fs=16000):
    print(f"\n[Recording] Speaking for {duration} seconds... (Speak now!)")
    try:
        recording = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
        sd.wait()  # Wait until the recording is finished
        return recording
    except KeyboardInterrupt:
        sd.stop()
        print("\n[Recording] Interrupted early.")
        return None

def transcribe(audio_data, fs=16000):
    temp_wav = "temp_dictate.wav"
    wav.write(temp_wav, fs, audio_data)
    
    url = "http://127.0.0.1:2022/v1/audio/transcriptions"
    print("[Whisper] Transcribing voice locally...")
    
    try:
        with open(temp_wav, 'rb') as f:
            files = {'file': (temp_wav, f, 'audio/wav')}
            data = {'model': 'ggml-base.bin', 'language': 'zh', 'prompt': '繁體中文'}
            resp = requests.post(url, files=files, data=data, timeout=30)
            
        if resp.status_code == 200:
            text = resp.json().get("text", "").strip()
            return text
        else:
            print(f"Error from Whisper server: {resp.status_code} {resp.text}")
            return None
    except Exception as e:
        print(f"Failed to connect to Whisper server: {e}")
        return None
    finally:
        if os.path.exists(temp_wav):
            os.remove(temp_wav)

def main():
    print("==================================================")
    print("     Antigravity Local Offline Dictation Helper")
    print("==================================================")
    print("Usage: Focus your cursor on the chat input window,")
    print("       then run this script. Speak your message.")
    print("       It will transcribe and auto-paste the text.")
    print("==================================================")
    
    # Give user 2 seconds to focus on the chat input window!
    print("\n[Prep] Please click on your Chat Input Box now! (Starting in 2s)")
    for i in range(2, 0, -1):
        print(f"{i}...")
        time.sleep(1)
        
    audio = record_audio(duration=6)  # Record 6 seconds
    if audio is not None and np.any(audio):
        text = transcribe(audio)
        if text:
            print(f"\n[Transcribed Text]: {text}")
            copy_and_paste(text)
        else:
            print("\n[Failed] Could not transcribe audio.")
    else:
        print("\n[Failed] No audio recorded.")

if __name__ == '__main__':
    main()
