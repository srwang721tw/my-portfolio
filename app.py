import os
from flask import Flask, render_template, jsonify, abort, request

app = Flask(__name__)

# ---------------------------------------------------------------------------
# Project data — edit PROJECTS to add / update your portfolio entries.
# Each project supports both zh and en fields for bilingual display.
# ---------------------------------------------------------------------------
PROJECTS = [
    {
        "id": 1,
        "title": "個人作品集網站",
        "title_en": "Personal Portfolio Website",
        "subtitle": "Flask + Vanilla JS 響應式個人網站",
        "subtitle_en": "Flask + Vanilla JS Responsive Personal Site",
        "tags": ["Python", "Flask", "HTML/CSS", "JavaScript"],
        "description": "使用 Flask 框架建立的個人作品集網站，儀表板風格設計，支援中英雙語切換與響應式布局，部署於 Railway。",
        "description_en": "A personal portfolio built with Flask featuring a dashboard layout, bilingual toggle, responsive design, and Railway deployment.",
        "details": "使用 Python Flask 作為後端，搭配原生 HTML、CSS 與 JavaScript，不依賴 React 或 Vue 等重型框架。採用深色冷色系設計，模態視窗取代分頁切換，支援中英雙語切換，並部署在 Railway 上。",
        "details_en": "Built with Python Flask as the backend and vanilla HTML, CSS, and JavaScript — no heavy frameworks. Features a dark cool-tone design, modal-based project viewer (no new tabs), bilingual (zh/en) toggle, and is deployed on Railway.",
        "highlights": [
            "響應式設計 (RWD)，完整支援手機、平板與桌機",
            "儀表板風格，點擊專案以模態視窗展示，無需開啟新分頁",
            "中英雙語一鍵切換，語言偏好存於 localStorage",
            "Flask RESTful API 架構",
            "安全標頭防護（CSP、X-Frame-Options、XSS Filter）",
            "一鍵部署至 Railway",
        ],
        "highlights_en": [
            "Fully responsive (RWD) across mobile, tablet, and desktop",
            "Dashboard-style layout with modal-based project viewer (no new tabs)",
            "One-click bilingual toggle (zh/en) with localStorage preference",
            "Flask RESTful API architecture",
            "Security headers: CSP, X-Frame-Options, XSS Filter",
            "One-click deployment to Railway",
        ],
        "github": "https://github.com/srwang721tw/my-portfolio",
        "demo": "https://srwang721tw.up.railway.app",
        "status": "completed",
        "year": "2025",
    },
    {
        "id": 2,
        "title": "股票投資組合儀表板",
        "title_en": "Portfolio Dashboard",
        "subtitle": "台美股即時追蹤 · Streamlit + Neon PostgreSQL",
        "subtitle_en": "Real-time TW & US stock tracker · Streamlit + Neon PostgreSQL",
        "tags": ["Python", "Streamlit", "PostgreSQL", "yfinance", "Altair"],
        "description": "個人台美股投資組合追蹤工具，支援即時報價、損益計算、質借維持率監控與多使用者帳號隔離，部署於 Railway。",
        "description_en": "Personal TW & US stock portfolio tracker with live prices, P&L calculation, pledge ratio monitoring, and multi-user isolation. Deployed on Railway.",
        "details": "使用 Streamlit 打造的個人投資管理工具，整合 yfinance 即時報價台灣 ETF 與美股，匯率透過國泰網銀爬取並以 yfinance 備援。後端以 Neon PostgreSQL 儲存交易紀錄與每日快照，支援多使用者帳號與資料完全隔離。台股賣出成本以 0.99860 係數調整，呈現實際清算價值。並提供質押維持率四色預警、每日 / 月 / 年損益趨勢圖表（Altair）。",
        "details_en": "A personal investment management app built with Streamlit. Integrates yfinance for live TW ETF and US stock prices, with FX rate scraped from Cathay Bank (yfinance as fallback). Neon PostgreSQL stores transaction records and daily snapshots, with full per-user data isolation. TW holdings apply a sell-cost factor of ×0.99860 for accurate net liquidation values. Features a 4-tier pledge ratio monitor and daily / monthly / annual P&L trend charts (Altair).",
        "highlights": [
            "台美股即時報價，FX 匯率爬取國泰網銀，yfinance 自動備援",
            "台股賣出成本係數（×0.99860）精確呈現實際清算價值",
            "券商 CSV 批次上傳與去重，對帳單自動轉換為持倉",
            "質借維持率監控，分四段色碼預警（紅警 / 橘警 / 黃注意 / 綠安全）",
            "每日 P&L 快照 + 月 / 年趨勢圖表（Altair 深色主題）",
            "PBKDF2-SHA256 密碼驗證，多使用者資料完全隔離",
        ],
        "highlights_en": [
            "Live TW/US stock prices; FX rate scraped from Cathay Bank with yfinance fallback",
            "TW sell-cost factor (×0.99860) for accurate net liquidation values",
            "Multi-file broker CSV upload with deduplication and position aggregation",
            "Pledge maintenance ratio monitor with 4-tier color-coded alerts",
            "Daily P&L snapshots + monthly/annual trend charts (Altair dark theme)",
            "PBKDF2-SHA256 password auth with full per-user data isolation",
        ],
        "github": "https://github.com/srwang721tw/portfolio-dashboard",
        "demo": "#",
        "status": "completed",
        "year": "2025",
    },
    {
        "id": 3,
        "title": "PantryAI 智慧食材庫存管家",
        "title_en": "PantryAI — Smart Pantry Manager",
        "subtitle": "語音 + AI 自然語言輸入，零摩擦管理家庭食材",
        "subtitle_en": "Voice + AI NLP for frictionless home pantry management",
        "tags": ["Python", "Flask", "Gemini API", "PostgreSQL", "Web Speech API"],
        "description": "用語音或自然語言描述食材，Google Gemini AI 自動解析名稱、數量、到期日。支援手機左滑刪除、拖拉排序與深色模式。",
        "description_en": "Describe food items by voice or text; Gemini AI auto-parses name, quantity, and expiry. Features swipe-to-delete, drag-to-reorder, and dark mode.",
        "details": "家庭食材庫存管理 Web App，以語音輸入為核心設計。後端採 Flask + Flask-SQLAlchemy，Neon PostgreSQL 存資料，Render 免費方案部署。AI 解析由 Google Gemini 2.5 Flash 驅動，失敗時自動降級到 jieba + regex 本地方案，確保無 API Key 時仍可使用。支援批次新增（一句話描述多項食材）、到期色碼預警、手機左滑刪除、長按拖拉排序存放地點，以及系統 / 亮 / 暗三段切換的深色模式，多使用者帳號完全隔離。",
        "details_en": "A food pantry web app centered on voice input. Built with Flask + Flask-SQLAlchemy on Neon PostgreSQL, deployed on Render free tier. AI parsing is powered by Google Gemini 2.5 Flash with automatic fallback to a local jieba + regex pipeline, keeping the app functional at zero cost. Features batch item entry (describe multiple items in one sentence), expiry color-coded alerts, mobile swipe-to-delete, drag-to-reorder storage locations, a three-mode dark theme (system / light / dark), and full per-user data isolation.",
        "highlights": [
            "Gemini 2.5 Flash AI 語意解析，失敗自動降級到本地 jieba + regex",
            "瀏覽器原生 Web Speech API 語音輸入，支援 iOS Safari & Chrome",
            "批次新增：一句話描述多項食材，預覽確認後一鍵加入庫存",
            "到期色碼預警（紅 ≤3 天 / 橘 ≤7 天 / 綠安全），左滑刪除 + 長按拖拉排序",
            "暗色模式三段切換（系統 / 亮 / 暗），偏好存於 localStorage",
            "Argon2 密碼雜湊，多使用者資料完全隔離",
        ],
        "highlights_en": [
            "Gemini 2.5 Flash AI NLP with automatic jieba + regex local fallback",
            "Native Web Speech API voice input (iOS Safari & Chrome)",
            "Batch entry: describe multiple items in one sentence, preview then confirm",
            "Color-coded expiry alerts (red ≤3d / orange ≤7d / green), swipe-to-delete, drag-to-reorder",
            "Three-mode dark theme (system / light / dark) stored in localStorage",
            "Argon2 password hashing with full per-user data isolation",
        ],
        "github": "https://github.com/srwang721tw/food-inventory",
        "demo": "https://food-inventory-4ygl.onrender.com",
        "status": "completed",
        "year": "2025",
    },
    {
        "id": 4,
        "title": "政府職缺 LINE 機器人",
        "title_en": "Gov Job LINE Bot",
        "subtitle": "訂閱條件 + 即時爬取台灣政府職缺",
        "subtitle_en": "Subscribe & crawl Taiwan government job listings in real time",
        "tags": ["Python", "FastAPI", "LINE Bot SDK", "BeautifulSoup", "PostgreSQL"],
        "description": "LINE 聊天機器人，設定工作地點與職缺關鍵字後，傳送任何訊息即可即時爬取人事行政總處職缺並回傳結果，輕量無 LLM。",
        "description_en": "A LINE chatbot that scrapes Taiwan DGPA government job listings in real time based on subscribed location and keyword filters — lightweight, no LLM.",
        "details": "整合 LINE Messaging API 的政府職缺訂閱通知機器人。使用者透過 Quick Reply 設定工作地點、人員類別與職缺關鍵字後，傳送任何訊息即可即時爬取人事行政總處（DGPA）網站，取得最近 30 天符合條件的職缺並以手機優化格式回覆。後端以 FastAPI 建構，BeautifulSoup 解析 ASP.NET WebForms 頁面（含 __VIEWSTATE 跨頁 POST），訂閱設定存於 Neon PostgreSQL，本機自動 fallback 到 SQLite，部署於 Render 免費方案。",
        "details_en": "A LINE chatbot for subscribing to Taiwan DGPA government job listings. Users set their work location, personnel category, and job keywords via Quick Reply; any subsequent message triggers a real-time crawl of the DGPA site, returning matching vacancies from the past 30 days in a mobile-optimized format. Built on FastAPI; BeautifulSoup handles ASP.NET WebForms pagination including __VIEWSTATE multi-page POST. Subscriptions stored in Neon PostgreSQL with automatic SQLite fallback for local dev. Deployed on Render free tier.",
        "highlights": [
            "BeautifulSoup 爬取 ASP.NET WebForms 分頁，自動處理 __VIEWSTATE 跨頁 POST",
            "LINE Quick Reply 引導使用者設定地點、人員類別、職缺關鍵字訂閱",
            "任意訊息觸發即時查詢，取得最近 30 天符合條件的職缺",
            "FastAPI 非同步後端，Neon PostgreSQL + SQLite 本地自動降級",
            "無 LLM、零向量搜尋，架構輕量低成本",
        ],
        "highlights_en": [
            "BeautifulSoup scrapes ASP.NET WebForms pages with __VIEWSTATE multi-page POST handling",
            "LINE Quick Reply guides users to set location, category, and keyword subscriptions",
            "Any message triggers real-time crawl of the latest 30-day matching job listings",
            "FastAPI async backend with Neon PostgreSQL and automatic SQLite local fallback",
            "No LLM, no vector search — lightweight and zero ongoing cost",
        ],
        "github": "https://github.com/srwang721tw/gov-job-linebot",
        "demo": "#",
        "status": "in-progress",
        "year": "2025",
    },
]


# ---------------------------------------------------------------------------
# Security headers
# ---------------------------------------------------------------------------
@app.after_request
def add_security_headers(response):
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "SAMEORIGIN"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; "
        "style-src 'self' 'unsafe-inline'; "
        "script-src 'self'; "
        "img-src 'self' data:; "
        "font-src 'self'; "
        "connect-src 'self'"
    )
    return response


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------
@app.route("/")
def index():
    return render_template("index.html", projects=PROJECTS)


@app.route("/api/projects")
def list_projects():
    return jsonify(PROJECTS)


@app.route("/api/projects/<int:project_id>")
def get_project(project_id):
    project = next((p for p in PROJECTS if p["id"] == project_id), None)
    if project is None:
        abort(404)
    return jsonify(project)


@app.errorhandler(404)
def not_found(e):
    if request.path.startswith("/api/"):
        return jsonify({"error": "Not found"}), 404
    return render_template("index.html"), 404


@app.errorhandler(500)
def server_error(e):
    if request.path.startswith("/api/"):
        return jsonify({"error": "Internal server error"}), 500
    return render_template("index.html"), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_DEBUG", "false").lower() == "true"
    app.run(host="0.0.0.0", port=port, debug=debug)
