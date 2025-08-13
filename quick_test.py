#!/usr/bin/env python3
"""
Быстрый тест одного сообщения в Notion
Полезно для проверки настроек без запуска полного теста
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

from bot.notion_utils import create_notion_task


def main():
    """Быстрый тест одного сообщения"""
    print("🚀 Быстрый тест Notion интеграции")
    print("=" * 40)
    
    # Загружаем переменные окружения
    load_dotenv()
    
    # Проверяем настройки
    notion_token = os.getenv("NOTION_TOKEN")
    database_id = os.getenv("NOTION_DATABASE_ID")
    
    if not notion_token or not database_id:
        print("❌ Не настроены переменные окружения")
        print("   Проверьте файл .env")
        return
    
    # Тестовое сообщение
    test_message = input("Введите тестовое сообщение (или нажмите Enter для примера): ").strip()
    
    if not test_message:
        test_message = "Тестовое сообщение из быстрого теста 🚀"
    
    username = input("Введите имя пользователя (или нажмите Enter для 'test_user'): ").strip()
    if not username:
        username = "test_user"
    
    chat_title = input("Введите название чата (или нажмите Enter для пропуска): ").strip()
    if not chat_title:
        chat_title = None
    
    print(f"\n📝 Создаем задачу:")
    print(f"   Сообщение: {test_message}")
    print(f"   Пользователь: {username}")
    print(f"   Чат: {chat_title or 'Личное сообщение'}")
    
    # Создаем задачу
    success = create_notion_task(test_message, username, chat_title)
    
    if success:
        print("\n✅ Задача создана успешно!")
        print("   Проверьте вашу базу данных в Notion")
    else:
        print("\n❌ Ошибка при создании задачи")
        print("   Проверьте настройки и попробуйте снова")


if __name__ == "__main__":
    main()
