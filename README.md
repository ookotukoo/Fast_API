# Roadmap: Изучение FastAPI до уровня Middle

## 1. Основы Python (если нужно освежить)
- Убедитесь, что уверенно владеете:
  - ООП (классы, наследование, методы)
  - Декораторы (`@decorator`)
  - Асинхронность (`async/await`)
  - Типизация (`typing`, `Type Hints`)

## 2. Основы FastAPI

### Шаг 1: Установка и первый проект
```bash
pip install fastapi uvicorn
```
main.py:

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}
```
Запуск:

```bash
uvicorn main:app --reload
```

Откройте http://127.0.0.1:8000/docs (Swagger UI).

### Шаг 2: Роуты и HTTP-методы
@app.get(), @app.post(), @app.put(), @app.delete()

Path-параметры (/items/{item_id})

Query-параметры (/items/?skip=0&limit=10)

Пример:

```python
@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}
```
### Шаг 3: Pydantic и валидация данных
```python
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    price: float

@app.post("/items/")
def create_item(item: Item):
    return item
```
### Шаг 4: Обработка ошибок
```python
from fastapi import HTTPException

@app.get("/items/{item_id}")
def read_item(item_id: int):
    if item_id == 42:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"item_id": item_id}
```
## 3. Углубленное изучение
### Шаг 5: Зависимости (Dependency Injection)
```python
from fastapi import Depends

def common_params(q: str = None, skip: int = 0, limit: int = 100):
    return {"q": q, "skip": skip, "limit": limit}

@app.get("/items/")
def read_items(commons: dict = Depends(common_params)):
    return commons
```
### Шаг 6: Асинхронность и БД (SQLAlchemy + asyncpg)
```python
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql+asyncpg://user:password@localhost/db"
engine = create_async_engine(DATABASE_URL)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession)

async def get_db():
    async with AsyncSessionLocal() as db:
        yield db

@app.get("/users/{user_id}")
async def read_user(user_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalar_one()
```
### Шаг 7: Фоновые задачи (Background Tasks)
```python
from fastapi import BackgroundTasks

def write_log(message: str):
    with open("log.txt", mode="a") as log:
        log.write(message)

@app.post("/send-notification/{email}")
def send_notification(email: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(write_log, f"Notification sent to {email}")
    return {"message": "Notification sent in background"}
```
### Шаг 8: Тестирование (pytest)
```python
from fastapi.testclient import TestClient

client = TestClient(app)

def test_read_item():
    response = client.get("/items/42")
    assert response.status_code == 200
    assert response.json() == {"item_id": 42}
```
### Шаг 9: Аутентификация (OAuth2 + JWT)
```python
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.get("/users/me")
def read_current_user(token: str = Depends(oauth2_scheme)):
    return {"token": token}
```
### Шаг 10: Middleware и CORS
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
```
## 4. Продвинутые темы (Middle Level)
### 1. Оптимизация запросов
Кэширование (redis, fastapi-cache)

Асинхронные запросы (databases)

### 2. WebSockets
```python
from fastapi import WebSocket

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Message: {data}")
```
### 3. OpenAPI кастомизация
Изменение документации Swagger/Redoc

Добавление своих схем

### 4. Docker + Deploy
```Dockerfile
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
```
### 5. Тестирование производительности
Locust / pytest-benchmark

Оптимизация запросов к БД

## 5. Практика
Создайте проект (блог, трекер задач).

Подключите:

БД (PostgreSQL/MySQL)

Аутентификацию

Логирование

Тесты

Выложите на GitHub.

## 6. Полезные ресурсы
Официальная документация FastAPI

Курс FastAPI на freeCodeCamp

Книга "FastAPI: Разработка веб-приложений на Python"
