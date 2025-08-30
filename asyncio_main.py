import time
import asyncio

from fastapi import FastAPI

app2 = FastAPI()

def sync_task():
    time.sleep(3)
    print("Отправлен email")

async def async_task():
    await asyncio.sleep(3)
    print("Сделан сторонний запрос в API")


@app2.post("/")
async def some_route():
    sync_task()
    return {"ok": True}