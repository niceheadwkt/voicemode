# VoiceMode

> 與 Claude Code（以及其他支援 MCP 的 AI 助理）進行自然的語音對話。

[![PyPI Downloads](https://static.pepy.tech/badge/voice-mode)](https://pepy.tech/project/voice-mode)
[![PyPI Downloads](https://static.pepy.tech/badge/voice-mode/month)](https://pepy.tech/project/voice-mode)
[![PyPI Downloads](https://static.pepy.tech/badge/voice-mode/week)](https://pepy.tech/project/voice-mode)

VoiceMode 讓您能與 Claude Code 進行自然的語音對話。語音並非為了解決打字，而是讓您在不方便打字時依然能與 AI 交流。

**非常適合以下情境：**

- 走路去參加下一場會議時
- 一邊做菜一邊進行除錯
- 盯著螢幕數小時後，讓您的眼睛休息一下
- 手上拿著咖啡（或牽著狗）
- 任何雙手或眼睛正忙碌的時刻

## 觀看展示影片

[![VoiceMode Demo](https://img.youtube.com/vi/cYdwOD_-dQc/maxresdefault.jpg)](https://www.youtube.com/watch?v=cYdwOD_-dQc)

## 快速開始

**基本要求：** 配備麥克風與喇叭的電腦

### 選項 1：Claude Code 插件 (推薦)

對 Claude Code 使用者而言最快的入門方式：

```bash
# 新增 VoiceMode 外掛市場
claude plugin marketplace add mbailey/voicemode

# 安裝 VoiceMode 插件
claude plugin install voicemode@voicemode

## 安裝相依套件 (命令列、本地語音服務)

/voicemode:install

# 開始對話！
/voicemode:converse
```

### 選項 2：Python 安裝包

安裝相依套件與 VoiceMode Python 軟體包。

```bash
# 安裝 UV 套件管理器 (如果尚未安裝)
curl -LsSf https://astral.sh/uv/install.sh | sh

# 執行安裝程式 (設定相依套件與本地語音服務)
uvx voice-mode-install

# 新增至 Claude Code
claude mcp add --scope user voicemode -- uvx --refresh --from voice-mode voicemode-mcp-launcher

# 可選：新增 OpenAI API key 作為本地服務的備用機制
export OPENAI_API_KEY=your-openai-key

# 開始對話
claude converse
```

若要手動設定，請參閱 [Getting Started 說明指南](docs/tutorials/getting-started.md)。

## 功能特點

- **自然對話** - 自然地說話，立即聽到回應
- **支援離線** - 可選的本地語音服務 (Whisper STT, Kokoro TTS)
- **低延遲** - 反應迅速，感覺就像真實的對話
- **智慧靜音偵測** - 在您停止說話時自動結束錄音
- **隱私選擇** - 可完全在本地端運行，或使用雲端服務

## 相容性

**支援平台：** Linux, macOS, Windows (原生或 WSL), NixOS
**Python 版本：** 3.10-3.14

## 設定說明

VoiceMode 開箱即用。若要進行自訂：

```bash
# 設定 OpenAI API key (如果使用雲端服務)
export OPENAI_API_KEY="your-key"

# 或者透過檔案進行設定
voicemode config edit
```

請參閱 [Configuration 說明指南](docs/guides/configuration.md) 了解所有設定選項。

## 權限設定 (可選)

若要使用 VoiceMode 且不跳出權限提示，請將以下內容新增至 `~/.claude/settings.json`：

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

請參閱 [Permissions 說明指南](docs/guides/permissions.md) 了解更多選項。

## 本地語音服務

基於隱私或離線使用考量，可以安裝本地語音服務：

- **[Whisper.cpp](docs/guides/whisper-setup.md)** - 本地語音轉文字 (STT)
- **[Kokoro](docs/guides/kokoro-setup.md)** - 本地文字轉語音 (TTS)，擁擁有多種語音選擇

這些服務提供了與 OpenAI 相同的 API 端點，因此 VoiceMode 可以在它們之間無縫切換。

## 安裝細節

<details>
<summary><strong>各平台系統相依套件</strong></summary>

#### Ubuntu/Debian

```bash
sudo apt update
sudo apt install -y ffmpeg gcc libasound2-dev libasound2-plugins libportaudio2 portaudio19-dev pulseaudio pulseaudio-utils python3-dev
```

**WSL2 使用者**：需要安裝上述 pulseaudio 套件以啟用麥克風存取。

#### Fedora/RHEL

```bash
sudo dnf install alsa-lib-devel ffmpeg gcc portaudio portaudio-devel python3-devel
```

#### macOS

```bash
brew install ffmpeg node portaudio
```

#### NixOS

```bash
# 使用開發 Shell
nix develop github:mbailey/voicemode

# 或者進行系統級安裝
nix profile install github:mbailey/voicemode
```

</details>

<details>
<summary><strong>其他安裝方式</strong></summary>

#### 從原始碼安裝

```bash
git clone https://github.com/mbailey/voicemode.git
cd voicemode
uv tool install -e .
```

#### NixOS 系統級安裝

```nix
# 於 /etc/nixos/configuration.nix 中設定
environment.systemPackages = [
  (builtins.getFlake "github:mbailey/voicemode").packages.${pkgs.system}.default
];
```

</details>

## 疑難排解


| 問題 | 解決方案 |
|---------|----------|
| 無法存取麥克風 | 檢查終端機/應用程式權限。WSL2 需要安裝 pulseaudio 套件。 |
| 找不到 UV 命令 | 請執行 `curl -LsSf https://astral.sh/uv/install.sh \| sh` |
| OpenAI API 錯誤 | 驗證 `OPENAI_API_KEY` 是否設定正確 |
| 無音訊輸出 | 檢查系統音訊設定與可用的播放裝置 |


### 儲存音訊以進行偵錯

```bash
export VOICEMODE_SAVE_AUDIO=true
# 檔案會儲存至 ~/.voicemode/audio/YYYY/MM/
```

## 說明文件

- [Getting Started](docs/tutorials/getting-started.md) - 完整設定指南
- [Configuration](docs/guides/configuration.md) - 所有環境變數說明
- [Whisper Setup](docs/guides/whisper-setup.md) - 本地語音轉文字
- [Kokoro Setup](docs/guides/kokoro-setup.md) - 本地文字轉語音
- [Development Setup](docs/tutorials/development-setup.md) - 開發貢獻指南

完整說明文件請參閱：[voicemode.dev](https://voicemode.dev)

## 相關連結

- **官方網站**: [voicemode.dev](https://voicemode.dev)
- **GitHub**: [github.com/mbailey/voicemode](https://github.com/mbailey/voicemode)
- **PyPI**: [pypi.org/project/voice-mode](https://pypi.org/project/voice-mode/)
- **YouTube**: [@getvoicemode](https://youtube.com/@getvoicemode)
- **Twitter/X**: [@getvoicemode](https://twitter.com/getvoicemode)
- **電子報**: [![訂閱](https://img.shields.io/badge/Subscribe-Newsletter-orange?style=flat-square)](https://buttondown.com/voicemode)

## 授權條款

MIT - 屬於 [Failmode](https://failmode.com) 的專案

---
mcp-name: dev.voicemode/voicemode
