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
        "description": "使用 Flask 框架建立的個人作品集網站，儀表板風格設計，支援中英雙語切換與響應式布局。",
        "description_en": "A personal portfolio built with Flask featuring a dashboard layout, bilingual support, and full responsive design.",
        "details": "使用 Python Flask 作為後端，搭配原生 HTML、CSS 與 JavaScript，不依賴 React 或 Vue 等重型框架。採用深色冷色系設計，模態視窗取代分頁切換，支援中英雙語切換，並部署在 Railway 上。",
        "details_en": "Built with Python Flask as the backend and vanilla HTML, CSS, and JavaScript — no heavy frameworks. Features a dark cool-tone design, modal-based project viewer (no new tabs), bilingual (zh/en) toggle, and is deployed on Railway.",
        "highlights": [
            "響應式設計 (RWD)，完整支援手機、平板與桌機",
            "儀表板風格，點擊專案以模態視窗展示，無需開啟新分頁",
            "中英雙語一鍵切換",
            "Flask RESTful API 架構",
            "安全標頭防護（CSP、X-Frame-Options、XSS Filter）",
            "一鍵部署至 Railway",
        ],
        "highlights_en": [
            "Fully responsive (RWD) across mobile, tablet, and desktop",
            "Dashboard-style layout with modal-based project viewer",
            "One-click bilingual toggle (Chinese / English)",
            "Flask RESTful API architecture",
            "Security headers: CSP, X-Frame-Options, XSS Filter",
            "One-click deployment to Railway",
        ],
        "github": "https://github.com/srwang721tw/my-portfolio",
        "demo": "#",
        "status": "completed",
        "year": "2025",
    },
    {
        "id": 2,
        "title": "專案名稱",
        "title_en": "Project Name",
        "subtitle": "填入專案副標題或技術棧",
        "subtitle_en": "Add your project subtitle or tech stack",
        "tags": ["Python", "API"],
        "description": "在這裡填入你的專案簡介（約 50–80 字）。",
        "description_en": "Add your project description here (about 50–80 words).",
        "details": "這是預留的作品集模板。在 app.py 中的 PROJECTS 列表新增你的專案資訊。",
        "details_en": "This is a placeholder. Add your project info to the PROJECTS list in app.py.",
        "highlights": ["功能亮點 1", "功能亮點 2", "功能亮點 3"],
        "highlights_en": ["Feature highlight 1", "Feature highlight 2", "Feature highlight 3"],
        "github": "#",
        "demo": "#",
        "status": "in-progress",
        "year": "2025",
    },
    {
        "id": 3,
        "title": "未來專案",
        "title_en": "Future Project",
        "subtitle": "計畫中的下一個作品",
        "subtitle_en": "Next project in planning",
        "tags": ["TBD"],
        "description": "這裡可以放置計畫中但尚未開始的專案。",
        "description_en": "Placeholder for a project that is planned but not yet started.",
        "details": "規劃中的專案，完成後請更新 app.py 中的資料。",
        "details_en": "Project in planning. Update the data in app.py when completed.",
        "highlights": ["待規劃"],
        "highlights_en": ["To be determined"],
        "github": "#",
        "demo": "#",
        "status": "planned",
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
