import logging
import os
import random
import time

import httpx
import uvicorn
from fastapi import FastAPI, Response, Request

EXPOSE_PORT = os.environ.get("EXPOSE_PORT", 8000)

TARGET_ONE_SVC = os.environ.get("TARGET_ONE_SVC", "localhost:8000")
TARGET_TWO_SVC = os.environ.get("TARGET_TWO_SVC", "localhost:8000")

app = FastAPI()

@app.get("/")
async def read_root(request: Request):
    logging.info(f"Request headers: {request.headers}")
    logging.error("Hello World")
    logging.debug("Debugging log")
    logging.info("Info log")
    logging.warn("Hey, This is a warning!")
    logging.error("Oops! We have an Error. OK")
    return {"Hello": "World"}


@app.get("/io_task")
async def io_task():
    time.sleep(1)
    logging.error("io task")
    return "IO bound task finish!"


@app.get("/cpu_task")
async def cpu_task():
    for i in range(1000):
        n = i*i*i
    logging.error("cpu task")
    return "CPU bound task finish!"


@app.get("/random_status")
async def random_status(response: Response):
    response.status_code = random.choice([200, 200, 300, 400, 500])
    logging.error("random status")
    return {"path": "/random_status"}


@app.get("/random_sleep")
async def random_sleep(response: Response):
    time.sleep(random.randint(0, 5))
    logging.error("random sleep")
    return {"path": "/random_sleep"}


@app.get("/error_test")
async def error_test(response: Response):
    logging.error("got error!!!!")
    raise ValueError("value error")


@app.get("/chain")
async def chain(response: Response):

    logging.info("Chain Started")
    async with httpx.AsyncClient() as client:
        await client.get("http://localhost:8000/")
    async with httpx.AsyncClient() as client:
        await client.get(f"http://{TARGET_ONE_SVC}/io_task")
    async with httpx.AsyncClient() as client:
        await client.get(f"http://{TARGET_TWO_SVC}/cpu_task")
    logging.info("Chain Finished")
    return {"path": "/chain"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=EXPOSE_PORT)
