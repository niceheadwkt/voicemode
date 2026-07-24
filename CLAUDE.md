# CLAUDE.md

本文件為 Claude Code (claude.ai/code) 在此專案庫中工作時的指導方針。

## 語音互動

載入 `voicemode` 技術技能以支援語音對話：`/voicemode:voicemode`

## 專案概述

VoiceMode 是一個 Python 套件，透過模型上下文協定 (Model Context Protocol, MCP) 為 AI 助理提供語音互動功能。它整合了語音轉文字 (STT) 與文字轉語音 (TTS) 服務，讓 Claude Code 和其他 AI 程式編碼助理能夠進行自然的語音對話。

## 常用指令

### 開發與測試
```bash
# 以開發模式安裝並安裝所有相依套件
make dev-install

# 執行所有單元測試
make test
# 或直接執行：uv run pytest tests/ -v --tb=short

# 執行特定測試
uv run pytest tests/test_voice_mode.py -v

# 清理建置產物
make clean
```

### 建置與發佈
```bash
# 建置 Python 套件
make build-package

# 建置開發版本（自動設定版本號）
make build-dev  

# 測試套件安裝
make test-package

# 發佈工作流（遞增版本號、建立標籤、推送到遠端）——執行前請參閱下方的「版本發佈與變更日誌」
make release
```

### 說明文件
```bash
# 於本地啟動說明文件伺服器：http://localhost:8000
make docs-serve

# 建置說明文件網站
make docs-build

# 檢查說明文件錯誤（嚴格模式）
make docs-check
```

## 版本發佈與變更日誌 (Releases & Changelog)

**變更日誌 (Changelog) 即為版本發佈說明。** 請隨時保持其準確性——它不是在發佈時才撰寫的。

### 版本命名規範 (Versioning)

- 採用語意化版本 (Semantic Versioning)，格式為 `X.Y.Z`。新增回溯相容的新功能 → 遞增次要版本（例如 `8.6.1` → `8.7.0`）；僅修復 Bug → 遞增修訂版本。
- **版本號的唯一事實來源為：`voice_mode/__version__.py`** ——此檔案由發佈指令腳本自動更新。**切勿手動編輯它**（檔案內有註明）。`pyproject.toml` 會透過 `[tool.hatch.version]` 讀取此檔案。
- 發佈腳本還會自動更新 `server.json`、`installer/pyproject.toml` 以及 `.claude-plugin/plugin.json`（插件會加上 `p0` 後綴，例如 `8.7.0p0`）。請勿手動修改這些檔案。

### 變更日誌 (CHANGELOG) 需持續維護

