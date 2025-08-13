#!/usr/bin/env python3
"""
Скрипт для проверки работы деплоя бота
"""

import requests
import sys
import os
from dotenv import load_dotenv

def check_deploy():
    """Проверяет работу деплоя"""
    
    # Загружаем переменные окружения
    load_dotenv()
    
    # Получаем URL из переменной или запрашиваем у пользователя
    webhook_url = os.getenv('WEBHOOK_URL')
    
    if not webhook_url:
        print("🌐 Введите URL вашего приложения (например: https://dimkava-bot.railway.app):")
        webhook_url = input().strip()
        
        if not webhook_url.startswith('http'):
            webhook_url = f"https://{webhook_url}"
    
    print(f"\n🔍 Проверяю деплой: {webhook_url}")
    print("-" * 50)
    
    try:
        # Проверяем главную страницу
        print("1️⃣ Проверяю главную страницу...")
        response = requests.get(webhook_url, timeout=10)
        
        if response.status_code == 200:
            print("✅ Главная страница работает!")
            print(f"   Ответ: {response.text[:100]}...")
        else:
            print(f"❌ Ошибка главной страницы: {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Не удалось подключиться к {webhook_url}")
        print(f"   Ошибка: {e}")
        return False
    
    try:
        # Проверяем вебхук
        print("\n2️⃣ Проверяю вебхук...")
        webhook_response = requests.get(f"{webhook_url}/set_webhook", timeout=10)
        
        if webhook_response.status_code == 200:
            print("✅ Вебхук работает!")
            print(f"   Ответ: {webhook_response.text}")
        else:
            print(f"❌ Ошибка вебхука: {webhook_response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Не удалось проверить вебхук")
        print(f"   Ошибка: {e}")
        return False
    
    print("\n🎉 Все проверки пройдены успешно!")
    print("\n📱 Теперь можете:")
    print("   1. Отправить сообщение боту")
    print("   2. Проверить, что оно сохранилось")
    print("   3. Проверить логи в Railway")
    
    return True

def main():
    """Главная функция"""
    print("🚀 DimKavaTGBot - Проверка деплоя")
    print("=" * 50)
    
    success = check_deploy()
    
    if success:
        print("\n✅ Деплой работает корректно!")
        sys.exit(0)
    else:
        print("\n❌ Проблемы с деплоем!")
        print("   Проверьте логи в Railway и переменные окружения")
        sys.exit(1)

if __name__ == "__main__":
    main()
