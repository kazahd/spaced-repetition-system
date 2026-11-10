
```markdown
# Spaced Repetition System

Веб-приложение для интервального повторения знаний с использованием алгоритма SM-2 (SuperMemo 2). Позволяет создавать колоды карточек, проходить сессии повторения, отслеживать статистику и управлять пользователями через административную панель.

**Стек:** Python, FastAPI, PostgreSQL, Vue 3, Pinia, Vuetify.

---

## Требования

Перед запуском убедитесь, что на компьютере установлены:

- **Python 3.11+**
- **Node.js** (рекомендуется LTS-версия)
- **PostgreSQL** (запущенный сервер)
- **Git**

---

## Инструкция по запуску

### Шаг 1. Клонировать репозиторий

```bash
git clone https://github.com/твой-ник/spaced-repetition-system.git
cd spaced-repetition-system
```

### Шаг 2. Настроить базу данных

1. Откройте **pgAdmin** (или `psql`) и создайте базу данных:

   ```sql
   CREATE DATABASE spaced_repetition_db;
   ```

2. В папке `backend/` скопируйте файл `.env.example` в `.env`:

   ```cmd
   cd backend
   copy .env.example .env
   ```

3. Откройте `.env` и впишите свой пароль от PostgreSQL:

   ```env
   DATABASE_URL=postgresql://postgres:ВАШ_ПАРОЛЬ@localhost:5432/spaced_repetition_db
   SECRET_KEY=change_me_to_something_secret
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=10080
   ```

   > **Важно:** замените `ВАШ_ПАРОЛЬ` на реальный пароль пользователя `postgres`.

---

### Шаг 3. Установить зависимости бэкенда

```cmd
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

> **Для macOS/Linux:** активация venv выполняется командой `source venv/bin/activate`.

---

### Шаг 4. Установить зависимости фронтенда

Откройте **новый терминал** (не закрывая первый) и выполните:

```cmd
cd frontend
npm install
```

---

## Запуск приложения

### Быстрый запуск (рекомендуется)

После первичной настройки (шаги 1–4) для запуска достаточно:

1. Убедитесь, что **PostgreSQL запущен**.
2. Дважды кликните файл **`start_all.bat`** в корне проекта.
3. Откроются два свёрнутых окна (Backend и Frontend), а браузер автоматически откроет `http://localhost:5173`.

Для остановки — закройте окна **Backend** и **Frontend** или запустите `stop_all.bat`.

---

### Ручной запуск (если `start_all.bat` не работает)

#### 1. Запуск бэкенда (FastAPI)

Откройте терминал и перейдите в папку `backend`:

```cmd
cd backend
venv\Scripts\activate
python -m uvicorn app.main:app --reload
```

**Результат:** сервер запустится на `http://127.0.0.1:8000`.

**Проверка:** откройте в браузере `http://127.0.0.1:8000/docs` — должна открыться документация Swagger.

#### 2. Запуск фронтенда (Vue.js)

Откройте **новый** терминал (бэкенд остаётся запущенным в первом) и перейдите в папку `frontend`:

```cmd
cd frontend
npm run dev
```

**Результат:** фронтенд запустится на `http://localhost:5173`.

**Проверка:** откройте в браузере `http://localhost:5173` — должна открыться страница входа.

---

## Если что-то не работает

| Проблема | Решение |
|----------|---------|
| `uvicorn not found` | Не активирован venv или не установлены зависимости → `venv\Scripts\activate` → `pip install -r requirements.txt` |
| `npm not found` | Node.js не установлен → скачать с [nodejs.org](https://nodejs.org) |
| `ModuleNotFoundError: No module named 'app'` | Не та папка → убедитесь, что вы в `backend/` |
| `pydantic_settings` не найден | `pip install pydantic-settings` |
| `ModuleNotFoundError: No module named 'jose'` | `pip install python-jose[cryptography]` |
| Порт 8000 занят | Остановить процесс или сменить порт: `python -m uvicorn app.main:app --reload --port 8001` |
| CORS ошибка | Проверьте, что бэкенд запущен и в `main.py` есть `allow_origins=["http://localhost:5173"]` |
| Ошибка подключения к БД | Проверьте `.env` (пароль от PostgreSQL) и что сервер БД запущен |
| `password cannot be longer than 72 bytes` | Конфликт `bcrypt`/`passlib` → `pip install bcrypt==4.0.1 passlib==1.7.4` |

---

## Остановка приложения

| Компонент | Действие |
|-----------|----------|
| Бэкенд | `Ctrl + C` в терминале |
| Фронтенд | `Ctrl + C` в терминале |
| Выйти из venv | `deactivate` |
| Все процессы сразу | Запустить `stop_all.bat` |

---

## Структура проекта

```
spaced-repetition-system/
├── backend/              # FastAPI-приложение
│   ├── app/
│   │   ├── api/          # REST API-маршруты
│   │   ├── core/         # Конфигурация и зависимости
│   │   ├── db/           # Подключение к БД
│   │   ├── models/       # SQLAlchemy-модели
│   │   ├── schemas/      # Pydantic-схемы
│   │   ├── services/     # Бизнес-логика (SM-2)
│   │   └── utils/        # Хеширование, JWT
│   ├── requirements.txt
│   └── .env.example
├── frontend/             # Vue 3-приложение
│   ├── src/
│   │   ├── api/          # Axios-клиент
│   │   ├── stores/       # Pinia-хранилища
│   │   ├── views/        # Страницы
│   │   └── router/       # Маршрутизация
│   └── package.json
├── start_all.bat         # Запуск всего приложения
├── stop_all.bat          # Остановка приложения
└── README.md
```

---

## После запуска

Откройте `http://localhost:5173` и зарегистрируйте нового пользователя или войдите под существующей учётной записью.

Для получения прав администратора (роль `ADMIN`) обратитесь к инструкции по настройке или выполните SQL-запрос:

```sql
UPDATE users SET role = 'ADMIN' WHERE username = 'ваш_логин';
```
```

---
