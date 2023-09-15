# Exporter

## Quick Start

1. 啟動所有服務

    ```bash
    docker-compose up -d
    ```

2. 開啟瀏覽器，輸入 `http://localhost:9090` 開啟 Prometheus UI
3. 開啟瀏覽器，輸入 `http://localhost:8080` 開啟 cAdvisor 內建的 UI
4. 關閉所有服務

    ```bash
    docker-compose down
    ```

## Goals

1. 建立 cAdvisor
2. 建立 Node Exporter
3. 建立 Prometheus，爬取 Node Exporter 與 cAdvisor 的 Metrics
