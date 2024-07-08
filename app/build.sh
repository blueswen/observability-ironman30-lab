#!/bin/bash
docker build -t ghcr.io/blueswen/observability-ironman30-lab/fastapi:latest ./fastapi
docker build -t ghcr.io/blueswen/observability-ironman30-lab/fastapi-otel:latest ./fastapi-otel
docker build -t ghcr.io/blueswen/observability-ironman30-lab/flask-datadog:latest ./flask-datadog
docker build -t ghcr.io/blueswen/observability-ironman30-lab/flask-pystatsd:latest ./flask-pystatsd
docker build -t ghcr.io/blueswen/observability-ironman30-lab/springboot:latest ./springboot
docker build -t ghcr.io/blueswen/observability-ironman30-lab/todo-app/backend:latest ./todo-app/backend
docker build -t ghcr.io/blueswen/observability-ironman30-lab/todo-app/jquery-app:latest ./todo-app/jquery-app
docker build -t ghcr.io/blueswen/observability-ironman30-lab/todo-app/vue-app:latest ./todo-app/vue-app
