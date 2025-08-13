from __future__ import annotations

import os
import requests
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, ContextTypes, MessageHandler, filters
from flask import Flask, request

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
    
    return f"""<html>
<head>
    <title>DimKavaTGBot Status</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; }}
        .status {{ color: green; font-weight: bold; }}
        .time {{ color: blue; }}
        .domain {{ color: purple; }}
    </style>
</head>
<body>
    <h1>🤖 DimKavaTGBot Status</h1>
    <p class="status">✅ Статус: Активен</p>
    <p class="time">⏰ Время: {current_time}</p>
    <p class="domain">🌐 Домен: https://dimkavatgbot-production.up.railway.app</p>
    <hr>
    <h2>📋 Тестирование:</h2>
    <p>1. Отправьте команду <code>/start</code> боту</p>
    <p>2. Отправьте команду <code>/status</code> боту</p>
    <p>3. Отправьте любое текстовое сообщение боту</p>
    <hr>
    <p><strong>Бот готов к работе! 🚀</strong></p>
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


