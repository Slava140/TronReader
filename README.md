# TronReader

### Тестовое задание

---

## Установка

1. Клонируйте репозиторий.
   ```bash
   git clone https://github.com/Slava140/TronReader.git
   ```

2. Измените файл `.env.example` и переименуйте в `.env`.

3. Скопируйте файл `.env` в `.env.test` и измените значение переменных `DB_NAME`, `TRONGRID_API_KEY`, `MODE`.

4. Поднимите docker-compose.
   ```bash
   docker-compose up db -d --build
   ```
   - Подключитесь к контейнеру `db`.
     ```bash
     docker exec -it db psql -U postgres
     ```
   - Создайте две базы данных с названиями, которое указали в `DB_NAME` в `.env` и `.env.test`.
     ```sql
     CREATE DATABASE name;
     CREATE DATABASE name_test;
     ```
   - Выйдите из контейнера
     ```bash
     exit
     ```

5. Завершите работу контейнера.
   ```bash
   docker-compose down
   ```

6. Запуск приложения с инфраструктурой.
   ```bash
   docker-compose up --build
    ```
