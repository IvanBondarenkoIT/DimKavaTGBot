# 🚀 Быстрый деплой на Railway (5 минут!)

## ⚡ Экспресс-план:

### 1. Загрузите код в GitHub (2 мин)
```bash
git add .
git commit -m "Ready for Railway deploy"
git push
```

### 2. Создайте проект на Railway (2 мин)
- Перейдите на [railway.app](https://railway.app)
- "New Project" → "Deploy from GitHub repo"
- Выберите ваш репозиторий
- "Deploy Now"

### 3. Настройте переменные (1 мин)
В Railway → Variables добавьте:
```
BOT_TOKEN=ваш_токен_бота
NOTION_TOKEN=ваш_notion_token  
NOTION_DATABASE_ID=id_базы_данных
```

### 4. Активируйте бота
Откройте: `https://ваш-домен.railway.app/set_webhook`

## ✅ Готово! Бот работает в облаке 24/7

**Проверка:** `python check_deploy.py`

---
📖 **Подробная инструкция:** [DEPLOY_RAILWAY.md](DEPLOY_RAILWAY.md)
