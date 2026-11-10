@echo off
echo ================================
echo   Запуск Spaced Repetition System
echo ================================

:: Запуск бэкенда в свёрнутом окне
start /min "Backend" cmd /c "cd /d %~dp0backend && call venv\Scripts\activate && python -m uvicorn app.main:app --reload"

:: Пауза, чтобы бэкенд успел стартовать
timeout /t 2 /nobreak >nul

:: Запуск фронтенда в свёрнутом окне
start /min "Frontend" cmd /c "cd /d %~dp0frontend && npm run dev"

:: Пауза и открытие браузера
timeout /t 4 /nobreak >nul
start http://localhost:5173

echo.
echo Всё запущено (окна свёрнуты в панель задач).
echo Для остановки закрой окна "Backend" и "Frontend".
pause