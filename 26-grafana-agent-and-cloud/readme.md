# Grafana Agent and Cloud

## Quick Start

### Grafana Agent

1. 啟動所有服務

    ```bash
    docker-compose up -d
    ```

2. 檢視服務
   1. FastAPI App
      1. app-a: [http://localhost:8000](http://localhost:8000)
      2. app-b: [http://localhost:8001](http://localhost:8001)
      3. app-c: [http://localhost:8002](http://localhost:8002)
   2. Prometheus: [http://localhost:9090](http://localhost:9090)
   3. Grafana Agent: [http://localhost:12345](http://localhost:12345)
   4. Grafana: [http://localhost:3000](http://localhost:3000)，登入帳號密碼為 `admin/admin`
      1. 使用 [k6](https://k6.io/) 發送 Request

            ```bash
            k6 run --vus 1 --duration 300s k6-script.js
            ```

      2. 使用 Explore 檢視 Tempo、Loki、Prometheus 資料
3. 關閉所有服務

    ```bash
    docker-compose down
    ```

### Grafana Cloud

1. 註冊 [Grafana Cloud](https://grafana.com/auth/sign-up) 帳號
2. 建立 API Key
3. 將 Grafana Cloud 上 Prometheus、Loki、Tempo 的資訊填入 `cloud.env.template`，並且將檔名改為 `cloud.env`
4. 啟動所有服務

    ```bash
    docker-compose -f docker-compose.cloud.yaml up -d
    ```

5. 檢視服務
   1. FastAPI App
      1. app-a: [http://localhost:8000](http://localhost:8000)
      2. app-b: [http://localhost:8001](http://localhost:8001)
      3. app-c: [http://localhost:8002](http://localhost:8002)
   2. Prometheus: [http://localhost:9090](http://localhost:9090)
   3. Grafana Agent: [http://localhost:12345](http://localhost:12345)
   4. Grafana: 進入 Grafana Cloud 上的 Grafana
      1. 使用 [k6](https://k6.io/) 發送 Request

            ```bash
            k6 run --vus 1 --duration 300s k6-script.js
            ```

      2. 使用 Explore 檢視 Tempo、Loki、Prometheus 資料
6. 關閉所有服務

    ```bash
    docker-compose -f docker-compose.cloud.yaml down
    ```

## Goals

### Grafana Agent

1. 建立 FastAPI App（app-a、app-b、app-c）
   1. 透過 OpenTelemetry Manual Instrumentation 產生與收集 Traces，並發送至 Grafana Agent
   2. 透過 OpenTelemetry Manual Instrumentation，將 Trace id 加入 Log 中，輸出於 console
   3. 透過 Prometheus Client 產生 OpenMetrics 格式的 Metrics，揭露於 `/metrics` endpoint
2. 建立 Grafana Agent
   1. 爬取 Prometheus Metrics 後 Remote Write 至 Prometheus
   2. 爬取 Docker Container Log 後轉送至 Loki
   3. 接收 OTEL 格式的 Trace 資料後轉發至 Tempo
3. 建立 Tempo，接收 Traces 資料
4. 建立 Loki，搭配 Loki Docker Driver 收集 Container Log
5. 建立 Prometheus，啟用 Exemplar 功能，收集 app-a、app-b、app-c 的 Metrics
6. 建立 Grafana，查詢 Tempo、Loki、Prometheus 資料

### Grafana Cloud

1. 建立 FastAPI App（app-a、app-b、app-c）
   1. 透過 OpenTelemetry Manual Instrumentation 產生與收集 Traces，並發送至 Grafana Agent
   2. 透過 OpenTelemetry Manual Instrumentation，將 Trace id 加入 Log 中，輸出於 console
   3. 透過 Prometheus Client 產生 OpenMetrics 格式的 Metrics，揭露於 `/metrics` endpoint
2. 建立 Grafana Agent
   1. 爬取 Prometheus Metrics 後 Remote Write 至 Grafana Cloud Prometheus
   2. 爬取 Docker Container Log 後轉送至 Grafana Cloud Loki
   3. 接收 OTEL 格式的 Trace 資料後轉發至 Grafana Cloud Tempo
