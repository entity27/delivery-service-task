# delivery-service-task
Микросервис "Службы междунарожной доставки". Тестовое задание в компанию «A».

# Структура проекта
- `docker` - файлы для апи, селери и проведения тестов
  - `scripts` - скрипты для использования внутри контейнеров
- `envs` - файлы с переменными окружения
  - `delivery.env.example` - пример для докера
  - `local.delivery.env.example` - пример для локальной разработки
  - `mysql.env.example` - пример для mysql контейнера
- `requirements` - зависимости
  - `requirements.txt` - для обычного контейнера
  - `requirements.test.txt` - для контейнера тестов
- `scripts` - утилиты для разработки
- `src` - исходный код проекта
  - `alembic` - менеджмент миграций
  - `backgrounds` - celery задачи
  - `config` - общая кофигурация проекта
  - `utils` - полезные зависимости
  - `...` - доменные пакеты с моделями, роутами и т.п.
- `tests` - тесты

# Подготовка переменных окружения
- В случае локального запуска
  - Копируем `envs/local.delivery.env.example` -> `envs/local.delivery.env`
- В случае запуска в докере
  - Копируем `envs/delivery.env.example` -> `envs/delivery.env`
- Копируем `envs/mysql.env.example` -> `envs/mysql.env` - переменные для mysql контейнера

# Запуск проекта
## Локально

Через Poetry:
```bash
poetry install
```

Запуск API:
```bash
uvicorn src.main:app --env-file ./envs/local.delivery.env --reload
```

Запуск Celery:
```bash
celery -A src.backgrounds worker -B -l INFO --queues some_task
```

Хук для разработки:
```bash
pre-commit install
```

## Докер
```bash
docker compose up -d
```
