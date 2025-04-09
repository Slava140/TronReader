#!/bin/sh

echo "Применение миграции"
alembic upgrade head

echo "Запуск приложения"
python -m uvicorn src.app:app --host $APP_HOST --port $APP_PORT

exec "$@"