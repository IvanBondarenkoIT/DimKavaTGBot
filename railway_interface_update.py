#!/usr/bin/env python3
"""
Обновление интерфейса для Railway
"""

import os
from flask import Flask, request, jsonify
from datetime import datetime
import requests

app = Flask(__name__)

@app.route('/')
def home():
    """Обновленный интерфейс для Railway"""
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Проверяем переменные окружения
    bot_token = os.getenv('BOT_TOKEN', 'НЕ НАСТРОЕН')
    notion_token = os.getenv('NOTION_TOKEN', 'НЕ НАСТРОЕН')
    notion_db_id = os.getenv('NOTION_DATABASE_ID', 'НЕ НАСТРОЕН')
    
    return f"""<html>
<head>
    <title>DimKavaTGBot - Обновленный интерфейс</title>
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
            <h1>🤖 DimKavaTGBot - Обновленный интерфейс</h1>
            <p>Проверка переменных окружения и статуса сервера</p>
        </div>
        
        <p class="status">✅ Сервер работает (railway_interface_update.py)</p>
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
        
                 <hr>
         <h2>🧪 Тестирование бота:</h2>
         <button onclick="testBot()" style="background: #4CAF50; color: white; padding: 15px 30px; border: none; border-radius: 8px; font-size: 16px; cursor: pointer; margin: 10px 0;">
             🚀 Тестировать бота
         </button>
         <button onclick="testNotion()" style="background: #2196F3; color: white; padding: 15px 30px; border: none; border-radius: 8px; font-size: 16px; cursor: pointer; margin: 10px 0; margin-left: 10px;">
             📝 Создать тестовый таск в Notion
         </button>
         <div id="testResult" style="margin-top: 15px; padding: 15px; border-radius: 8px; display: none;"></div>
         <div id="notionResult" style="margin-top: 15px; padding: 15px; border-radius: 8px; display: none;"></div>
        
        <hr>
        <h2>📱 Инструкции:</h2>
        <p>1. Нажмите кнопку "Тестировать бота" выше</p>
        <p>2. Отправьте боту команду <code>/start</code></p>
        <p>3. Отправьте боту команду <code>/status</code></p>
        <p>4. Отправьте любое текстовое сообщение боту</p>
    </div>
    
    <script>
         function testBot() {{
         var button = document.querySelector('button');
         var result = document.getElementById('testResult');
         
         button.disabled = true;
         button.textContent = '🔄 Тестируем...';
         result.style.display = 'block';
         result.innerHTML = '<p>🔄 Проверяем подключение к боту...</p>';
         
         fetch('/test_bot')
             .then(response => response.json())
             .then(data => {{
                 if (data.success) {{
                     result.style.backgroundColor = '#d4edda';
                     result.style.color = '#155724';
                     result.style.border = '1px solid #c3e6cb';
                     result.innerHTML = `
                         <h3>✅ Бот работает!</h3>
                         <p><strong>Имя бота:</strong> ${{data.bot_info.result.first_name}}</p>
                         <p><strong>Username:</strong> @${{data.bot_info.result.username}}</p>
                         <p><strong>Статус:</strong> ${{data.status}}</p>
                         <p><strong>Тестовое сообщение:</strong> ${{data.message}}</p>
                     `;
                 }} else {{
                     result.style.backgroundColor = '#f8d7da';
                     result.style.color = '#721c24';
                     result.style.border = '1px solid #f5c6cb';
                     result.innerHTML = `
                         <h3>❌ Ошибка!</h3>
                         <p><strong>Ошибка:</strong> ${{data.error}}</p>
                         ${{data.response ? `<p><strong>Ответ:</strong> ${{data.response}}</p>` : ''}}
                     `;
                 }}
             }})
             .catch(error => {{
                 result.style.backgroundColor = '#f8d7da';
                 result.style.color = '#721c24';
                 result.style.border = '1px solid #f5c6cb';
                 result.innerHTML = `
                     <h3>❌ Ошибка сети!</h3>
                     <p><strong>Ошибка:</strong> ${{error.message}}</p>
                 `;
             }})
             .finally(() => {{
                 button.disabled = false;
                 button.textContent = '🚀 Тестировать бота';
             }});
     }}
     
     function testNotion() {{
         var button = document.querySelector('button[onclick="testNotion()"]');
         var result = document.getElementById('notionResult');
         
         button.disabled = true;
         button.textContent = '🔄 Создаем таск...';
         result.style.display = 'block';
         result.innerHTML = '<p>🔄 Создаем тестовую задачу в Notion...</p>';
         
         fetch('/test_notion')
             .then(response => response.json())
             .then(data => {{
                 if (data.success) {{
                     result.style.backgroundColor = '#d4edda';
                     result.style.color = '#155724';
                     result.style.border = '1px solid #c3e6cb';
                     result.innerHTML = `
                         <h3>✅ Задача создана в Notion!</h3>
                         <p><strong>Название:</strong> ${{data.title}}</p>
                         <p><strong>Пользователь:</strong> ${{data.username}}</p>
                         <p><strong>Статус:</strong> ${{data.status}}</p>
                         <p><strong>Время создания:</strong> ${{data.timestamp}}</p>
                         ${{data.notion_url ? `<p><strong>Ссылка:</strong> <a href="${{data.notion_url}}" target="_blank">Открыть в Notion</a></p>` : ''}}
                     `;
                 }} else {{
                     result.style.backgroundColor = '#f8d7da';
                     result.style.color = '#721c24';
                     result.style.border = '1px solid #f5c6cb';
                     result.innerHTML = `
                         <h3>❌ Ошибка создания задачи!</h3>
                         <p><strong>Ошибка:</strong> ${{data.error}}</p>
                         ${{data.details ? `<p><strong>Детали:</strong> ${{data.details}}</p>` : ''}}
                         <p><strong>Проверьте:</strong></p>
                         <ul>
                             <li>NOTION_TOKEN настроен правильно</li>
                             <li>NOTION_DATABASE_ID указан корректно</li>
                             <li>База данных доступна для записи</li>
                         </ul>
                     `;
                 }}
             }})
             .catch(error => {{
                 result.style.backgroundColor = '#f8d7da';
                 result.style.color = '#721c24';
                 result.style.border = '1px solid #f5c6cb';
                 result.innerHTML = `
                     <h3>❌ Ошибка сети!</h3>
                     <p><strong>Ошибка:</strong> ${{error.message}}</p>
                 `;
             }})
             .finally(() => {{
                 button.disabled = false;
                 button.textContent = '📝 Создать тестовый таск в Notion';
             }});
     }}
    </script>
</body>
</html>"""

