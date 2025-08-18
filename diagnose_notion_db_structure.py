#!/usr/bin/env python3
"""
Диагностика структуры базы данных Notion
"""

import os
import requests
from dotenv import load_dotenv

def main():
    """Диагностика структуры базы данных Notion"""
    print("🔍 Диагностика структуры базы данных Notion")
    print("=" * 50)
    
    # Загружаем переменные окружения
    load_dotenv()
    
    notion_token = os.getenv('NOTION_TOKEN')
    database_id = os.getenv('NOTION_DATABASE_ID')
    
    if not notion_token:
        print("❌ NOTION_TOKEN не настроен!")
        return
    
    if not database_id:
        print("❌ NOTION_DATABASE_ID не настроен!")
        return
    
    headers = {
        "Authorization": f"Bearer {notion_token}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }
    
    # Получаем информацию о базе данных
    url = f"https://api.notion.com/v1/databases/{database_id}"
    
    try:
        print(f"🔗 Запрашиваем информацию о базе данных: {database_id}")
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            db_info = response.json()
            print("✅ База данных найдена!")
            print(f"📝 Название: {db_info.get('title', [{}])[0].get('text', {}).get('content', 'Без названия')}")
            print()
            
            # Показываем свойства
            properties = db_info.get('properties', {})
            print("🔧 Свойства базы данных:")
            print("-" * 30)
            
            for prop_name, prop_info in properties.items():
                prop_type = prop_info.get('type', 'unknown')
                print(f"📋 {prop_name} ({prop_type})")
                
                # Показываем дополнительные детали для title
                if prop_type == 'title':
                    print(f"   ✅ Это свойство можно использовать для названия задачи")
                elif prop_type == 'status':
                    print(f"   ✅ Это свойство можно использовать для статуса")
                elif prop_type == 'multi_select':
                    print(f"   ✅ Это свойство можно использовать для тегов")
            
            print()
            print("💡 Рекомендации:")
            
            # Ищем подходящие свойства
            title_props = [name for name, info in properties.items() if info.get('type') == 'title']
            status_props = [name for name, info in properties.items() if info.get('type') == 'status']
            
            if title_props:
                print(f"✅ Используйте '{title_props[0]}' для названия задачи")
            else:
                print("❌ Нет свойства типа 'title' для названия задачи")
                print("   Создайте свойство типа 'Title' в базе данных")
            
            if status_props:
                print(f"✅ Используйте '{status_props[0]}' для статуса")
            else:
                print("ℹ️  Нет свойства типа 'status' (необязательно)")
            
        else:
            print(f"❌ Ошибка доступа к базе данных: {response.status_code}")
            print(f"📄 Ответ: {response.text}")
            
    except Exception as e:
        print(f"❌ Ошибка: {e}")

if __name__ == "__main__":
    main()
