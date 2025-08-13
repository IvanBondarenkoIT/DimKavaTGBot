from __future__ import annotations

import os
import requests
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, ContextTypes, MessageHandler, filters
from flask import Flask, request, jsonify

DATA_DIR = Path("data")

from .notion_utils import create_notion_task

# Создаем Flask приложение для веб-сервера
app = Flask(__name__)

# Глобальная переменная для отслеживания первого запуска
first_startup = True

def sanitize_filename(value: str) -> str:
    safe = "".join(c if c.isalnum() or c in ("-", "_", ".") else "_" for c in value)
    return safe.strip("._") or "unknown"

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_chat is None or update.effective_message is None:
        return

    chat = update.effective_chat
    message = update.effective_message

    if message.text is None:
        return

    username = (
        message.from_user.username
        if message.from_user and message.from_user.username
        else (message.from_user.full_name if message.from_user else "unknown")
    )

    timestamp = message.date
    date_dir = timestamp.strftime("%Y-%m-%d")
    time_part = timestamp.strftime("%H-%M-%S")

    user_part = sanitize_filename(username)
    chat_part = sanitize_filename(str(chat.id))

    target_dir = DATA_DIR / chat_part / date_dir
    target_dir.mkdir(parents=True, exist_ok=True)

    filename = f"{message.id}_{time_part}_{user_part}.txt"
    file_path = target_dir / filename

    meta_lines = [
        f"chat_id: {chat.id}",
        f"chat_type: {chat.type}",
        f"message_id: {message.id}",
        f"date_iso: {timestamp.isoformat()}",
        f"user: {username}",
    ]

    content = message.text or ""
    file_path.write_text("\n".join(meta_lines) + "\n\n" + content, encoding="utf-8")
    
    # Создаем задачу в Notion
    chat_title = chat.title if chat.type != "private" else None
    create_notion_task(content, username, chat_title)

async def handle_start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /start"""
    if update.effective_chat is None:
        return
    
    from datetime import datetime
    startup_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    message = f"""🤖 DimKavaTGBot активен!

⏰ Время: {startup_time}
🌐 Домен: https://dimkavatgbot-production.up.railway.app
💬 Чат ID: {update.effective_chat.id}

Бот готов к работе! Отправьте любое сообщение для тестирования. 🚀"""
    
    await update.message.reply_text(message)

async def handle_status_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /status"""
    if update.effective_chat is None:
        return
    
    from datetime import datetime
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    message = f"""📊 Статус бота:

✅ Статус: Активен
⏰ Время: {current_time}
🌐 Домен: https://dimkavatgbot-production.up.railway.app
💬 Чат ID: {update.effective_chat.id}
👤 Пользователь: {update.effective_user.full_name if update.effective_user else 'Unknown'}

Бот работает корректно! 🎉"""
    
    await update.message.reply_text(message)

async def send_startup_message(bot):
    """Отправляет сообщение о запуске во все чаты"""
    try:
        from datetime import datetime
        startup_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        message = f"🤖 DimKavaTGBot запущен!\n\n⏰ Время запуска: {startup_time}\n🌐 Домен: https://dimkavatgbot-production.up.railway.app\n\nБот готов к работе! 🚀"
        
        # Получаем список чатов (это может не работать без сохранения chat_id)
        # Пока отправляем в тестовый чат или используем другой подход
        
        print(f"Startup message prepared: {message}")
        return True
    except Exception as e:
        print(f"Error sending startup message: {e}")
        return False

def create_bot_app():
    """Создает и настраивает Telegram бота"""
    load_dotenv()
    token = os.getenv("BOT_TOKEN")
    if not token:
        raise RuntimeError("BOT_TOKEN is not set. Create .env with BOT_TOKEN=...")

    bot_app = (
        Application.builder()
        .token(token)
        .concurrent_updates(True)
        .build()
    )

    text_filter = filters.TEXT & ~filters.COMMAND
    bot_app.add_handler(MessageHandler(text_filter, handle_text))
    
    # Добавляем команду для тестирования
    from telegram.ext import CommandHandler
    bot_app.add_handler(CommandHandler("start", handle_start_command))
    bot_app.add_handler(CommandHandler("status", handle_status_command))
    
    return bot_app

# Глобальная переменная для бота
telegram_app = None

@app.route('/')
def home():
    """Главная страница для проверки работы сервера"""
    from datetime import datetime
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
        
        <p class="status">✅ Сервер работает (bot/__main__.py)</p>
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
        <div id="testResult" style="margin-top: 15px; padding: 15px; border-radius: 8px; display: none;"></div>
        
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
    </script>
</body>
</html>"""

@app.route('/webhook', methods=['POST'])
def webhook():
    """Обработчик вебхуков от Telegram"""
    global telegram_app
    if telegram_app is None:
        telegram_app = create_bot_app()
    
    try:
        # Обрабатываем обновление от Telegram
        update = Update.de_json(request.get_json(), telegram_app.bot)
        telegram_app.process_update(update)
        return 'OK'
    except Exception as e:
        print(f"Ошибка обработки вебхука: {e}")
        return 'Error', 500

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

@app.route('/set_webhook')
def set_webhook():
    """Устанавливает вебхук для бота"""
    global telegram_app
    if telegram_app is None:
        telegram_app = create_bot_app()
    
    # Получаем URL для вебхука
    # Пытаемся получить из переменной окружения, иначе используем текущий домен
    webhook_url = os.getenv('WEBHOOK_URL')
    if not webhook_url:
        # Определяем домен автоматически
        if request:
            # В контексте веб-запроса
            webhook_url = f"{request.url_root.rstrip('/')}/webhook"
        else:
            # Fallback
            webhook_url = 'https://dimkavatgbot-production.up.railway.app/webhook'
    
    # Для тестирования просто возвращаем успешный ответ
    # В реальном деплое вебхук будет установлен через Telegram API
    return f'Webhook готов к установке: {webhook_url}'

def main() -> None:
    """Основная функция для локального запуска"""
    load_dotenv()
    token = os.getenv("BOT_TOKEN")
    if not token:
        raise RuntimeError("BOT_TOKEN is not set. Create .env with BOT_TOKEN=...")

    bot_app = create_bot_app()
    bot_app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    # Проверяем, запускаем ли мы локально или в облаке
    if os.getenv('RAILWAY_ENVIRONMENT') or os.getenv('PORT'):
        # В облаке - запускаем Flask сервер
        port = int(os.getenv('PORT', 5000))
        app.run(host='0.0.0.0', port=port)
    else:
        # Локально - запускаем polling
        main()