@app.route('/test_bot')
def test_bot_endpoint():
    """API endpoint для тестирования бота"""
    try:
        bot_token = os.getenv('BOT_TOKEN')
        if not bot_token:
            return jsonify({'success': False, 'error': 'BOT_TOKEN не настроен'})
        
        # Создаем тестовое сообщение
        test_message = f"Тестовое сообщение от Railway - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        
        # Отправляем сообщение через Telegram API
        url = f"https://api.telegram.org/bot{bot_token}/getMe"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            bot_info = response.json()
            return jsonify({
                'success': True,
                'message': test_message,
                'bot_info': bot_info,
                'status': 'Бот доступен'
            })
        else:
            return jsonify({
                'success': False,
                'error': f'Ошибка подключения к боту: {response.status_code}',
                'response': response.text
            })
            
    except Exception as e:
        return jsonify({'success': False, 'error': f'Ошибка: {str(e)}'})

@app.route('/test_notion')
def test_notion_endpoint():
    """API endpoint для тестирования Notion интеграции"""
    try:
        notion_token = os.getenv('NOTION_TOKEN')
        database_id = os.getenv('NOTION_DATABASE_ID')
        
        if not notion_token:
            return jsonify({
                'success': False, 
                'error': 'NOTION_TOKEN не настроен',
                'details': 'Добавьте NOTION_TOKEN в переменные окружения Railway'
            })
        
        if not database_id:
            return jsonify({
                'success': False, 
                'error': 'NOTION_DATABASE_ID не настроен',
                'details': 'Добавьте NOTION_DATABASE_ID в переменные окружения Railway'
            })
        
        # Создаем тестовую задачу
        test_text = f"Тестовая задача от Railway - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        test_username = "Railway Test User"
        
        # Проверяем подключение к Notion API
        headers = {
            "Authorization": f"Bearer {notion_token}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28"
        }
        
        # Сначала проверяем доступ к базе данных
        db_url = f"https://api.notion.com/v1/databases/{database_id}"
        db_response = requests.get(db_url, headers=headers, timeout=10)
        
        if db_response.status_code != 200:
            return jsonify({
                'success': False,
                'error': f'Ошибка доступа к базе данных: {db_response.status_code}',
                'details': db_response.text
            })
        
        # Создаем тестовую задачу
        from bot.notion_utils import create_notion_task
        success = create_notion_task(test_text, test_username, "Railway Test")
        
        if success:
            return jsonify({
                'success': True,
                'title': test_text,
                'username': test_username,
                'status': 'Задача создана успешно',
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'notion_url': f"https://notion.so/{database_id.replace('-', '')}"
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Не удалось создать задачу в Notion',
                'details': 'Проверьте логи сервера для получения дополнительной информации'
            })
            
    except Exception as e:
        return jsonify({
            'success': False, 
            'error': f'Ошибка: {str(e)}',
            'details': 'Проверьте настройки Notion интеграции'
                 })

@app.route('/webhook', methods=['POST'])
def webhook():
    """Обработчик вебхуков от Telegram"""
    try:
        from telegram import Update
        from bot.__main__ import create_bot_app
        
        # Создаем бота если еще не создан
        if not hasattr(app, 'telegram_app'):
            app.telegram_app = create_bot_app()
        
        # Обрабатываем обновление от Telegram
        update = Update.de_json(request.get_json(), app.telegram_app.bot)
        app.telegram_app.process_update(update)
        return 'OK'
    except Exception as e:
        print(f"Ошибка обработки вебхука: {e}")
        return 'Error', 500

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    print(f"🚀 Starting updated Railway interface on port {port}")
    app.run(host='0.0.0.0', port=port, debug=False)
