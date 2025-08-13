#!/usr/bin/env python3
"""
Тестовый скрипт для пробного импорта данных в Notion
Позволяет протестировать интеграцию с Notion без запуска Telegram бота
"""

import os
import sys
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

from bot.notion_utils import create_notion_task


def test_notion_connection():
    """Тестирует подключение к Notion API"""
    print("🔍 Тестирование подключения к Notion...")
    
    notion_token = os.getenv("NOTION_TOKEN")
    database_id = os.getenv("NOTION_DATABASE_ID")
    
    if not notion_token:
        print("❌ NOTION_TOKEN не найден в .env файле")
        return False
    
    if not database_id:
        print("❌ NOTION_DATABASE_ID не найден в .env файле")
        return False
    
    print("✅ Переменные окружения найдены")
    print(f"   Database ID: {database_id[:8]}...")
    print(f"   Token: {notion_token[:10]}...")
    
    return True


def test_simple_task():
    """Тестирует создание простой задачи"""
    print("\n📝 Тест 1: Создание простой задачи")
    
    test_text = "Тестовое сообщение из скрипта"
    username = "test_user"
    
    success = create_notion_task(test_text, username)
    
    if success:
        print("✅ Простая задача создана успешно")
    else:
        print("❌ Ошибка при создании простой задачи")
    
    return success


def test_long_text():
    """Тестирует создание задачи с длинным текстом"""
    print("\n📝 Тест 2: Создание задачи с длинным текстом")
    
    long_text = """
    Это очень длинное сообщение для тестирования обработки больших текстов.
    Оно должно быть обрезано до 100 символов в заголовке задачи.
    
    Дополнительная информация:
    - Пункт 1
    - Пункт 2
    - Пункт 3
    
    Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor 
    incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis 
    nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.
    """
    
    username = "long_text_user"
    
    success = create_notion_task(long_text, username)
    
    if success:
        print("✅ Задача с длинным текстом создана успешно")
    else:
        print("❌ Ошибка при создании задачи с длинным текстом")
    
    return success


def test_special_characters():
    """Тестирует создание задачи с специальными символами"""
    print("\n📝 Тест 3: Создание задачи со специальными символами")
    
    special_text = "Сообщение с эмодзи 🚀 и специальными символами: @#$%^&*()_+{}|:<>?[]\\;'\",./"
    username = "special_chars_user"
    
    success = create_notion_task(special_text, username)
    
    if success:
        print("✅ Задача со специальными символами создана успешно")
    else:
        print("❌ Ошибка при создании задачи со специальными символами")
    
    return success


def test_group_chat():
    """Тестирует создание задачи из группового чата"""
    print("\n📝 Тест 4: Создание задачи из группового чата")
    
    group_text = "Сообщение из группового чата"
    username = "group_user"
    chat_title = "Тестовая группа"
    
    success = create_notion_task(group_text, username, chat_title)
    
    if success:
        print("✅ Задача из группового чата создана успешно")
    else:
        print("❌ Ошибка при создании задачи из группового чата")
    
    return success


def test_multiple_tasks():
    """Тестирует создание нескольких задач подряд"""
    print("\n📝 Тест 5: Создание нескольких задач подряд")
    
    test_messages = [
        ("Первое тестовое сообщение", "user1"),
        ("Второе тестовое сообщение", "user2"),
        ("Третье тестовое сообщение", "user3"),
    ]
    
    success_count = 0
    
    for i, (text, username) in enumerate(test_messages, 1):
        print(f"   Создание задачи {i}/3...")
        if create_notion_task(text, username):
            success_count += 1
    
    print(f"✅ Создано {success_count}/{len(test_messages)} задач")
    return success_count == len(test_messages)


def test_existing_data():
    """Тестирует импорт существующих данных из папки data"""
    print("\n📝 Тест 6: Импорт существующих данных")
    
    data_dir = Path("data")
    if not data_dir.exists():
        print("   Папка data не найдена, пропускаем тест")
        return True
    
    # Находим первый текстовый файл для тестирования
    txt_files = list(data_dir.rglob("*.txt"))
    
    if not txt_files:
        print("   Текстовые файлы не найдены в папке data")
        return True
    
    # Берем первый файл для тестирования
    test_file = txt_files[0]
    print(f"   Тестируем файл: {test_file}")
    
    try:
        content = test_file.read_text(encoding="utf-8")
        
        # Извлекаем метаданные из файла
        lines = content.split('\n')
        meta = {}
        text_content = ""
        
        for line in lines:
            if line.startswith('user: '):
                meta['user'] = line.replace('user: ', '').strip()
            elif line.startswith('chat_id: '):
                meta['chat_id'] = line.replace('chat_id: ', '').strip()
            elif line.startswith('chat_type: '):
                meta['chat_type'] = line.replace('chat_type: ', '').strip()
            elif line and not line.startswith(('chat_id:', 'chat_type:', 'message_id:', 'date_iso:', 'user:')):
                text_content += line + '\n'
        
        text_content = text_content.strip()
        username = meta.get('user', 'unknown_user')
        
        if text_content:
            success = create_notion_task(text_content, username, f"Импорт из {test_file.parent.name}")
            if success:
                print("✅ Существующие данные импортированы успешно")
                return True
            else:
                print("❌ Ошибка при импорте существующих данных")
                return False
        else:
            print("   Файл не содержит текстового контента")
            return True
            
    except Exception as e:
        print(f"   Ошибка при чтении файла: {e}")
        return False


def main():
    """Основная функция тестирования"""
    print("🚀 Запуск тестов импорта в Notion")
    print("=" * 50)
    
    # Загружаем переменные окружения
    load_dotenv()
    
    # Проверяем подключение
    if not test_notion_connection():
        print("\n❌ Тестирование прервано из-за проблем с настройкой")
        return
    
    # Запускаем тесты
    tests = [
        test_simple_task,
        test_long_text,
        test_special_characters,
        test_group_chat,
        test_multiple_tasks,
        test_existing_data,
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ Ошибка в тесте {test.__name__}: {e}")
    
    print("\n" + "=" * 50)
    print(f"📊 Результаты тестирования: {passed}/{total} тестов прошли успешно")
    
    if passed == total:
        print("🎉 Все тесты прошли успешно! Интеграция с Notion работает корректно.")
    else:
        print("⚠️  Некоторые тесты не прошли. Проверьте настройки и попробуйте снова.")


if __name__ == "__main__":
    main()
