# Kaggle ETL project (Pet-проект)

Отработка написания ETL-запросов с привязкой Docker, PostgreSQL и подробным логгированием.

### Что добавлено:
**1)** Контейнеризация связки Python + PostgreSQL через Docker Compose.

**2)** Переход от CSV к PostgreSQL с использованием SQLAlchemy с контролем типов данных в таблице.

**3)** Настроено логирование всех этапов работы конвейера с вынесением логгера в отдельный модуль.

## Технологический стек
* **Python 3.13 (Pandas, SQLAlchemy, Psycopg2)**
* **Logging**
* **PostgreSQL**
* **Docker & Docker Compose**

## Структура проекта
* `main.py` - основной файл с функциями для организации ETL-процесса.
* `Dockerfile` - конфигурация образа Docker
* `docker-compose.yml` - App + DB
* `logger_config.py` - файл с логикой логгера
* `requirements.txt` - текстовый файл с зависимостями
* `scripts/init.sql` - SQL-файл с прописанными типами данных
