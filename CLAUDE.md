# 專案說明

王世儒的個人作品集網站，使用 Python Flask 建立。

## 技術棧

- **後端**：Python Flask（`app.py`）
- **前端**：原生 HTML / CSS / JavaScript（Jinja2 模板，無 React / Vue / Angular）
- **部署**：Railway（`Procfile` + `railway.toml` + gunicorn）

## 本地啟動

```bash
# port 5000 被 macOS AirPlay 佔用，改用 8080
PORT=8080 python app.py
```

## 新增作品集專案

編輯 `app.py` 的 `PROJECTS` 清單，每筆資料需同時填寫 zh / en 雙語欄位：

```python
{
    "id": 4,
    "title": "專案名稱",
    "title_en": "Project Name",
    "subtitle": "副標題",
    "subtitle_en": "Subtitle",
    "tags": ["Python", "Flask"],
    "description": "卡片簡介",
    "description_en": "Card description",
    "details": "模態視窗完整說明",
    "details_en": "Full details for modal",
    "highlights": ["亮點一", "亮點二"],
    "highlights_en": ["Highlight one", "Highlight two"],
    "github": "https://github.com/srwang721tw/repo",
    "demo": "#",          # 填 "#" 代表不顯示按鈕
    "status": "completed", # completed / in-progress / planned
    "year": "2025",
}
```

## 替換頭像

1. 將照片命名為 `avatar.jpg` 放到 `static/img/`
2. 在 `templates/index.html` 中搜尋 `avatar.svg`，將兩處都改為 `avatar.jpg`

## 雙語切換機制

- UI 文字使用 `.zh-only` / `.en-only` CSS class 控制顯示
- JavaScript 在 `<html>` 上切換 `lang-zh` / `lang-en` class
- 語言偏好存入 `localStorage`，重新整理後維持設定
