#!/usr/bin/env python3
"""
Простая тестовая страница
"""

from flask import Flask
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def home():
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return f"""<html>
<head>
    <title>Test Page</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; background-color: #f0f0f0; }}
        .container {{ background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        .status {{ color: green; font-weight: bold; font-size: 18px; }}
        .time {{ color: blue; font-size: 16px; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🤖 DimKavaTGBot - Test Page</h1>
        <p class="status">✅ Статус: Активен и обновлен!</p>
        <p class="time">⏰ Время: {current_time}</p>
        <p>🌐 Домен: https://dimkavatgbot-production.up.railway.app</p>
        <hr>
        <h2>📋 Тестирование бота:</h2>
        <p>1. Отправьте <code>/start</code> боту</p>
        <p>2. Отправьте <code>/status</code> боту</p>
        <p>3. Отправьте любое сообщение боту</p>
        <hr>
        <p><strong>🎉 Бот готов к работе!</strong></p>
    </div>
</body>
</html>"""

if __name__ == "__main__":
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
