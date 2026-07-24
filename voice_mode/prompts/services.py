"""Whisper 和 Kokoro 服務管理提示詞。"""

from voice_mode.server import mcp


@mcp.prompt(name="whisper")
def whisper_prompt(action: str = "status") -> str:
    """管理 Whisper 語音轉文字 (STT) 服務。
    
    Args:
        action: 服務動作 (status, start, stop, restart, enable, disable, logs) 或安裝請求
    """
    valid_actions = ["status", "start", "stop", "restart", "enable", "disable", "logs"]
    
    # 檢查使用者是否想安裝
    install_keywords = ["install", "setup", "configure", "download", "get", "安裝", "設定", "下載", "獲取"]
    if action.lower() in install_keywords or any(keyword in action.lower() for keyword in install_keywords):
        return "使用者想要安裝 Whisper。請使用 whisper_install 工具來安裝 Whisper STT 服務。"
    
    if action not in valid_actions:
        return f"無效的動作 '{action}'。請使用以下之一：{', '.join(valid_actions)}"
    
    return f"請使用 service 工具，並設定 service_name='whisper' 且 action='{action}'"


@mcp.prompt(name="kokoro")
def kokoro_prompt(action: str = "status") -> str:
    """管理 Kokoro 文字轉語音 (TTS) 服務。
    
    Args:
        action: 服務動作 (status, start, stop, restart, enable, disable, logs) 或安裝請求
    """
    valid_actions = ["status", "start", "stop", "restart", "enable", "disable", "logs"]
    
    # 檢查使用者是否想安裝
    install_keywords = ["install", "setup", "configure", "download", "get", "安裝", "設定", "下載", "獲取"]
    if action.lower() in install_keywords or any(keyword in action.lower() for keyword in install_keywords):
        return "使用者想要安裝 Kokoro。請使用 kokoro_install 工具來安裝 Kokoro TTS 服務。"
    
    if action not in valid_actions:
        return f"無效的動作 '{action}'。請使用以下之一：{', '.join(valid_actions)}"
    
    return f"請使用 service 工具，並設定 service_name='kokoro' 且 action='{action}'"