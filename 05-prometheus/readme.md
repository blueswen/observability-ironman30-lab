# Prometheus

## Quick Start

1. 啟動所有服務

    ```bash
    docker-compose up -d
    ```

2. 開啟瀏覽器，輸入 `http://localhost:9090` 開啟 Prometheus UI
3. 關閉所有服務

    ```bash
    docker-compose down
    ```

## Goals

1. 建立 Prometheus，並根據 etc/prometheus/prometheus.yml 設定檔，從 FastAPI App 與 Spring Boot App 爬取 Metrics
2. 檢視 Prometheus UI 的 Targets，確認兩個 App 的 Metrics 都有被爬取
