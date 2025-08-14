#!/usr/bin/env python3
"""
Тестирование endpoint /webhook
"""

import requests
import json

def test_webhook_endpoint():
    """Тестирует endpoint /webhook"""
    print("🔍 Тестирование endpoint /webhook")
    print("=" * 40)
    
    # URL для тестирования
    webhook_url = "https://dimkavatgbot-production.up.railway.app/webhook"
    
    print(f"🔗 Тестируем URL: {webhook_url}")
    print()
    
    # Тест 1: GET запрос (должен вернуть 405 Method Not Allowed)
    print("1️⃣ Тест GET запроса:")
    try:
        response = requests.get(webhook_url, timeout=10)
        print(f"   Статус: {response.status_code}")
        print(f"   Ответ: {response.text[:200]}...")
        
        if response.status_code == 405:
            print("   ✅ Правильно - GET не разрешен (ожидаемо)")
        else:
            print("   ⚠️ Неожиданный статус")
            
    except Exception as e:
        print(f"   ❌ Ошибка: {e}")
    
    print()
    
    # Тест 2: POST запрос с пустыми данными
    print("2️⃣ Тест POST запроса с пустыми данными:")
    try:
        response = requests.post(webhook_url, json={}, timeout=10)
        print(f"   Статус: {response.status_code}")
        print(f"   Ответ: {response.text[:200]}...")
        
        if response.status_code == 200:
            print("   ✅ Endpoint отвечает")
        else:
            print("   ⚠️ Неожиданный статус")
            
    except Exception as e:
        print(f"   ❌ Ошибка: {e}")
    
    print()
    
    # Тест 3: POST запрос с тестовыми данными Telegram
    print("3️⃣ Тест POST запроса с тестовыми данными Telegram:")
    test_data = {
        "update_id": 123456789,
        "message": {
            "message_id": 1,
            "from": {
                "id": 123456789,
                "first_name": "Test",
                "username": "testuser"
            },
            "chat": {
                "id": 123456789,
                "type": "private"
            },
            "date": 1234567890,
            "text": "/start"
        }
    }
    
    try:
        response = requests.post(webhook_url, json=test_data, timeout=10)
        print(f"   Статус: {response.status_code}")
        print(f"   Ответ: {response.text[:200]}...")
        
        if response.status_code == 200:
            print("   ✅ Endpoint обрабатывает данные Telegram")
        else:
            print("   ⚠️ Неожиданный статус")
            
    except Exception as e:
        print(f"   ❌ Ошибка: {e}")
    
    print()
    print("🔍 Диагностика завершена")

if __name__ == "__main__":
    test_webhook_endpoint()
