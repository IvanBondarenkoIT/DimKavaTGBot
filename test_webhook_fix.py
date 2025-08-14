#!/usr/bin/env python3
"""
Тестовый скрипт для проверки исправления webhook обработки
"""

import os
import sys
import requests
import json
from datetime import datetime

def test_health_endpoint():
    """Тестирует endpoint /health"""
    print("🔍 Тестируем endpoint /health...")
    
    try:
        response = requests.get('http://localhost:5000/health', timeout=10)
        print(f"✅ Health check: {response.status_code}")
        data = response.json()
        print(f"📄 Ответ: {json.dumps(data, indent=2, ensure_ascii=False)}")
        return True
    except requests.exceptions.ConnectionError:
        print("❌ Не удалось подключиться к серверу. Убедитесь, что сервер запущен.")
        return False
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return False

def test_webhook_endpoint():
    """Тестирует endpoint /webhook с тестовыми данными"""
    print("\n🔍 Тестируем endpoint /webhook...")
    
    # Тестовые данные от Telegram
    test_update = {
        "update_id": 123456789,
        "message": {
            "message_id": 1,
            "from": {
                "id": 123456789,
                "is_bot": False,
                "first_name": "Test",
                "username": "testuser"
            },
            "chat": {
                "id": 123456789,
                "first_name": "Test",
                "type": "private"
            },
            "date": int(datetime.now().timestamp()),
            "text": "Тестовое сообщение для проверки webhook"
        }
    }
    
    try:
        response = requests.post(
            'http://localhost:5000/webhook',
            json=test_update,
            timeout=10
        )
        print(f"✅ Webhook test: {response.status_code}")
        print(f"📄 Ответ: {response.text}")
        return True
    except requests.exceptions.ConnectionError:
        print("❌ Не удалось подключиться к серверу.")
        return False
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return False

def test_bot_control_endpoints():
    """Тестирует endpoints управления ботом"""
    print("\n🔍 Тестируем endpoints управления ботом...")
    
    # Тестируем сброс ошибок
    try:
        response = requests.get('http://localhost:5000/reset_errors', timeout=10)
        print(f"✅ Reset errors: {response.status_code}")
        data = response.json()
        print(f"📄 Ответ: {json.dumps(data, indent=2, ensure_ascii=False)}")
    except Exception as e:
        print(f"❌ Ошибка сброса ошибок: {e}")
    
    # Тестируем перезапуск бота
    try:
        response = requests.get('http://localhost:5000/restart_bot', timeout=10)
        print(f"✅ Restart bot: {response.status_code}")
        data = response.json()
        print(f"📄 Ответ: {json.dumps(data, indent=2, ensure_ascii=False)}")
    except Exception as e:
        print(f"❌ Ошибка перезапуска бота: {e}")
    
    return True

def test_multiple_webhooks():
    """Тестирует множественные webhook запросы"""
    print("\n🔍 Тестируем множественные webhook запросы...")
    
    test_messages = [
        "Первое тестовое сообщение",
        "Второе тестовое сообщение", 
        "Третье тестовое сообщение",
        "Четвертое тестовое сообщение",
        "Пятое тестовое сообщение"
    ]
    
    success_count = 0
    
    for i, message in enumerate(test_messages, 1):
        test_update = {
            "update_id": 123456789 + i,
            "message": {
                "message_id": i,
                "from": {
                    "id": 123456789,
                    "is_bot": False,
                    "first_name": "Test",
                    "username": "testuser"
                },
                "chat": {
                    "id": 123456789,
                    "first_name": "Test",
                    "type": "private"
                },
                "date": int(datetime.now().timestamp()),
                "text": message
            }
        }
        
        try:
            response = requests.post(
                'http://localhost:5000/webhook',
                json=test_update,
                timeout=5
            )
            if response.status_code == 200:
                print(f"✅ Webhook {i}: OK")
                success_count += 1
            else:
                print(f"❌ Webhook {i}: {response.status_code}")
        except Exception as e:
            print(f"❌ Webhook {i}: {e}")
    
    print(f"📊 Результат: {success_count}/{len(test_messages)} успешных запросов")
    return success_count == len(test_messages)

def main():
    """Основная функция тестирования"""
    print("🚀 Тестирование исправления webhook обработки")
    print("=" * 60)
    
    # Проверяем переменные окружения
    print("🔧 Проверка переменных окружения:")
    bot_token = os.getenv('BOT_TOKEN')
    notion_token = os.getenv('NOTION_TOKEN')
    notion_db_id = os.getenv('NOTION_DATABASE_ID')
    
    print(f"  BOT_TOKEN: {'✅ Настроен' if bot_token else '❌ Не настроен'}")
    print(f"  NOTION_TOKEN: {'✅ Настроен' if notion_token else '❌ Не настроен'}")
    print(f"  NOTION_DATABASE_ID: {'✅ Настроен' if notion_db_id else '❌ Не настроен'}")
    
    if not bot_token:
        print("\n⚠️  ВНИМАНИЕ: BOT_TOKEN не настроен. Создайте файл .env с BOT_TOKEN=your_token")
        print("   Тесты могут не работать корректно.")
    
    print("\n" + "=" * 60)
    
    # Запускаем тесты
    tests = [
        ("Health endpoint", test_health_endpoint),
        ("Webhook endpoint", test_webhook_endpoint),
        ("Bot control endpoints", test_bot_control_endpoints),
        ("Multiple webhooks", test_multiple_webhooks),
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n🧪 {test_name}:")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ Ошибка в тесте {test_name}: {e}")
            results.append((test_name, False))
    
    # Выводим итоги
    print("\n" + "=" * 60)
    print("📊 Итоги тестирования:")
    
    passed = 0
    for test_name, result in results:
        status = "✅ ПРОЙДЕН" if result else "❌ ПРОВАЛЕН"
        print(f"  {test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\n🎯 Результат: {passed}/{len(results)} тестов пройдено")
    
    if passed == len(results):
        print("🎉 Все тесты пройдены! Webhook исправление работает корректно.")
        print("\n💡 Теперь ваш бот должен:")
        print("  - Обрабатывать webhook'и без ошибок event loop")
        print("  - Автоматически восстанавливаться при ошибках")
        print("  - Предоставлять управление через веб-интерфейс")
    else:
        print("⚠️  Некоторые тесты не пройдены. Проверьте настройки и логи.")
    
    return passed == len(results)

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

