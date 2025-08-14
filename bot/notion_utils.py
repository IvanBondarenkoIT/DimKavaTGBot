"""
Утилиты для работы с Notion API
"""

import os
import requests


def create_notion_task(text: str, username: str, chat_title: str = None) -> bool:
    """Создает задачу в Notion на основе сообщения"""
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
    
    # Создаем свойства для задачи с правильными названиями
    properties = {
        "Task name": {  # Используем "Task name" для названия
            "title": [
                {
                    "text": {
                        "content": title
                    }
                }
            ]
        },
        "Status": {  # Используем "Status" для статуса
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
