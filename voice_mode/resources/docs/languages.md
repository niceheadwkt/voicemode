# 非英語語言支援

## 概述

在說非英語語言時，您**必須**為適當的發音指定 `voice` 與 `tts_provider`。預設的 OpenAI 語音在說非英語時會帶有美式口音。

## 推薦的 Kokoro 中文語音

### 中文 (繁體/國語)
```python
converse("您好，今天想做些什麼？", voice="zf_xiaobei", tts_provider="kokoro")
```

## 可用的 Kokoro 語音列表（按語言劃分）

### 中文 (國語/普通話)
- `zf_xiaobei` - 女聲 (推薦)
- `zm_xiaoming` - 男聲

### 英語 (美式)
- `af_sky` - 女聲
- `af_sarah` - 女聲
- `am_adam` - 男聲
- `am_michael` - 男聲

### 西班牙語
- `ef_dora` - 女聲
- `em_marco` - 男聲

### 法語
- `ff_siwis` - 女聲
- `fm_jean` - 男聲

### 義大利語
- `if_sara` - 女聲
- `im_marco` - 男聲

### 日語
- `jf_alpha` - 女聲
- `jm_beta` - 男聲

### 德語
- `gf_lisa` - 女聲
- `gm_hans` - 男聲

### 葡萄牙語 (巴西)
- `bf_maria` - 女聲
- `bm_joao` - 男聲

### 俄語
- `rf_natasha` - 女聲
- `rm_dmitri` - 男聲

### 韓語
- `kf_yuna` - 女聲
- `km_junho` - 男聲

### 印地語
- `hf_priya` - 女聲
- `hm_raj` - 男聲

### 阿拉伯語
- `af_layla` - 女聲
- `am_omar` - 男聲

### 土耳其語
- `tf_ayse` - 女聲
- `tm_mehmet` - 男聲

## 語音命名慣例

Kokoro 語音遵循以下模式：`{language}{gender}_{name}`

- **語言代碼：** 語言的第一個字母
  - `a` = 英語 (American)
  - `e` = 西班牙語 (Español)
  - `f` = 法語 (Français)
  - `i` = 義大利語
  - `z` = 中文 (中文)
  - `j` = 日語
  - `g` = 德語
  - `b` = 葡萄牙語 (Brazilian)
  - `r` = 俄語
  - `k` = 韓語
  - `h` = 印地語
  - `t` = 土耳其語
- **性別代碼：**
  - `f` = 女性 (Female)
  - `m` = 男性 (Male)
