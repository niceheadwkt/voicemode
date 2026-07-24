# VoiceMode 參數參考指南

## 核心參數

### message (必要)
**類型：** 字串 (string)
要向使用者播放的語音訊息。

### wait_for_response
**類型：** 布林值 (boolean)（預設：true）
播放完語音後，是否聆聽使用者的語音回覆。

## 時間參數

### listen_duration_max
**類型：** 數字 (number)（預設：120.0 秒）
聆聽回覆的最長時間。工具的靜音偵測機制通常能很好地處理此限制。

**何時需要覆寫：**
- 靜音偵測已停用且您需要特定逾時時間
- 預期回覆時間非常長 (>120 秒)
- 特殊的時間排程需求

**通常建議：** 保留預設值，讓靜音偵測自動處理。

### listen_duration_min
**類型：** 數字 (number)（預設：2.0 秒）
在靜音偵測被觸發停止錄音前的最少錄音時間。

**適用情境：**
- 複雜問題：2-3 秒
- 開放式提問：3-5 秒
- 快速簡短回答：0.5-1 秒

### timeout (已棄用)
請改用 `listen_duration_max`。僅適用於 LiveKit 傳輸協定。

## 語音與 TTS 參數

### voice
**類型：** 字串 (string)（選用）
覆寫 TTS 的語音選擇。

**何時指定：**
- 使用者明確要求特定語音
- 說非英語語言時（請參閱多國語言資源說明）

**範例：**
- OpenAI: nova, shimmer, alloy, echo, fable, onyx
- Kokoro: zf_xiaobei (中文女聲推薦), zm_xiaoming (中文男聲), af_sky, af_sarah 等

**重要提示：** 請不要使用 'coral' 語音。

### tts_provider
**類型：** "openai" | "kokoro"（選用）
TTS 語音合成提供者。

**何時指定：**
- 使用者明確要求特定的語音提供者
- 進行容錯移轉 (Failover) 測試
- 非英語語言（通常推薦使用 kokoro）

**通常建議：** 讓系統自動選擇。

### tts_model
**類型：** 字串 (string)（選用）
TTS 語音合成模型。

**選項：**
- `tts-1` - 標準音質 (OpenAI)
- `tts-1-hd` - 高解析音質 (OpenAI)
- `gpt-4o-mini-tts` - 支援情緒語調表達 (OpenAI)

**何時指定：**
- 需要高解析音質 (HD)
- 希望能表現情緒語調（需搭配 tts_instructions）

**通常建議：** 讓系統自動選擇。

### tts_instructions
**類型：** 字串 (string)（選用）
用於情緒語音表達的語調/風格引導說明。

**要求：** 僅在使用 `tts_model="gpt-4o-mini-tts"` 時有效。

**範例：**
- "用開朗活潑的語調說話"
- "聽起來很生氣"
- "表現得非常悲傷"
- "語氣聽起來很緊急且關切"

**備註：** 使用 OpenAI API，將產生額外費用（每分鐘約 $0.02 美元）。

### speed
**類型：** 數字 (number)（範圍：0.25 到 4.0，選用）
語音播速。

**範例：**
- 0.5 = 半速
- 1.0 = 正常播速（預設）
- 1.5 = 1.5 倍速
- 2.0 = 雙倍速

**支援提供者：** OpenAI 與 Kokoro 皆支援。

## 音訊與靜音偵測

### disable_silence_detection
**類型：** 布林值 (boolean)（預設：false）
停用自動靜音偵測。

**何時使用：**
- 使用者回報說話被強行切斷
- 吵雜的背景環境
- 需要頻繁停頓的口述記錄模式

**通常建議：** 保持啟用狀態 (false)。

### vad_aggressiveness
**類型：** 整數 (integer) 0-3（選用）
語音活動偵測 (VAD) 的嚴格度等級。

**等級：**
- `0` - 最寬鬆，錄入較多音訊，可能包含非人聲背景音
- `1` - 稍嚴格的過濾
- `2` - 平衡 - 適合大多數環境
- `3` - 最嚴格，高強度偵測（預設） - 最適合過濾背景雜音

**何時調整：**
- 安靜房間：使用 0-1 以完整捕獲所有輕聲說話
- 一般居家/辦公室：使用預設值 (3)
- 吵雜的咖啡廳/戶外：使用 3

### chime_leading_silence
**類型：** 數字 (number)（秒數，選用）
在提示音開始前加入的靜音秒數。

**適用情境：** 藍牙裝置需要音訊緩衝啟動時間（例如：1.0 秒）。

