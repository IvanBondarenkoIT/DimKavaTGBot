#!/usr/bin/env python3
"""
Скрипт для принудительного обновления Railway деплоя
"""

import os
import time
from datetime import datetime

def main():
    """Принудительное обновление Railway деплоя"""
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    print(f"🔄 Принудительное обновление Railway деплоя - {current_time}")
    print("=" * 60)
    
    # Создаем файл с временной меткой для принудительного обновления
    timestamp_file = f"railway_deployment_{int(time.time())}.txt"
    
    with open(timestamp_file, 'w', encoding='utf-8') as f:
        f.write(f"Railway Deployment Update: {current_time}\n")
        f.write(f"Force Update: {int(time.time())}\n")
        f.write("This file forces Railway to update the deployment\n")
        f.write("Branch: railway-interface-update\n")
        f.write("Status: READY FOR DEPLOYMENT\n")
    
    print(f"✅ Создан файл: {timestamp_file}")
    print("📝 Содержимое файла:")
    
    with open(timestamp_file, 'r', encoding='utf-8') as f:
        print(f.read())
    
    print("\n🚀 Теперь загрузите изменения в GitHub:")
    print("git add .")
    print("git commit -m 'Force Railway deployment update'")
    print("git push")
    
    print("\n⏳ Railway автоматически перезапустит деплой")
    print("🌐 Проверьте: https://dimkavatgbot-production.up.railway.app")
    
    print("\n📋 Если Railway не обновляется:")
    print("1. Перейдите в Railway Dashboard")
    print("2. Найдите проект DimKavaTGBot")
    print("3. В настройках измените ветку на 'railway-interface-update'")
    print("4. Нажмите 'Deploy' → 'Deploy Now'")

if __name__ == "__main__":
    main()
