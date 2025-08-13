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
    
    # Создаем свойства для задачи
    # Используем настраиваемое название свойства или стандартное "Name"
    title_property = os.getenv("NOTION_TITLE_PROPERTY", "Name")
    status_property = os.getenv("NOTION_STATUS_PROPERTY", "Status")
    
    properties = {
        title_property: {
            "title": [
                {
                    "text": {
                        "content": title
                    }
                }
            ]
        }
    }
    
    # Добавляем статус только если он настроен
    if status_property:
        # Получаем правильное название статуса из переменной окружения или используем по умолчанию
        default_status = os.getenv("NOTION_DEFAULT_STATUS", "Not started")
        properties[status_property] = {
            "status": {
                "name": default_status
            }
        }
    
    # Добавляем тег с источником (Telegram)
    if "Tags" in os.getenv("NOTION_DATABASE_PROPERTIES", ""):
        properties["Tags"] = {
            "multi_select": [
                {"name": "Telegram"},
                {"name": username}
            ]
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
