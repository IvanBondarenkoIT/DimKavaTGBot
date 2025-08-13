#!/usr/bin/env python3
"""
Приложение для Railway - диагностика
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
    <title>Railway Bot Test</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; background-color: #f0f8ff; }}
        .container {{ background: white; padding: 30px; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); }}
        .status {{ color: green; font-weight: bold; font-size: 18px; }}
        .error {{ color: red; font-weight: bold; font-size: 16px; }}
        .warning {{ color: orange; font-weight: bold; }}
        .info {{ color: blue; font-size: 16px; }}
        .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 10px; margin-bottom: 20px; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🤖 DimKavaTGBot - Railway Диагностика</h1>
            <p>Проверка переменных окружения и статуса сервера</p>
        </div>
        
        <p class="status">✅ Сервер работает (railway_app.py)</p>
        <p class="info">⏰ Время: {current_time}</p>
        <p class="info">🌐 Домен: https://dimkavatgbot-production.up.railway.app</p>
        
        <hr>
        <h2>🔧 Переменные окружения:</h2>
        <p><strong>BOT_TOKEN:</strong> <span class="{'error' if bot_token == 'НЕ НАСТРОЕН' else 'status'}">{bot_token[:10]}{'...' if len(bot_token) > 10 else ''}</span></p>
        <p><strong>NOTION_TOKEN:</strong> <span class="{'error' if notion_token == 'НЕ НАСТРОЕН' else 'status'}">{notion_token[:10]}{'...' if len(notion_token) > 10 else ''}</span></p>
        <p><strong>NOTION_DATABASE_ID:</strong> <span class="{'error' if notion_db_id == 'НЕ НАСТРОЕН' else 'status'}">{notion_db_id}</span></p>
        
        <hr>
        <h2>📋 Следующие шаги:</h2>
        <p>1. Настройте переменные окружения в Railway</p>
        <p>2. Перезапустите деплой</p>
        <p>3. Протестируйте бота командами /start и /status</p>
        
        <hr>
        <p><strong>🎯 Если переменные НЕ настроены - бот не будет работать!</strong></p>
    </div>
</body>
</html>"""

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    print(f"🚀 Starting Railway diagnostic server on port {port}")
    print(f"📊 Checking environment variables...")
    app.run(host='0.0.0.0', port=port, debug=False)
