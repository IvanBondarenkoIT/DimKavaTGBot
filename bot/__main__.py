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
    
    return bot_app

# Глобальная переменная для бота
telegram_app = None

@app.route('/')
def home():
    """Главная страница для проверки работы сервера"""
    return "DimKavaTGBot работает! 🚀"

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
    webhook_url = os.getenv('WEBHOOK_URL', 'https://your-app-name.railway.app/webhook')
    
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


