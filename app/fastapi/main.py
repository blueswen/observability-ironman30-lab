import logging
import os
import random
import time
from typing import Optional

import httpx
import uvicorn
from fastapi import FastAPI, Response
from utils import PrometheusMiddleware, metrics

APP_NAME = os.environ.get("APP_NAME", "fastapi-demo-app")
EXPOSE_PORT = os.environ.get("EXPOSE_PORT", 8000)

ENABLE_PYROSCOPE = os.environ.get("ENABLE_PYROSCOPE", "false").lower().strip()
PYROSCOPE_SERVER = os.environ.get("PYROSCOPE_SERVER", "http://pyroscope:4040")

if ENABLE_PYROSCOPE == "true":
    import pyroscope

    logging.error("Pyroscope enabled")

    pyroscope.configure(
        application_name=APP_NAME,
        server_address=PYROSCOPE_SERVER,
    )

TARGET_ONE_SVC = os.environ.get("TARGET_ONE_SVC", "localhost:8000")
TARGET_TWO_SVC = os.environ.get("TARGET_TWO_SVC", "localhost:8000")

logging.basicConfig(
    format="%(asctime)s %(levelname)s [%(name)s] [%(filename)s:%(lineno)d] - %(message)s"
)

app = FastAPI()

# Setting metrics middleware
app.add_middleware(PrometheusMiddleware, app_name=APP_NAME)
app.add_route("/metrics", metrics)


class EndpointFilter(logging.Filter):
    # Uvicorn endpoint access log filter
    def filter(self, record: logging.LogRecord) -> bool:
        return record.getMessage().find("GET /metrics") == -1


# Filter out /metrics
logging.getLogger("uvicorn.access").addFilter(EndpointFilter())


@app.get("/")
async def read_root():
    logging.error("Hello World")
    return {"Hello": "World"}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Optional[str] = None):
    logging.error("items")
    return {"item_id": item_id, "q": q}


@app.get("/io_task")
async def io_task():
    time.sleep(1)
    logging.error("io task")
    return "IO bound task finish!"


@app.get("/cpu_task")
async def cpu_task():
    for i in range(1000):
        _ = i * i * i
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
    logging.info("Chain Start")

    async with httpx.AsyncClient() as client:
        await client.get(
            "http://localhost:8000/",
        )
    async with httpx.AsyncClient() as client:
        await client.get(
            f"http://{TARGET_ONE_SVC}/io_task",
        )
    async with httpx.AsyncClient() as client:
        await client.get(
            f"http://{TARGET_TWO_SVC}/cpu_task",
        )
    logging.info("Chain Finished")
    return {"path": "/chain"}


if __name__ == "__main__":
    # update uvicorn access logger format
    log_config = uvicorn.config.LOGGING_CONFIG
    log_config["formatters"]["access"][
        "fmt"
    ] = "%(asctime)s %(levelname)s [%(name)s] [%(filename)s:%(lineno)d] - %(message)s"
    log_config["formatters"]["default"][
        "fmt"
    ] = "%(asctime)s %(levelname)s [%(name)s] [%(filename)s:%(lineno)d] - %(message)s"
    uvicorn.run(app, host="0.0.0.0", port=EXPOSE_PORT, log_config=log_config)
