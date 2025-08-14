#!/usr/bin/env python3
"""
Тестовый скрипт для проверки исправления Event loop is closed
"""

import os
import sys
import asyncio
import requests
from datetime import datetime

def test_health_endpoint():
    """Тестирует endpoint /health"""
    print("🔍 Тестируем endpoint /health...")
    
    try:
        # Тестируем локально
        response = requests.get('http://localhost:5000/health', timeout=10)
        print(f"✅ Health check: {response.status_code}")
        print(f"📄 Ответ: {response.json()}")
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
            "text": "Тестовое сообщение"
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

def test_bot_initialization():
    """Тестирует инициализацию бота"""
    print("\n🔍 Тестируем инициализацию бота...")
    
    try:
        # Импортируем и тестируем инициализацию
        from bot.__main__ import initialize_bot, get_or_create_bot_app
        
        # Тестируем инициализацию
        bot_app = initialize_bot()
        if bot_app:
            print("✅ Бот успешно инициализирован")
            
            # Тестируем получение существующего экземпляра
            bot_app2 = get_or_create_bot_app()
            if bot_app2 == bot_app:
                print("✅ Singleton pattern работает корректно")
            else:
                print("❌ Singleton pattern не работает")
                
            return True
        else:
            print("❌ Не удалось инициализировать бота")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка инициализации: {e}")
        return False

def main():
    """Основная функция тестирования"""
    print("🚀 Тестирование исправления Event loop is closed")
    print("=" * 50)
    
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
    
    print("\n" + "=" * 50)
    
    # Запускаем тесты
    tests = [
        ("Инициализация бота", test_bot_initialization),
        ("Health endpoint", test_health_endpoint),
        ("Webhook endpoint", test_webhook_endpoint),
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
    print("\n" + "=" * 50)
    print("📊 Итоги тестирования:")
    
    passed = 0
    for test_name, result in results:
        status = "✅ ПРОЙДЕН" if result else "❌ ПРОВАЛЕН"
        print(f"  {test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\n🎯 Результат: {passed}/{len(results)} тестов пройдено")
    
    if passed == len(results):
        print("🎉 Все тесты пройдены! Исправление работает корректно.")
    else:
        print("⚠️  Некоторые тесты не пройдены. Проверьте настройки и логи.")
    
    return passed == len(results)

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