**預設值：** 使用環境變數 `VOICEMODE_CHIME_LEADING_SILENCE` (0.1 秒)。

### chime_trailing_silence
**類型：** 數字 (number)（秒數，選用）
在提示音結束後加入的靜音秒數。

**適用情境：** 防止提示音被系統過早切斷（例如：0.5 秒）。

**預設值：** 使用環境變數 `VOICEMODE_CHIME_TRAILING_SILENCE` (0.2 秒)。

## 詞彙偏好調整 (STT 提示詞)

### VOICEMODE_STT_PROMPT
**類型：** 環境變數（字串，選用）

利用提示詞引導來調整 Whisper 的語音辨識偏好。這有助於提高 Whisper 對專有名詞、程式碼術語、特定人名以及可能誤聽的領域詞彙的辨識精準度。

**運作原理：**

Whisper 使用 "prompt" 欄位來引導其辨識方向。藉由提供您經常使用的單字和片語，模型會被預先引導以正確辨識這些詞彙。這對於以下項目特別有用：

- **人名/名稱：** 人名、寵物名、地名（例如：Sense Bar, Tali, Mike）
- **技術術語：** 指令名稱、工具（例如：tmux, kubectl, pytest, voicemode）
- **專案詞彙：** 您專案代碼庫所特有的詞彙
- **縮寫：** 您領域內常見的縮寫字

**格式彈性：**

以下所有格式都具有同等效果：
```bash
# 逗號分隔
export VOICEMODE_STT_PROMPT="tmux, Tali, VoiceMode, kubectl, 繁體中文"

# 空格分隔
export VOICEMODE_STT_PROMPT="tmux Tali VoiceMode kubectl 繁體中文"

# 句子格式 (有助於提供語境)
export VOICEMODE_STT_PROMPT="使用者經常討論 Tali, tmux 工作階段, 以及 繁體中文 程式開發。"
```

**Token 限制：**

Whisper 僅使用提示詞中的最後 224 個 tokens。實務上這代表：
- 簡短字詞列表：完全沒有限制（最常見的用法）
- 長提示詞：只有最後的部分有效，因此請將最重要的詞彙放在最後面
- 典型字彙量：50-100 個字彙可輕鬆容納於限制中

**何時使用：**

- Whisper 經常誤聽特定的中文或英文詞彙
- 您使用不尋常的專有名詞或技術術語
- 領域特有詞彙無法被正確辨識

**疑難排解提示：**

如果加入提示詞後某個單字仍然被誤認，請嘗試將其置於語境中：例如不要只寫 "Tali"，改用 "我的狗 Tali" 或 "帶 Tali 出去散步"。

**另請參閱：** [疑難排解 - 單字被誤認](troubleshooting.md#特定單字一直被誤認)

## 音訊格式與回饋

### audio_format
**類型：** 字串 (string)（選用）
覆寫音訊格式。

**選項：** pcm, mp3, wav, flac, aac, opus

**預設值：** 使用環境變數 `VOICEMODE_TTS_AUDIO_FORMAT`。

### chime_enabled
**類型：** 布林值 | 字串（選用）
啟用或停用音訊回饋提示音。

**預設值：** 使用環境變數 `VOICEMODE_CHIME_ENABLED`。

### skip_tts
**類型：** 布林值 (boolean)（選用）
跳過文字轉語音合成，僅顯示文字。

**值：**
- `true` - 跳過 TTS，回覆速度極快，僅文字顯示
- `false` - 總是使用 TTS
- `null` (預設) - 遵循環境變數 `VOICEMODE_SKIP_TTS` 的設定

**適用情境：**
- 快速的開發與測試迭代
- 當不需要語音回覆時
- 純文字模式

## 傳輸參數

### transport
**類型：** "auto" | "local" | "livekit"（預設："auto"）
傳輸方式選擇。

**選項：**
- `auto` - 優先嘗試 LiveKit，若失敗則退回到 local 模式
- `local` - 直接存取本機麥克風與揚聲器
- `livekit` - 基於聊天室的傳輸通訊

### room_name
**類型：** 字串 (string)（選用）
LiveKit 的房間名稱。

**僅限於：** `livekit` 傳輸模式。
**預設值：** 若為空，則會自動偵測。

## 端點規範

STT/TTS 服務必須提供與 OpenAI 相容的端點：
- Whisper/Kokoro 必須在以下路徑提供服務：
  - `/v1/audio/transcriptions` (STT 語音轉文字)
  - `/v1/audio/speech` (TTS 文字轉語音)

若發生連線錯誤，系統會清楚回報所嘗試連線的端點路徑。
