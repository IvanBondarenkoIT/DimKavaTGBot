#!/usr/bin/env python3
"""
Локальное тестирование Notion интеграции
"""

import os
from datetime import datetime
from dotenv import load_dotenv
from bot.notion_utils import create_notion_task

def main():
    """Тестирование Notion интеграции локально"""
    print("🧪 Локальное тестирование Notion интеграции")
    print("=" * 50)
    
    # Загружаем переменные окружения
    load_dotenv()
    
    # Проверяем переменные
    notion_token = os.getenv('NOTION_TOKEN')
    database_id = os.getenv('NOTION_DATABASE_ID')
    
    print(f"🔑 NOTION_TOKEN: {notion_token[:10] if notion_token else 'НЕ НАСТРОЕН'}...")
    print(f"📊 NOTION_DATABASE_ID: {database_id}")
    print()
    
    if not notion_token:
        print("❌ NOTION_TOKEN не настроен!")
        print("Добавьте NOTION_TOKEN в файл .env")
        return
    
    if not database_id:
        print("❌ NOTION_DATABASE_ID не настроен!")
        print("Добавьте NOTION_DATABASE_ID в файл .env")
        return
    
    # Создаем тестовую задачу
    test_text = f"Локальный тест Notion - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    test_username = "Local Test User"
    
    print(f"📝 Создаем тестовую задачу:")
    print(f"   Текст: {test_text}")
    print(f"   Пользователь: {test_username}")
    print()
    
    try:
        # Создаем задачу
        success = create_notion_task(test_text, test_username, "Local Test")
        
        if success:
            print("✅ Задача успешно создана в Notion!")
            print(f"🔗 Откройте базу данных: https://notion.so/{database_id}")
        else:
            print("❌ Не удалось создать задачу в Notion")
            print("Проверьте логи выше для получения дополнительной информации")
            
    except Exception as e:
        print(f"❌ Ошибка при создании задачи: {e}")
        print("Проверьте настройки Notion интеграции")

if __name__ == "__main__":
    main()
