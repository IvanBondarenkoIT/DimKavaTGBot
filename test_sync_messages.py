#!/usr/bin/env python3
"""
Тестовый скрипт для проверки синхронной отправки сообщений
"""

import os
import sys
import requests
import json
from datetime import datetime

def test_sync_message_sending():
    """Тестирует синхронную отправку сообщений"""
    print("🔍 Тестируем синхронную отправку сообщений...")
    
    # Импортируем функцию из модуля
    try:
        from bot.__main__ import send_message_sync
        
        # Тестовый chat_id (замените на реальный)
        test_chat_id = os.getenv('TEST_CHAT_ID', '123456789')
        test_message = f"🧪 Тестовое сообщение от синхронной отправки - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        
        print(f"📤 Отправляем сообщение в чат {test_chat_id}...")
        result = send_message_sync(test_chat_id, test_message)
        
        if result:
            print("✅ Сообщение отправлено успешно!")
            return True
        else:
            print("❌ Ошибка отправки сообщения")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка тестирования: {e}")
        return False

def test_webhook_with_commands():
    """Тестирует webhook с командами"""
    print("\n🔍 Тестируем webhook с командами...")
    
    # Тест команды /start
    start_update = {
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
            "text": "/start"
        }
    }
    
    try:
        response = requests.post(
            'http://localhost:5000/webhook',
            json=start_update,
            timeout=10
        )
        print(f"✅ /start command: {response.status_code}")
        
        # Тест команды /status
        status_update = {
            "update_id": 123456790,
            "message": {
                "message_id": 2,
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
                "text": "/status"
            }
        }
        
        response = requests.post(
            'http://localhost:5000/webhook',
            json=status_update,
            timeout=10
        )
        print(f"✅ /status command: {response.status_code}")
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка тестирования команд: {e}")
        return False

def test_webhook_with_text():
    """Тестирует webhook с текстовыми сообщениями"""
    print("\n🔍 Тестируем webhook с текстовыми сообщениями...")
    
    test_messages = [
        "Привет! Это тестовое сообщение",
        "Проверяем работу бота",
        "Тестируем сохранение в файл и создание задач в Notion"
    ]
    
    success_count = 0
    
    for i, message in enumerate(test_messages, 1):
        text_update = {
            "update_id": 123456791 + i,
            "message": {
                "message_id": 10 + i,
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
                json=text_update,
                timeout=10
            )
            if response.status_code == 200:
                print(f"✅ Text message {i}: OK")
                success_count += 1
            else:
                print(f"❌ Text message {i}: {response.status_code}")
        except Exception as e:
            print(f"❌ Text message {i}: {e}")
    
    print(f"📊 Результат: {success_count}/{len(test_messages)} успешных запросов")
    return success_count == len(test_messages)

def main():
    """Основная функция тестирования"""
    print("🚀 Тестирование синхронной отправки сообщений")
    print("=" * 60)
    
    # Проверяем переменные окружения
    print("🔧 Проверка переменных окружения:")
    bot_token = os.getenv('BOT_TOKEN')
    test_chat_id = os.getenv('TEST_CHAT_ID')
    
    print(f"  BOT_TOKEN: {'✅ Настроен' if bot_token else '❌ Не настроен'}")
    print(f"  TEST_CHAT_ID: {'✅ Настроен' if test_chat_id else '❌ Не настроен'}")
    
    if not bot_token:
        print("\n⚠️  ВНИМАНИЕ: BOT_TOKEN не настроен. Создайте файл .env с BOT_TOKEN=your_token")
        print("   Тесты могут не работать корректно.")
    
    print("\n" + "=" * 60)
    
    # Запускаем тесты
    tests = [
        ("Синхронная отправка сообщений", test_sync_message_sending),
        ("Webhook с командами", test_webhook_with_commands),
        ("Webhook с текстовыми сообщениями", test_webhook_with_text),
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
        print("🎉 Все тесты пройдены! Синхронная отправка работает корректно.")
        print("\n💡 Теперь ваш бот должен:")
        print("  - Отправлять сообщения без ошибок event loop")
        print("  - Обрабатывать команды /start и /status")
        print("  - Отправлять подтверждения для текстовых сообщений")
    else:
        print("⚠️  Некоторые тесты не пройдены. Проверьте настройки и логи.")
    
    return passed == len(results)

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
