# VoiceMode 快速入門

## 基本用法

### 簡單對話
```python
converse("你叫什麼名字？")
```
系統會自動選擇語音與模型。

### 發表聲明並等待回覆
```python
converse("請跟我多說一些關於那件事的細節")
```

### 說話且不等待回覆
```python
converse("再見！", wait_for_response=False)
```

### 使用者要求特定語音
```python
converse("你好", voice="zf_xiaobei")
```
僅在使用者明確要求時才指定語音。

## 常見模式

### 快速確認（不需要回覆）
```python
converse("完成！檔案已儲存", wait_for_response=False)
```

### 提出問題（等待回答）
```python
converse("我應該打開哪一個檔案？")
```

### 工作期間的狀態更新
```python
converse("正在搜尋該檔案", wait_for_response=False)
# 接著立即執行 grep/search 等搜尋工具
```

## 隱私說明
當 `wait_for_response=True` 時，需要麥克風存取權限。音訊透過 STT 服務處理，不會被儲存。

## 另請參閱
- [參數說明](parameters.md) - 完整參數參考
- [對話模式](patterns.md) - 進階對話模式
- [多國語言](languages.md) - 非英語語言支援
- [疑難排解](troubleshooting.md) - 常見問題與解決方案
