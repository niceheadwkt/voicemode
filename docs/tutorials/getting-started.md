# VoiceMode 使用入門指南 (Getting Started)

VoiceMode 為 AI 程式編碼助理帶來了語音對話功能。它既可作為 Claude Code 的 MCP 伺服器，也可作為獨立的命令列 (CLI) 工具使用。

## 什麼是 VoiceMode？

VoiceMode 提供以下功能：

- **MCP 伺服器**：為 Claude Code 新增語音工具——無需額外安裝其他複雜設定。
- **CLI 工具**：直接從您的終端機使用 VoiceMode 的語音工具。
- **本地服務**：可選的、注重隱私的本地語音處理服務。

## 快速開始：在 Claude Code 中使用

與 Claude Code 搭配使用是開始體驗 VoiceMode 最快的方法。

### 1. 安裝步驟

請先安裝 UV 套件管理器（如果尚未安裝），然後執行 VoiceMode 安裝程式：

```bash
# 安裝 UV 套件管理器 (如果系統中還沒有)
curl -LsSf https://astral.sh/uv/install.sh | sh

# 安裝 VoiceMode 並設定服務
uvx voice-mode-install

# 將其新增至 Claude Code 的 MCP 列表中
claude mcp add --scope user voicemode -- uvx --refresh --from voice-mode voicemode-mcp-launcher
```

安裝程式將會自動：

- 安裝缺失的系統相依套件（如 FFmpeg、PortAudio 等）。
- 為 VoiceMode 設定執行環境。
- 提供安裝本地語音服務的選項（Whisper 語音識別與 Kokoro 語音合成）。

**其他的 UV 安裝方式：**
- **macOS**：`brew install uv`
- **使用 pip**：`pip install uv`

