@echo off
echo ========================================
echo    DimKavaTGBot - Тестирование Notion
echo ========================================
echo.

echo Выберите тип теста:
echo 1. Быстрый тест одного сообщения
echo 2. Полный тест интеграции
echo 3. Массовый импорт (dry-run, 5 файлов)
echo 4. Массовый импорт (реальный, 5 файлов)
echo 5. Выход
echo.

set /p choice="Введите номер (1-5): "

if "%choice%"=="1" (
    echo.
    echo Запуск быстрого теста...
    python quick_test.py
) else if "%choice%"=="2" (
    echo.
    echo Запуск полного теста...
    python test_notion_import.py
) else if "%choice%"=="3" (
    echo.
    echo Запуск массового импорта (dry-run)...
    python import_existing_data.py --dry-run --limit 5
) else if "%choice%"=="4" (
    echo.
    echo Запуск массового импорта (реальный)...
    python import_existing_data.py --limit 5
) else if "%choice%"=="5" (
    echo Выход...
    exit /b 0
) else (
    echo Неверный выбор!
    pause
    goto :eof
)

echo.
echo Тест завершен!
pause

