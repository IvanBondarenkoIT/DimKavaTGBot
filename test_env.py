#!/usr/bin/env python3
"""
Тестовый скрипт для проверки загрузки переменных окружения
"""

import os
from dotenv import load_dotenv

print("🔍 Тестирование загрузки переменных окружения")
print("=" * 50)

# Проверяем текущую директорию
print(f"📁 Текущая директория: {os.getcwd()}")

# Проверяем наличие файла .env
env_file = ".env"
if os.path.exists(env_file):
    print(f"✅ Файл {env_file} найден")
    print(f"   Размер: {os.path.getsize(env_file)} байт")
else:
    print(f"❌ Файл {env_file} не найден")

# Загружаем переменные окружения
print("\n🔄 Загрузка переменных окружения...")
load_dotenv()

# Проверяем переменные
bot_token = os.getenv("BOT_TOKEN")
notion_token = os.getenv("NOTION_TOKEN")
database_id = os.getenv("NOTION_DATABASE_ID")

print(f"\n📋 Результаты загрузки:")
print(f"   BOT_TOKEN: {'✅ Найден' if bot_token else '❌ Не найден'}")
if bot_token:
    print(f"      Значение: {bot_token[:10]}...")

print(f"   NOTION_TOKEN: {'✅ Найден' if notion_token else '❌ Не найден'}")
if notion_token:
    print(f"      Значение: {notion_token[:10]}...")

print(f"   NOTION_DATABASE_ID: {'✅ Найден' if database_id else '❌ Не найден'}")
if database_id:
    print(f"      Значение: {database_id}")

# Проверяем все переменные окружения
print(f"\n🔍 Все переменные окружения:")
for key, value in os.environ.items():
    if key.startswith(('BOT_', 'NOTION_')):
        print(f"   {key}: {value[:20]}{'...' if len(value) > 20 else ''}")