詳情請參閱：[UV 安裝指引](https://docs.astral.sh/uv/getting-started/installation/)

### 2. 設定您的 API 金鑰 (API Key)

將您的 OpenAI API 金鑰設定為環境變數（若使用雲端服務）：

```bash
export OPENAI_API_KEY="您的_OpenAI_API_金鑰"
```

或者將其加入到您的 Shell 設定檔中（如 `~/.bashrc`、`~/.zshrc` 等）。

### 3. 驗證安裝狀態

```bash
# 檢查 VoiceMode 是否已成功連線
claude mcp list
```

您應該會在已連線的伺服器列表中看到 `voicemode`。

### 4. 設定自動核准權限 (可選)

預設情況下，每次使用 VoiceMode 工具時，Claude Code 都會跳出詢問視窗要求授權。若要啟用自動核准，請將以下設定加入至您的 `~/.claude/settings.json` 中：

```json
{
  "permissions": {
    "allow": [
      "mcp__voicemode__converse",
      "mcp__voicemode__service"
    ]
  }
}
```

這能讓您在不被打擾的情況下進行語音對話與管理服務。如需了解更多權限設定，請參閱 [權限指南](../guides/permissions.md)。

### 5. 開始使用語音

在 Claude Code 中，直接輸入：
```
converse
```

聽到提示音（Chime）後即可開始說話，Claude 就會用聲音回覆您！

---

## 替代方案：作為獨立 CLI 工具使用

如果您想直接在命令列中使用 VoiceMode：

### 安裝步驟

```bash
# 使用 pip 安裝
uv tool install voice-mode

# 或者從原始碼以可編輯模式進行安裝
git clone https://github.com/mbailey/voicemode
cd voicemode
uv tool install -e .
```

### 基本用法

```bash
# 設定您的 API 金鑰
export OPENAI_API_KEY="您的_OpenAI_API_金鑰"

# 啟動語音對話
voicemode converse
```

---

## 建立本地語音服務 (可選)

為了維護個人隱私，您可以選擇在本地端運行語音服務，而非將語音傳送至 OpenAI 雲端。

### 快速設定步驟

```bash
# 安裝本地語音服務
voicemode service install whisper   # 語音轉文字 (STT)
voicemode service install kokoro    # 文字轉語音 (TTS)

# 啟動本地服務
voicemode service start whisper
voicemode service start kokoro

# 檢查所有服務的運行狀態
voicemode service status
```

當本地服務可用時，VoiceMode 會自動偵測並優先使用它們。

### 啟用開機/登入自動啟動 (推薦)

若要讓這些語音服務在您登入系統時自動在背景啟動：

```bash
# 啟用自動啟動
voicemode service enable whisper
voicemode service enable kokoro
```

在 macOS 上，這會建立 launchd 守護行程；在 Linux 上，則會建立 systemd 使用者服務。

### 檔案下載大小與系統需求

| 服務 | 下載大小 | 佔用硬碟空間 | 首次啟動耗時 |
|---------|---------------|------------|------------------|
| Whisper (tiny) | ~75MB | ~150MB | 30 秒 |
| Whisper (base) | ~150MB | ~300MB | 1-2 分鐘 |
| Whisper (small) | ~460MB | ~1GB | 2-3 分鐘 |
| Kokoro TTS | ~350MB | ~700MB | 2-3 分鐘 |

**推薦配置**：Whisper base + Kokoro = 共需下載約 500MB，硬碟佔用約 1GB。

### 等待服務啟動

安裝後，服務在首次啟動時需要下載模型。請耐心等待它們準備就緒：

```bash
# 等待 Whisper 服務就緒 (連接埠 2022)
while ! nc -z localhost 2022 2>/dev/null; do sleep 2; done
echo "Whisper 已就緒"

# 等待 Kokoro 服務就緒 (連接埠 8880)
while ! nc -z localhost 8880 2>/dev/null; do sleep 2; done
echo "Kokoro 已就緒"
```

詳細說明請參閱：[Whisper 安裝指南](../guides/whisper-setup.md) | [Kokoro 安裝指南](../guides/kokoro-setup.md)

---

## 自訂設定 (Configuration)

VoiceMode 隨附了合理的預設值。若要自訂偏好：

### 選擇語音聲音 (Voice)

```bash
# OpenAI 提供的語音
export VOICEMODE_VOICES="nova,shimmer"

# 或者使用 Kokoro 本地語音 (若使用本地 TTS)
export VOICEMODE_VOICES="af_sky,am_adam"
```

可用的 OpenAI 語音：alloy, echo, fable, onyx, nova, shimmer

### 專案級特定設定

在您的專案根目錄下建立 `.voicemode.env`：

```bash
export VOICEMODE_VOICES="af_nova,nova"
export VOICEMODE_TTS_SPEED=1.2
```

詳細說明請參閱：[設定指南](../guides/configuration.md)

---

## 疑難排解 (Troubleshooting)

### 語音在 Claude 中無法正常運作？

1. **檢查 MCP 連線狀態**：
   ```bash
   claude mcp list
   ```
   
2. **驗證您的 MCP 設定檔中是否正確設定了 `OPENAI_API_KEY`**。

3. 手動新增環境變數至您的 MCP 設定檔中：
   ```json
   "env": {
     "OPENAI_API_KEY": "sk-...",
   }
   ```

### 麥克風沒有聲音輸入？

```bash
# 列出系統的音訊裝置
voicemode diag devices

# 測試 TTS 與 STT 功能
voicemode converse
```

### 本地服務連線問題？

```bash
# 檢查服務狀態
voicemode service status           # 所有服務
voicemode service status whisper   # 特定服務

# 檢視運行日誌
voicemode service logs whisper -n 50
voicemode service logs kokoro -n 50

# 檢查服務是否有回應（健康度檢查）
voicemode service health whisper
voicemode service health kokoro
```

---

## 以背景服務方式執行 VoiceMode (進階)

若要進行遠端存取或持續運行，您可以將 VoiceMode 作為背景服務啟動：

```bash
# 啟動 VoiceMode HTTP 伺服器
voicemode service start voicemode

# 啟用開機/登入時自動啟動
voicemode service enable voicemode

# 檢查所有服務狀態
voicemode service status
```

啟動 HTTP 伺服器後，您便可從區域網路中的其他裝置或透過安全隧道 (Tunnel) 進行遠端存取。

當需要將服務開放至遠端存取時，請務必參閱 [設定指南中的安全建議](../guides/configuration.md#http-server-security)。

---

## 下一步引言

- **[設定自訂指南](../guides/configuration.md)** - 調整您的 VoiceMode 參數
- **[開發人員設定](development-setup.md)** - 參與 VoiceMode 的開源貢獻
- **[語音服務指南](../guides/)** - 設定本地 Whisper、Kokoro 或 LiveKit 服務
- **[CLI 指令參考](../reference/cli.md)** - 查詢所有可用的命令

## 尋求協助

- **GitHub 錯誤回報**：[github.com/mbailey/voicemode/issues](https://github.com/mbailey/voicemode/issues)
- **Discord**：加入我們的社群取得即時技術支援

歡迎來到語音啟動的 AI 程式開發新時代！ 🎙️
