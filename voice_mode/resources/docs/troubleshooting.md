# VoiceMode 疑難排解指南

## 音訊問題

### 使用者說話在句中被切斷

**問題：** 靜音偵測過早停止錄音。

**解決方案：**
1. 增加 `listen_duration_min`（最少錄音秒數）：
   ```python
   converse("您在想些什麼？", listen_duration_min=5.0)
   ```

2. 降低 VAD 偵測嚴格度：
   ```python
   converse("跟我多說一些", vad_aggressiveness=0)
   ```

3. 完全停用靜音偵測：
   ```python
   converse("請詳細描述一下", disable_silence_detection=True)
   ```

### 背景雜音觸發錯誤錄音

**問題：** VAD 將非人聲的背景雜音誤判為說話聲。

**解決方案：**
1. 提高 VAD 嚴格度：
   ```python
   converse("你聽得見我嗎？", vad_aggressiveness=3)
   ```

2. 檢查環境雜音音量。
3. 使用高品質的麥克風。

### 提示音被切斷

**問題：** 藍牙耳機或系統音訊啟動延遲。

**解決方案：**
1. 增加前置靜音秒數：
   ```python
   converse("你好", chime_leading_silence=1.0)
   ```

2. 增加後置靜音秒數：
   ```python
   converse("你好", chime_trailing_silence=0.5)
   ```

3. 同時增加兩者：
   ```python
   converse("你好", chime_leading_silence=1.0, chime_trailing_silence=0.5)
   ```

### 沒有聲音輸出

**問題：** TTS 無法播放語音。

**解決方案：**
1. 檢查是否啟用了 `skip_tts`。
2. 驗證環境變數 `VOICEMODE_SKIP_TTS` 是否設為 true。
3. 強制啟用 TTS：
   ```python
   converse("測試訊息", skip_tts=False)
   ```
4. 檢查系統的音訊輸出裝置設定。
5. 驗證 TTS 服務端點是否正常運作。

## 語音活動偵測 (VAD)

### 了解 VAD 嚴格度等級

- **0 (最寬鬆)：** 捕獲所有聲音，包括背景雜音。
- **1 (低)：** 稍微嚴格，適合安靜環境。
- **2 (平衡 - 預設)：** 適合一般居家/辦公室。
- **3 (最嚴格)：** 嚴格的人聲偵測，過濾絕大多數雜音。

### 何時調整 VAD

| 環境 | 推薦設定 | 原因 |
|-------------|-------------------|---------|
| 安靜房間 | 0-1 | 確保不會漏掉輕聲說話 |
| 居家辦公室 | 2 | 平衡設定（預設） |
| 忙碌辦公室 | 2-3 | 過濾打字聲與他人交談聲 |
| 咖啡廳/公共場所 | 3 | 過濾高強度背景雜音 |
| 戶外 | 3 | 過濾風聲與交通雜音 |
| 口述記錄模式 | 0-1 + 較高 listen_duration_min | 允許思考時的短暫停頓 |

## 連線問題

### STT/TTS 端點錯誤

**問題：** 無法連線至語音服務。

**檢查項目：**
1. 確認服務是否提供了與 OpenAI 相容的端點：
   - `/v1/audio/transcriptions` (STT 語音轉文字)
   - `/v1/audio/speech` (TTS 文字轉語音)

2. 確認環境變數設定正確：
   - `OPENAI_API_KEY` (若使用 OpenAI 雲端服務)
   - 本地服務 URL（如 Whisper 或 Kokoro 的端點）

3. 確認與這些服務的網路連線狀態。

4. 檢查服務的錯誤日誌。

### 傳輸協定問題

**問題：** LiveKit 或 local 本地傳輸失敗。

**解決方案：**
1. 嘗試不同的傳輸方式：
   ```python
   # 強制使用本地傳輸 (direct microphone)
   converse("測試", transport="local")
 
   # 強制使用 LiveKit 傳輸
   converse("測試", transport="livekit")
   ```

2. 檢查 LiveKit 房間設定。
3. 驗證終端機或應用程式的麥克風存取權限。

### 逾時問題

**問題：** 語音操作逾時。

**解決方案：**
1. 增加最大聆聽時間：
   ```python
   command("請詳述內容", listen_duration_max=300)
   ```

2. 檢查與語音服務之間的網路延遲。
3. 驗證服務本身是否仍有回應。

## 語音品質問題

### 發音不正確

**問題：** 單字發音錯誤（特別是非英語語言）。

**解決方案：**
1. 對於非英語，使用 Kokoro 時請指定適當的語音：
   ```python
   converse("Bonjour", voice="ff_siwis", tts_provider="kokoro")
   ```

2. 請參閱 `voicemode-languages` 資源以尋找適用特定語言的語音名稱。

### 語意機械化/不自然

**問題：** 語音聽起來太像機器人。

