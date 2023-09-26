import os
import random
import time
from functools import partial

import statsd
from flask import Flask, Response


class StatsdMiddleware:
    def __init__(self, application, app_name):
        self.__application = application
        self.__app_name = app_name
        self.statsd_client = statsd.StatsClient(os.getenv("STATSD_HOST", "graphite-statsd"), os.getenv("STATSD_PORT", "8125"))

        # send service info with gauge
        self.statsd_client.gauge(f"flask.name.{self.__app_name}", 1)

    def __call__(self, environ, start_response):
        patch_info = {
            "statsd_client": self.statsd_client,
            "app_name": self.__app_name, 
            "method": environ['REQUEST_METHOD'],
            "endpoint": environ['PATH_INFO']
        }

        def _start_response(status, headers, *args, **kwargs):
            # count request by method and endpoint
            kwargs.get("statsd_client").incr(
                f"flask.request_total.${kwargs.get('method', '')}.${kwargs.get('endpoint', '')}".lower(), 1
            )
            return start_response(status, headers, *args)

        # timing each request
        with self.statsd_client.timer("flask.request_duration_seconds"):
            return self.__application(environ, partial(_start_response, **patch_info))


app = Flask(__name__)

# Add statsd middleware to track each request and send statsd UDP request
app.wsgi_app = StatsdMiddleware(app.wsgi_app, "flask-monitoring")

@app.route("/")
def hello_world():
    app.logger.error("Hello, World!")
    return "Hello, World!"

@app.route("/io_task")
def io_task():
    time.sleep(2)
    return "IO bound task finish!"

@app.route("/cpu_task")
def cpu_task():
    for i in range(10000):
        n = i*i*i
    return "CPU bound task finish!"

@app.route("/random_sleep")
def random_sleep():
    time.sleep(random.randint(0,5))
    return "random sleep"

@app.route("/random_status")
def random_status():
    status_code = random.choice([200] * 6 + [300, 400, 400, 500])
    return Response("random status", status=status_code)
