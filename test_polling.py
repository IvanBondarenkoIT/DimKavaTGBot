#!/usr/bin/env python3
"""
Тест режима polling для локального тестирования
"""

import os
import sys
import time

# Устанавливаем тестовые переменные окружения
os.environ['BOT_TOKEN'] = 'test_token'
os.environ['NOTION_TOKEN'] = 'test_token'
os.environ['NOTION_DATABASE_ID'] = 'test_id'

def test_polling_mode():
    """Тестирует режим polling"""
    try:
        print("🔍 Проверяю импорт модулей...")
        
        # Проверяем импорт
        from bot.__main__ import create_bot_app
        
        print("✅ Модули импортируются успешно")
        
        # Проверяем создание приложения
        print("🔧 Создаю приложение бота...")
        bot_app = create_bot_app()
        
        print("✅ Приложение бота создано успешно")
        print(f"   Токен: {bot_app.bot.token[:10]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка тестирования: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Тестирую режим polling...")
    success = test_polling_mode()
    
    if success:
        print("\n✅ Все тесты пройдены! Бот готов к работе.")
        print("\n📱 Для локального запуска используйте:")
        print("   python -m bot")
        sys.exit(0)
    else:
        print("\n❌ Тесты не пройдены. Проверьте код.")
        sys.exit(1)
