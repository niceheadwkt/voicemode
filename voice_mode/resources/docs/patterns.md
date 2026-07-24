# VoiceMode 對話模式指南

## 並行操作模式 (推薦)

執行不需要使用者確認的動作時，使用 `wait_for_response=False` 來播放語音，同時在背景執行其他工具。這能建立自然流暢的互動體驗。

### 模式範例
```python
converse("正在更新狀態...", wait_for_response=False)
# 立即並行執行其他工具
```

語音會在您的背景工作執行的同時播放。

### 好處
- 背景操作時不會有尷尬的靜音空檔
- 使用者能清楚知道目前進度
- 對話流程更為自然
- 提供更優質的使用者體驗

## 並行模式範例

### 搜尋過程旁白
```python
converse("正在為您搜尋該檔案", wait_for_response=False)
# 立即執行：
Grep(pattern="function_name", output_mode="files_with_matches")
```

### 處理進度更新
```python
converse("正在分析螢幕截圖", wait_for_response=False)
# 立即執行：
Read(file_path="/path/to/screenshot.png")
```

### 建立狀態
```python
converse("現在開始為您建立該文件", wait_for_response=False)
# 立即執行：
Write(file_path="/path/to/file.md", content="...")
```

### 快速確認
```python
converse("完成！檔案已儲存", wait_for_response=False)
# 簡單的確認不需要等待使用者回覆
```

## 何時使用並行模式

✅ **適合使用並行模式的情境：**
- 檔案操作（讀取、寫入、搜尋）
- 資料處理（分析、計算）
- 長時間操作期間的狀態更新
- 不需要使用者回覆的確認訊息

❌ **不適合使用並行模式的情境：**
- 需要使用者回答的問題
- 需要使用者核准的確認動作
- 需要使用者確認知悉的錯誤訊息
- 對話結束時的道別（除非正在執行清理工作）

## 情緒語音模式

使用 OpenAI 的 `gpt-4o-mini-tts` 模型搭配 `tts_instructions` 來表達特定的情緒語調。

### 興奮
```python
converse(
    "我們成功了！",
    tts_model="gpt-4o-mini-tts",
    tts_instructions="語氣聽起來非常興奮且帶有慶祝感"
)
```

### 悲傷
```python
converse(
    "對於您的損失，我深感遺憾",
    tts_model="gpt-4o-mini-tts",
    tts_instructions="語氣溫和且帶有同理心"
)
```

### 緊急
```python
converse(
    "當心！",
    tts_model="gpt-4o-mini-tts",
    tts_instructions="語氣聽起來緊急且關切"
)
```

### 幽默
```python
converse(
    "那太搞笑了！",
    tts_model="gpt-4o-mini-tts",
    tts_instructions="語氣聽起來好笑且帶有玩味"
)
```

**備註：** 情緒語音使用 OpenAI API，會產生額外費用（每分鐘約 $0.02 美元）。

## 播速控制模式

根據不同的情境調整語音播放速率。

### 正常速度（預設）
```python
converse("這是正常的播速")
```

### 較快播速（快速狀態更新）
```python
converse("這是較快的播速", speed=1.5)
```

### 雙倍速（非常快速）
```python
converse("這是雙倍速的播速", speed=2.0)
```

### 較慢播速（強調或提升清晰度）
```python
converse("這是較慢的播速", speed=0.8)
```

**備註：** OpenAI 與 Kokoro 提供者均支援此功能。

## VAD 嚴格度模式

根據環境噪音調整語音活動偵測 (VAD) 的嚴格度。

### 安靜房間 - 捕獲所有輕聲說話
```python
converse("讓我們開始對話吧", vad_aggressiveness=0)
```

### 一般居家/辦公室（預設）
```python
converse("跟我說說你今天過得怎麼樣")  # 使用預設值 (2)
```

### 吵雜的咖啡廳/戶外
```python
converse("你聽得見我說話嗎？", vad_aggressiveness=3)
```

### 適合多數情況的平衡設定
```python
converse("你好嗎？", vad_aggressiveness=2)
```

**請記住：**
- 較低的值 (0-1) = 較寬鬆，可能會誤判非人聲的背景音
- 較高的值 (2-3) = 較嚴格，可能會漏掉較輕聲的說話

## 跳過 TTS 模式

使用純文字模式以加快開發與測試迭代的速度。

### 快速迭代模式
```python
converse("正在處理您的請求", skip_tts=True)  # 僅文字顯示，無語音
```

### 重要公告（強制播放語音）
```python
converse("警告：系統即將重新啟動", skip_tts=False)
```

### 快速確認
```python
converse("完成！", skip_tts=True, wait_for_response=False)
```

### 遵循使用者偏好（預設）
```python
converse("你好")  # 使用 VOICEMODE_SKIP_TTS 的環境設定
```

## 多步驟對話模式

處理複雜的多回合互動。

### 提出後續問題
```python
# 第一個問題
response1 = converse("您今天想做些什麼？")
 
# 處理回覆並提出後續問題
if "編輯" in response1.lower() or "edit" in response1.lower():
    response2 = converse("您想要編輯哪一個檔案？")
    # 根據 response2 繼續後續動作
```

### 執行動作前進行確認
```python
converse("我即將刪除所有暫存檔案。這樣可以嗎？")
# 在繼續執行前等待使用者語音確認
```

### 提供進度更新
```python
converse("開始備份程序", wait_for_response=False)
# 執行第一部分備份
converse("已完成百分之五十", wait_for_response=False)
# 執行第二部分備份
converse("備份已完成！", wait_for_response=False)
```

## 錯誤處理模式

清晰地傳達錯誤訊息。

### 簡單錯誤
```python
try:
    # 執行某些操作
    pass
except Exception as e:
    converse(f"我遇到了一個錯誤：{str(e)}。您希望我再試一次嗎？")
```

### 提供替代方案
```python
converse("我找不到那個檔案。您希望我搜尋其他的目錄嗎？")
```

### 請求澄清
```python
converse("我發現了多個同名檔案。您指的是哪一個？")
```

## 另請參閱
- `voicemode-quickstart` - 快速入門範例
- `voicemode-parameters` - 完整參數參考
- `voicemode-troubleshooting` - 常見問題排解
