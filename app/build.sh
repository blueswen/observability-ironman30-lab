#!/bin/bash
docker build -t ghcr.io/blueswen/observability-ironman30-lab/fastapi:latest ./fastapi
docker build -t ghcr.io/blueswen/observability-ironman30-lab/fastapi-otel:latest ./fastapi-otel
docker build -t ghcr.io/blueswen/observability-ironman30-lab/flask-datadog:latest ./flask-datadog
docker build -t ghcr.io/blueswen/observability-ironman30-lab/flask-pystatsd:latest ./flask-pystatsd
docker build -t ghcr.io/blueswen/observability-ironman30-lab/springboot:latest ./springboot
