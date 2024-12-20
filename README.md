# Лабораторная работа №4 по "Технологии программирования на Python".

TaskManager — это API для управления задачами, созданное на FastAPI с использованием PostgreSQL в качестве базы данных. Приложение работает асинхронно. В приложении реализована регистрация пользователей, авторизация с использованием JWT токенов и куки, а также возможность создания, получения, обновления и удаления задач.

## Инструкция по установке

Следуйте данной инструкции для локального запуска проекта с использованием Docker.

### Шаг 1. Клонирование репозитория

Сначала клонируйте проект с GitHub:

```bash
git clone https://github.com/pumpsulp/taskAPI
```
```bash
cd taskAPI
```
### Шаг 2. Запуск контейнеров Docker
Запуск приложения FastAPI и сопутствующих сервисов (PostgreSQL, Redis) осуществляется с помощью Docker Compose:
```bash
docker-compose up -d --build
```
Приложение будет доступно по адресу: http://localhost:8000.
Для доступа к документации API (Swagger UI), перейдите на http://localhost:8000/docs. Там же можно ознакомится со всеми эндпоинтами и протестировать их.

Авторизация происходит с использованием JWT-токенов, которые передаются в куки. После успешной авторизации с помощью эндпоинта ```/login```, токен сохраняется в куки и используется для доступа к защищённым эндпоинтам.

### Переменные окружения
Переменные окружения имеют следующий вид:
```python
POSTGRES_USER=user
POSTGRES_PASSWORD=password
POSTGRES_DB='testdatabase'
POSTGRES_PORT=5432
POSTGRES_HOST=db # имя хоста
POSTGRES_SCHEME=postgresql+psycopg2  # sync driver for alembic
POSTGRES_ASYNC_SCHEME=postgresql+asyncpg # async driver

REDIS_URL=redis://redis:6379/0
REDIS_PORT=6379

APP_RATE_LIMIT=100/minute

FASTAPI_CACHE_EXPIRE_SECONDS=120


JWT_SECRET_KEY='TOP_SECRET'
JWT_ALGORITHM ='HS256'
ACCESS_TOKEN_EXPIRE_MINUTES=30
SALT='VERY_SALT_SALT'
```
В переменных окружения находятся переменные для кодирования / декодирования / задания TTL JWT-токена, SALT - для хэширования пароля при регистрации пользователя. 
Данные для инициализации движка PostgreSQL также находятся в переменных окружения, как и данные для создания Redis подключения.

### Redis 
В приложении используется хэширование с использованием **Redis**: при запуске приложения инициализируется FastAPICache с RedisBackend, таким образом в Redis хэшируются результаты некоторых запросов, таких как ```GET /tasks``` для получения списка всех задач и ```GET /tasks/id``` для получения конкретной задачи по id. Задать TTL хэширования результатов запросов можно в переменных окружения.

Также в Redis хранятся экземпляры класса Limiter из модуля SlowAPI, отвечающие за подсчет количества запросов (для всего приложения, т.е. одинаково для каждого эндпоинта). Задать количество запросов в единицу времени можно в переменных окружения.
