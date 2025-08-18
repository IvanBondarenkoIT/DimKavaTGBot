#!/usr/bin/env python3
"""
Тестирование Notion интеграции с исправленными названиями свойств
"""

import os
import requests
from datetime import datetime

def create_notion_task_fixed(text: str, username: str, chat_title: str = None) -> bool:
    """Создает задачу в Notion с правильными названиями свойств"""
    notion_token = os.getenv("NOTION_TOKEN")
    database_id = os.getenv("NOTION_DATABASE_ID")
    
    if not notion_token or not database_id:
        print("Notion credentials not configured")
        return False
    
    headers = {
        "Authorization": f"Bearer {notion_token}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }
    
    # Определяем заголовок задачи
    title = text[:100] + "..." if len(text) > 100 else text
    
    # Используем правильные названия свойств из базы данных
    properties = {
        "Task name": {  # Используем "Task name" вместо "Name"
            "title": [
                {
                    "text": {
                        "content": title
                    }
                }
            ]
        },
        "Status": {  # Используем "Status"
            "status": {
                "name": "Not started"
            }
        },
        "Task type": {  # Используем "Task type" для тегов
            "multi_select": [
                {"name": "Telegram"},
                {"name": username}
            ]
        }
    }
    
    # Создаем описание с полным текстом
    children = [
        {
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [
                    {
                        "type": "text",
                        "text": {
                            "content": f"Источник: Telegram\nПользователь: {username}\nЧат: {chat_title or 'Личное сообщение'}\n\n{text}"
                        }
                    }
                ]
            }
        }
    ]
    
    data = {
        "parent": {"database_id": database_id},
        "properties": properties,
        "children": children
    }
    
    try:
        response = requests.post(
            "https://api.notion.com/v1/pages",
            headers=headers,
            json=data
        )
        
        if response.status_code == 200:
            print(f"✅ Создана задача в Notion: {title}")
            return True
        else:
            print(f"❌ Ошибка создания задачи: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка при создании задачи: {e}")
        return False

def main():
    """Тестирование с исправленными названиями свойств"""
    print("🧪 Тестирование Notion интеграции (исправленная версия)")
    print("=" * 60)
    
    # Проверяем переменные
    notion_token = os.getenv('NOTION_TOKEN')
    database_id = os.getenv('NOTION_DATABASE_ID')
    
    print(f"🔑 NOTION_TOKEN: {notion_token[:10] if notion_token else 'НЕ НАСТРОЕН'}...")
    print(f"📊 NOTION_DATABASE_ID: {database_id}")
    print()
    
    if not notion_token:
        print("❌ NOTION_TOKEN не настроен!")
        return
    
    if not database_id:
        print("❌ NOTION_DATABASE_ID не настроен!")
        return
    
    # Создаем тестовую задачу
    test_text = f"Исправленный тест Notion - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    test_username = "Fixed Test User"
    
    print(f"📝 Создаем тестовую задачу:")
    print(f"   Текст: {test_text}")
    print(f"   Пользователь: {test_username}")
    print(f"   Свойства: Task name, Status, Task type")
    print()
    
    try:
        # Создаем задачу
        success = create_notion_task_fixed(test_text, test_username, "Fixed Test")
        
        if success:
            print("✅ Задача успешно создана в Notion!")
            print(f"🔗 Откройте базу данных: https://notion.so/{database_id}")
        else:
            print("❌ Не удалось создать задачу в Notion")
            
    except Exception as e:
        print(f"❌ Ошибка при создании задачи: {e}")

if __name__ == "__main__":
    main()