- 格式規範：[Keep a Changelog](https://keepachangelog.com/) —— 在最上方保留一個 `## [Unreleased]` 區段，並分類為 `### Added / Changed / Deprecated / Removed / Fixed`（本專案還包含一個 `### Migration` 子區段）。
- **當 PR 合併時，其面向使用者的變更必須直接寫入 `## [Unreleased]`** ——不要推遲到發佈當天。請參考現有條目的風格，附上任務 ID (`VM-xxxx`) 與 PR 連結。
- 條目內容應寫成**給使用者看的發佈說明**：GitHub Actions 會將該版本的變更日誌內容逐字擷取並發佈為 GitHub Release 的內容，因此它必須具備良好的可讀性並突出新功能。
- 您可以使用 `/changelog` 技術技能 (`claude-code-tools:changelog`) 來協助起草條目，但標題與宣傳字句仍需人工精修，因為這會直接發送給使用者。

### 執行發佈 —— `make release`

```bash
make release        # 系統會提示輸入新版本號，然後執行 scripts/release.py X.Y.Z
```

`scripts/release.py X.Y.Z` 將會**自動執行以下所有步驟** —— 請勿手動操作：

1. 更新上述四個檔案中的版本號。
2. **重寫 CHANGELOG 標頭**：將 `## [Unreleased]` 轉換為新的空白 `## [Unreleased]`，並在下方建立 `## [X.Y.Z] - YYYY-MM-DD` 區段。**因此，切勿手動切割版本標頭或加入日期——這是發佈腳本的工作。** 您在發佈前的唯一職責是確保 *Unreleased* 區段的內容完整且正確。
3. 執行 `git commit -m "chore: bump version to X.Y.Z for all packages"`。
4. 建立附註標籤 (Annotated Tag) `vX.Y.Z`。
5. 執行 `git push origin`（推送**當前分支**）並推送標籤。

常用參數（可直接傳遞給 `scripts/release.py`）：`--current`（顯示目前版本）、`--no-commit`（僅更新檔案不送交）、`--no-push`（提交並建立標籤但不推送）、`--package package|installer`。

### 標籤觸發的後續動作

推送 `v*` 標籤會觸發兩個 GitHub Actions 工作流：

- **`create-release.yml`** —— 透過 `awk` 擷取 CHANGELOG.md 中的 `## [X.Y.Z] - DATE` 區段，並將其發佈為 GitHub Release 的主體內容。**標頭必須完全符合 `## [X.Y.Z] - DATE` 格式**，否則擷取會產生空白說明——這也是交給 `release.py` 寫入的另一個原因。
- **`publish-pypi-and-mcp.yml`** —— 建置並將套件發佈至 PyPI 和 MCP 登錄庫。

監控網址：https://github.com/mbailey/voicemode/actions

### 發佈前檢查清單 (Pre-release checklist)

1. **確保切換至 `master` 分支並先執行 `git pull`。** Mike 會在本地合併 PR (`--no-ff`) 並推送至 master；`release.py` 會推送您當前所在的分支，因此必須從最新的 `master` 建立標籤，否則已合併的工作會被默默排除。
2. 驗證 `## [Unreleased]` 內容完整 —— 每個已合併且面向使用者的 PR 都有記錄，核心功能都有展示。可與 `git log <last-tag>..origin/master` 進行對照。
3. 根據語意化版本規範決定版本號如何遞增。
4. 執行 `make release`，然後觀察 Actions 的執行狀態。

## 架構概述

### 核心組件

1. **MCP 伺服器 (`voice_mode/server.py`)**
   - 基於 FastMCP 的伺服器，透過 stdio 傳輸協定提供語音工具。
   - 自動匯入所有工具 (tools)、提示詞 (prompts) 與資源 (resources)。
   - 負責 FFmpeg 可用性檢查與日誌設定。

2. **工具系統 (`voice_mode/tools/`)**
   - **converse.py**：核心語音對話工具，整合 TTS/STT。
   - **service.py**：整合 Whisper/Kokoro 的服務管理工具。
   - **providers.py**：提供者探索與註冊管理。
   - **devices.py**：音訊裝置偵測與管理。
   - 服務子目錄包含用於安裝/解除安裝 Whisper 與 Kokoro 的工具。
   - 詳細的內部設計請參閱 [工具載入架構說明](docs/reference/tool-loading-architecture.md)。

3. **提供者系統 (`voice_mode/providers.py`)**
   - 動態探索與 OpenAI 相容的 TTS/STT 端點。
   - 支援健康檢查與故障轉移 (failover)。
   - 維護可用語音服務的註冊表。

4. **設定模組 (`voice_mode/config.py`)**
   - 基於環境變數的設定系統，附帶合理的預設值。
   - 支援專案級與使用者級的語音偏好設定檔。
   - 音訊格式設定（支援 PCM、MP3、WAV、FLAC、AAC、Opus）。

5. **資源系統 (`voice_mode/resources/`)**
   - 開放給用戶端存取的 MCP 資源。
   - 包含統計資訊、配置設定、變更日誌與版本資訊。
   - Whisper 模型管理。

### 服務架構

本專案支援多種語音服務後端：
- **OpenAI API**：雲端 TTS/STT（需要 API 金鑰）。
- **Whisper.cpp**：本地語音轉文字服務。
- **Kokoro**：本機文字轉語音服務，擁有多種語音。

服務可以透過 MCP 工具進行安裝與管理，並支援自動服務探索與健康檢查。

### 核心設計模式

1. **OpenAI API 相容性**：所有語音服務皆提供與 OpenAI 相容的端點，便於在不同提供者之間進行無縫切換。
2. **動態工具探索**：工具會從 tools 目錄結構中自動匯入。
3. **故障轉移支援**：根據可用性在不同服務之間自動進行 fallback 切換。
4. **本地麥克風傳輸**：透過 PyAudio 直接擷取音訊以進行語音互動。
5. **音訊格式協議**：針對提供者的支援能力自動驗證音訊格式。

## 開發備忘錄

- 本專案使用 `uv` 進行套件管理（而非直接使用 pip）。
- 需使用 Python 3.10+ 版本。
- 音訊處理需安裝 FFmpeg。
- 專案遵循基於 FastMCP 模式的模組化架構。
- 服務安裝工具會處理平台特定的設定（在 macOS 上為 launchd，在 Linux 上為 systemd）。
- 提供事件日誌與對話日誌以供偵錯使用。
- 在支援的環境下，會使用 WebRTC VAD 進行靜音偵測。

## 測試

- 單元測試：位於 `tests/` —— 執行 `make test`。
- 手動測試：位於 `tests/manual/` —— 需要使用者互動。

## 日誌紀錄

日誌檔案儲存於 `~/.voicemode/` 目錄中：
- `logs/conversations/` —— 語音交談歷史紀錄 (JSONL)
- `logs/events/` —— 運行事件與錯誤紀錄
- `audio/` —— 儲存的 TTS/STT 音訊檔案
- `voicemode.env` —— 使用者設定檔

## VoiceMode 完整套件

這是核心 Python 套件。VoiceMode 是一系列相關專案的組合：

**若要取得所有 VoiceMode 組件的完整概述，請參閱：**
- **[voicemode-meta/COMPONENTS.md](../voicemode-meta/COMPONENTS.md)** —— 完整套件說明文件

快速參考：
- **voicemode**（本專案庫）—— 用於本地語音模式的 Python MCP 伺服器。
- **voicemode-dev** —— 用於 voicemode.dev 的 Cloudflare Workers 後端。
- **voicemode-ios** —— 原生 iOS 應用程式。
- **voicemode-macos** —— 原生 macOS 應用程式。
- **voicemode-meta** —— 專案協調與營運管理。

## 延伸閱讀

- **[skills/voicemode/SKILL.md](skills/voicemode/SKILL.md)** —— 語音互動使用說明與 MCP 工具。
- **[skills/voicemode-connect/SKILL.md](skills/voicemode-connect/SKILL.md)** —— 透過行動/網頁用戶端進行遠端語音連線。
- **[docs/tutorials/getting-started.md](docs/tutorials/getting-started.md)** —— 安裝設定指南。
- **[docs/guides/configuration.md](docs/guides/configuration.md)** —— 設定規格參考。
- **[docs/concepts/architecture.md](docs/concepts/architecture.md)** —— 詳細架構設計。