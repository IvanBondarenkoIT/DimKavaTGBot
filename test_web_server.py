#!/usr/bin/env python3
"""
Тест веб-сервера для проверки работоспособности
"""

import os
import sys
import threading
import time
import requests

# Устанавливаем тестовые переменные окружения
os.environ['BOT_TOKEN'] = 'test_token'
os.environ['NOTION_TOKEN'] = 'test_token'
os.environ['NOTION_DATABASE_ID'] = 'test_id'

def test_web_server():
    """Тестирует веб-сервер"""
    try:
        # Импортируем приложение
        from app import app
        
        # Запускаем сервер в отдельном потоке
        def run_server():
            app.run(host='127.0.0.1', port=5001, debug=False)
        
        server_thread = threading.Thread(target=run_server, daemon=True)
        server_thread.start()
        
        # Ждем запуска сервера
        time.sleep(3)
        
        # Тестируем главную страницу
        response = requests.get('http://127.0.0.1:5001/', timeout=5)
        if response.status_code == 200:
            print("✅ Главная страница работает!")
            print(f"   Ответ: {response.text}")
        else:
            print(f"❌ Ошибка главной страницы: {response.status_code}")
            return False
        
        # Тестируем вебхук
        response = requests.get('http://127.0.0.1:5001/set_webhook', timeout=5)
        if response.status_code == 200:
            print("✅ Вебхук работает!")
            print(f"   Ответ: {response.text}")
        else:
            print(f"❌ Ошибка вебхука: {response.status_code}")
            return False
        
        print("\n🎉 Веб-сервер работает корректно!")
        return True
        
    except Exception as e:
        print(f"❌ Ошибка тестирования: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Тестирую веб-сервер...")
    success = test_web_server()
    
    if success:
        print("\n✅ Все тесты пройдены! Бот готов к деплою.")
        sys.exit(0)
    else:
        print("\n❌ Тесты не пройдены. Проверьте код.")
        sys.exit(1)
