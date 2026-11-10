@echo off
echo Останавливаю Backend и Frontend...

:: Мягко закрываем окна по заголовку
taskkill /FI "WindowTitle eq Backend*" /T /F >nul 2>&1
taskkill /FI "WindowTitle eq Frontend*" /T /F >nul 2>&1

echo Готово.
pause