**解決方案：**
1. 嘗試不同的語音：
   ```python
   converse("你好", voice="nova")  # OpenAI
   converse("你好", voice="zf_xiaobei", tts_provider="kokoro")
   ```

2. 使用 HD 高解析模型以獲得更好的品質：
   ```python
   converse("你好", tts_model="tts-1-hd")
   ```

3. 加入情緒語調指引：
   ```python
   converse(
       "我非常高興能為您提供協助！",
       tts_model="gpt-4o-mini-tts",
       tts_instructions="語氣溫暖且友善"
   )
   ```

### 語音速度太快或太慢

**問題：** 預設播速不符合您的偏好。

**解決方案：** 調整 speed 播速：
   ```python
   # 變慢
   converse("複雜的技術細節", speed=0.8)
 
   # 變快
   converse("快速更新", speed=1.5)
   ```

## 辨識問題

### STT 無法偵測到說話

**問題：** 您的說話未被轉錄為文字。

**解決方案：**
1. 檢查麥克風是否正常運作。
2. 驗證麥克風的系統存取權限。
3. 增加錄音秒數：
   ```python
   converse("你覺得呢？", listen_duration_min=5.0)
   ```
4. 停用靜音偵測以確認是否為 VAD 判斷問題：
   ```python
   converse("測試", disable_silence_detection=True, listen_duration_max=10)
   ```

### 轉錄結果不正確

**問題：** 語音辨識的文字有誤。

**解決方案：**
1. 說話更清晰、大聲一些。
2. 減少背景雜音。
3. 根據您的環境調整 VAD 嚴格度。
4. 使用高品質的麥克風。
5. 檢查您的 STT 語音服務設定。

### 特定單字一直被誤認

**問題：** 某些單字、專有名詞或英文簡寫即使說得很清楚，也一再被辨識錯誤。

**症狀：**
- 同一個單字總是辨識錯誤（例如：將 "tmux" 辨識為 "T-Mux" 或 "踢馬克"）
- 人名拼寫錯誤（例如：將 "Tali" 辨識為 "Talley" 或 "多力"）
- 技術術語損毀（例如：將 "kubectl" 辨識為 "cube control"）

**解決方案：** 使用環境變數 `VOICEMODE_STT_PROMPT` 來設定詞彙偏好。

在您的 `~/.voicemode/voicemode.env` 中設定您常用的詞彙：
```bash
VOICEMODE_STT_PROMPT="tmux, Tali, kubectl, pytest, VoiceMode, 繁體中文"
```

這會「預引導」Whisper 以正確辨識這些特定術語。

**請參閱：** [參數說明 - 詞彙偏好調整](parameters.md#詞彙偏好調整-stt-提示詞) 以取得詳細的配置選項。

## 效能問題

### 回應時間緩慢

**問題：** 在說話與收到回應之間有很長的延遲。

**可能原因：**
1. 與 STT/TTS 語音服務之間的網路延遲。
2. 伺服器負載過重。
3. 音訊檔案過大。

**解決方案：**
1. 如果可能，使用較低品質的音訊格式以減少傳輸時間。
2. 檢查語音服務的回應時間。
3. 考慮在本地運行 STT/TTS 語音服務（Nvidia CUDA 或 Apple Silicon 本地運行快得多）。
4. 在開發與測試時使用 `skip_tts=True`：
   ```python
   converse("快速測試", skip_tts=True)
   ```

## 常見錯誤

### 使用 coral 語音
❌ **錯誤：** `voice="coral"` - 此語音不受支援
✅ **正確：** 使用受支援的語音（如 nova, shimmer, zf_xiaobei 等）

### 說中文/非英語時沒有指定語音
❌ **錯誤：** `converse("你好")`
✅ **正確：** `converse("你好", voice="zf_xiaobei", tts_provider="kokoro")`

### 將 listen_duration_max 設得太低
❌ **錯誤：** 面對複雜問題時設定 `listen_duration_max=5`
✅ **正確：** 使用預設值 (120) 或更高，以防回應被截斷

### 無謂地覆寫預設值
❌ **錯誤：** 在沒有特別需求的情況下，每一次呼叫都手動指定 `voice`, `tts_provider`, `tts_model`
✅ **正確：** 除非有特定需求，否則讓系統自動選擇以確保最優解

## 取得更多協助

如果問題持續存在：
1. 檢查語音服務的日誌。
2. 驗證環境變數與 .env 檔配置。
3. 先用最少、最單純的參數進行測試。
4. 每次僅添加一個參數，以隔離出問題所在。

## 另請參閱
- [參數說明](parameters.md) - 完整參數參考（包含 [詞彙偏好](parameters.md#%e8%a9%9e%e5%8c%af%e5%81%8f%e5%a5%bd%e8%aa%bf%e6%95%b4-stt-%e6%8f%90%e7%a4%ba%e8%a9%9e)）
- [對話模式](patterns.md) - 最佳實踐模式
- [多國語言支援](languages.md) - 針對各國語言的語音配置
