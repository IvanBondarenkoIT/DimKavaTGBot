#!/usr/bin/env python3
"""
Главный файл для диагностики
"""

import os
from flask import Flask
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def home():
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Проверяем переменные окружения
    bot_token = os.getenv('BOT_TOKEN', 'НЕ НАСТРОЕН')
    notion_token = os.getenv('NOTION_TOKEN', 'НЕ НАСТРОЕН')
    notion_db_id = os.getenv('NOTION_DATABASE_ID', 'НЕ НАСТРОЕН')
    
    return f"""<html>
<head>
    <title>Bot Test</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; background-color: #f5f5f5; }}
        .container {{ background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        .status {{ color: green; font-weight: bold; }}
        .error {{ color: red; font-weight: bold; }}
        .warning {{ color: orange; font-weight: bold; }}
        .info {{ color: blue; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🤖 DimKavaTGBot - Диагностика</h1>
        <p class="status">✅ Сервер работает</p>
        <p class="info">⏰ Время: {current_time}</p>
        <hr>
        <h2>🔧 Переменные окружения:</h2>
        <p><strong>BOT_TOKEN:</strong> <span class="{'error' if bot_token == 'НЕ НАСТРОЕН' else 'status'}">{bot_token[:10]}{'...' if len(bot_token) > 10 else ''}</span></p>
        <p><strong>NOTION_TOKEN:</strong> <span class="{'error' if notion_token == 'НЕ НАСТРОЕН' else 'status'}">{notion_token[:10]}{'...' if len(notion_token) > 10 else ''}</span></p>
        <p><strong>NOTION_DATABASE_ID:</strong> <span class="{'error' if notion_db_id == 'НЕ НАСТРОЕН' else 'status'}">{notion_db_id}</span></p>
        <hr>
        <h2>📋 Что делать:</h2>
        <p>1. Настройте переменные окружения в Railway</p>
        <p>2. Перезапустите деплой</p>
        <p>3. Протестируйте бота</p>
        <hr>
        <p><strong>🌐 Домен: https://dimkavatgbot-production.up.railway.app</strong></p>
    </div>
</body>
</html>"""

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    print(f"Starting diagnostic server on port {port}")
    app.run(host='0.0.0.0', port=port, debug=False)
