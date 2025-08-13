#!/usr/bin/env python3
"""
Настройка вебхука для Telegram бота
"""

import os
import requests
from dotenv import load_dotenv

def setup_webhook():
    """Настраивает вебхук для бота"""
    print("🔧 Настройка вебхука для Telegram бота")
    print("=" * 50)
    
    # Загружаем переменные окружения
    load_dotenv()
    
    bot_token = os.getenv('BOT_TOKEN')
    if not bot_token:
        print("❌ BOT_TOKEN не настроен!")
        return False
    
    # URL вебхука
    webhook_url = "https://dimkavatgbot-production.up.railway.app/webhook"
    
    print(f"🤖 Настраиваем вебхук для бота...")
    print(f"🔗 URL вебхука: {webhook_url}")
    print()
    
    # Устанавливаем вебхук
    url = f"https://api.telegram.org/bot{bot_token}/setWebhook"
    data = {
        "url": webhook_url,
        "allowed_updates": ["message", "edited_message", "channel_post", "edited_channel_post"]
    }
    
    try:
        response = requests.post(url, json=data, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            if result.get('ok'):
                print("✅ Вебхук успешно установлен!")
                print(f"📊 Результат: {result}")
                return True
            else:
                print(f"❌ Ошибка установки вебхука: {result}")
                return False
        else:
            print(f"❌ Ошибка HTTP: {response.status_code}")
            print(f"📄 Ответ: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return False

def check_webhook():
    """Проверяет текущий вебхук"""
    print("\n🔍 Проверка текущего вебхука")
    print("=" * 30)
    
    bot_token = os.getenv('BOT_TOKEN')
    if not bot_token:
        print("❌ BOT_TOKEN не настроен!")
        return
    
    url = f"https://api.telegram.org/bot{bot_token}/getWebhookInfo"
    
    try:
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            if result.get('ok'):
                webhook_info = result.get('result', {})
                
                print(f"🔗 URL вебхука: {webhook_info.get('url', 'Не установлен')}")
                print(f"📊 Статус: {'Активен' if webhook_info.get('url') else 'Не установлен'}")
                print(f"📈 Ожидающие обновления: {webhook_info.get('pending_update_count', 0)}")
                print(f"📅 Последняя ошибка: {webhook_info.get('last_error_message', 'Нет ошибок')}")
                
                if webhook_info.get('url'):
                    print("✅ Вебхук настроен корректно!")
                else:
                    print("❌ Вебхук не настроен!")
                    
            else:
                print(f"❌ Ошибка получения информации: {result}")
        else:
            print(f"❌ Ошибка HTTP: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Ошибка: {e}")

def delete_webhook():
    """Удаляет вебхук (для переключения на polling)"""
    print("\n🗑️ Удаление вебхука")
    print("=" * 20)
    
    bot_token = os.getenv('BOT_TOKEN')
    if not bot_token:
        print("❌ BOT_TOKEN не настроен!")
        return
    
    url = f"https://api.telegram.org/bot{bot_token}/deleteWebhook"
    
    try:
        response = requests.post(url, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            if result.get('ok'):
                print("✅ Вебхук удален!")
                print("🔄 Теперь можно использовать polling")
            else:
                print(f"❌ Ошибка удаления: {result}")
        else:
            print(f"❌ Ошибка HTTP: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Ошибка: {e}")

def main():
    """Основная функция"""
    print("🚀 Настройка Telegram бота")
    print("=" * 40)
    
    # Проверяем переменные
    bot_token = os.getenv('BOT_TOKEN')
    if not bot_token:
        print("❌ BOT_TOKEN не настроен!")
        print("Добавьте BOT_TOKEN в переменные окружения")
        return
    
    print(f"🔑 BOT_TOKEN: {bot_token[:10]}...")
    print()
    
    # Проверяем текущий вебхук
    check_webhook()
    
    print("\n" + "=" * 50)
    print("Выберите действие:")
    print("1. Установить вебхук")
    print("2. Удалить вебхук (для polling)")
    print("3. Проверить вебхук")
    print("4. Выход")
    
    choice = input("\nВведите номер (1-4): ").strip()
    
    if choice == "1":
        setup_webhook()
    elif choice == "2":
        delete_webhook()
    elif choice == "3":
        check_webhook()
    elif choice == "4":
        print("👋 До свидания!")
    else:
        print("❌ Неверный выбор")

if __name__ == "__main__":
    main()
