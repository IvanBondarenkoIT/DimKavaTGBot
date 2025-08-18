#!/usr/bin/env python3
"""
Проверка статуса вебхука
"""

import os
import requests

def check_webhook():
    """Проверяет статус вебхука"""
    bot_token = os.getenv('BOT_TOKEN')
    
    if not bot_token:
        print("❌ BOT_TOKEN не настроен!")
        print("Добавьте BOT_TOKEN в переменные окружения")
        return
    
    url = f"https://api.telegram.org/bot{bot_token}/getWebhookInfo"
    
    try:
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            if result.get('ok'):
                webhook_info = result.get('result', {})
                
                print("🔍 Статус вебхука:")
                print(f"🔗 URL: {webhook_info.get('url', 'Не установлен')}")
                print(f"📊 Активен: {'Да' if webhook_info.get('url') else 'Нет'}")
                print(f"📈 Ожидающие обновления: {webhook_info.get('pending_update_count', 0)}")
                print(f"📅 Последняя ошибка: {webhook_info.get('last_error_message', 'Нет ошибок')}")
                
                if webhook_info.get('url'):
                    print("✅ Вебхук настроен и активен!")
                else:
                    print("❌ Вебхук не настроен!")
                    
            else:
                print(f"❌ Ошибка: {result}")
        else:
            print(f"❌ HTTP ошибка: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Ошибка: {e}")

if __name__ == "__main__":
    check_webhook()
