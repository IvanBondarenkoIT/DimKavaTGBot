#!/usr/bin/env python3
"""
Скрипт для тестирования разных вариантов ID базы данных
"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()

notion_token = os.getenv("NOTION_TOKEN")

# Разные варианты ID базы данных
database_ids = [
    "1a575ffaa32f80979917f54cbb6027fb",  # Без дефисов
    "1a575ffa-a32f-8097-9917-f54cbb6027fb",  # С дефисами
    "1a575ffa-a32f-8097-9917-f54cbb6027fb",  # Стандартный формат UUID
]

headers = {
    "Authorization": f"Bearer {notion_token}",
    "Notion-Version": "2022-06-28"
}

print("🔍 Тестирование ID базы данных")
print("=" * 50)

for db_id in database_ids:
    print(f"\n📋 Тестируем ID: {db_id}")
    
    try:
        response = requests.get(
            f"https://api.notion.com/v1/databases/{db_id}",
            headers=headers
        )
        
        if response.status_code == 200:
            data = response.json()
            title = data.get('title', [{}])[0].get('text', {}).get('content', 'Без названия')
            print(f"✅ Успех! База данных: {title}")
            print(f"   Правильный ID: {db_id}")
            break
        else:
            print(f"❌ Ошибка {response.status_code}: {response.text}")
            
    except Exception as e:
        print(f"❌ Исключение: {e}")

print("\n💡 Если ни один ID не работает, проверьте:")
print("   1. Правильность URL базы данных")
print("   2. Добавлена ли интеграция в базу данных")
print("   3. Существует ли база данных")





