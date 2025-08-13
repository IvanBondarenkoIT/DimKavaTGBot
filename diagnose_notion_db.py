#!/usr/bin/env python3
"""
Скрипт для диагностики структуры базы данных Notion
Помогает понять, какие свойства доступны в базе данных
"""

import os
import requests
from dotenv import load_dotenv


def get_database_schema():
    """Получает схему базы данных Notion"""
    load_dotenv()
    
    notion_token = os.getenv("NOTION_TOKEN")
    database_id = os.getenv("NOTION_DATABASE_ID")
    
    if not notion_token or not database_id:
        print("❌ Не настроены переменные окружения NOTION_TOKEN или NOTION_DATABASE_ID")
        return None
    
    headers = {
        "Authorization": f"Bearer {notion_token}",
        "Notion-Version": "2022-06-28"
    }
    
    try:
        response = requests.get(
            f"https://api.notion.com/v1/databases/{database_id}",
            headers=headers
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"❌ Ошибка получения схемы: {response.status_code} - {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Ошибка при получении схемы: {e}")
        return None


def analyze_database_schema():
    """Анализирует схему базы данных и выводит информацию"""
    print("🔍 Диагностика базы данных Notion")
    print("=" * 50)
    
    schema = get_database_schema()
    if not schema:
        return
    
    print(f"📊 База данных: {schema.get('title', [{}])[0].get('text', {}).get('content', 'Без названия')}")
    print(f"🆔 ID: {schema.get('id', 'Неизвестно')}")
    print()
    
    properties = schema.get('properties', {})
    print(f"📋 Доступные свойства ({len(properties)}):")
    print("-" * 50)
    
    title_properties = []
    status_properties = []
    other_properties = []
    
    for prop_name, prop_data in properties.items():
        prop_type = prop_data.get('type', 'unknown')
        
        if prop_type == 'title':
            title_properties.append(prop_name)
        elif prop_type == 'status':
            status_properties.append(prop_name)
        else:
            other_properties.append(prop_name)
        
        print(f"  • {prop_name} ({prop_type})")
        
        # Показываем дополнительные детали для статуса
        if prop_type == 'status':
            options = prop_data.get('status', {}).get('options', [])
            if options:
                option_names = [opt.get('name', '') for opt in options]
                print(f"    Варианты: {', '.join(option_names)}")
    
    print()
    print("🎯 Рекомендации для .env файла:")
    print("-" * 50)
    
    if title_properties:
        print(f"NOTION_TITLE_PROPERTY={title_properties[0]}")
    else:
        print("❌ Нет свойств типа 'title' для заголовка!")
        print("   Создайте свойство типа 'Title' в вашей базе данных")
    
    if status_properties:
        print(f"NOTION_STATUS_PROPERTY={status_properties[0]}")
    else:
        print("NOTION_STATUS_PROPERTY=")
        print("   (опционально, если нет свойства статуса)")
    
    print()
    print("📝 Пример создания задачи:")
    print("-" * 50)
    
    if title_properties:
        title_prop = title_properties[0]
        print(f"properties = {{")
        print(f'    "{title_prop}": {{')
        print(f'        "title": [{{"text": {{"content": "Заголовок задачи"}}}}]')
        print(f'    }}')
        
        if status_properties:
            status_prop = status_properties[0]
            print(f'    "{status_prop}": {{')
            print(f'        "status": {{"name": "Not Started"}}')
            print(f'    }}')
        
        print(f"}}")
    else:
        print("❌ Невозможно создать задачу без свойства типа 'title'")


def test_simple_task_with_schema():
    """Тестирует создание простой задачи с правильной схемой"""
    print("\n🧪 Тест создания задачи с правильной схемой")
    print("=" * 50)
    
    schema = get_database_schema()
    if not schema:
        return
    
    properties = schema.get('properties', {})
    title_properties = [name for name, data in properties.items() if data.get('type') == 'title']
    
    if not title_properties:
        print("❌ Нет свойств типа 'title' для создания задачи")
        return
    
    title_prop = title_properties[0]
    
    # Создаем простую задачу
    notion_token = os.getenv("NOTION_TOKEN")
    database_id = os.getenv("NOTION_DATABASE_ID")
    
    headers = {
        "Authorization": f"Bearer {notion_token}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }
    
    properties_data = {
        title_prop: {
            "title": [
                {
                    "text": {
                        "content": "Тестовая задача из диагностики"
                    }
                }
            ]
        }
    }
    
    data = {
        "parent": {"database_id": database_id},
        "properties": properties_data
    }
    
    try:
        response = requests.post(
            "https://api.notion.com/v1/pages",
            headers=headers,
            json=data
        )
        
        if response.status_code == 200:
            print("✅ Тестовая задача создана успешно!")
            print("   Проверьте вашу базу данных в Notion")
        else:
            print(f"❌ Ошибка создания тестовой задачи: {response.status_code} - {response.text}")
            
    except Exception as e:
        print(f"❌ Ошибка при создании тестовой задачи: {e}")


def main():
    """Основная функция"""
    analyze_database_schema()
    
    # Спрашиваем, хочет ли пользователь протестировать создание задачи
    response = input("\nХотите протестировать создание задачи? (y/N): ")
    if response.lower() == 'y':
        test_simple_task_with_schema()


if __name__ == "__main__":
    main()



