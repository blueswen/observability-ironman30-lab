# Metrics From Traces

## Quick Start

### Basic

1. 啟動所有服務

    ```bash
    docker-compose up -d
    ```

2. 檢視服務
   1. FastAPI App: [http://localhost:8000](http://localhost:8000)
   2. Spring Boot App: [http://localhost:8080](http://localhost:8080)
   3. Prometheus: [http://localhost:9090](http://localhost:9090)
   4. Grafana: [http://localhost:3000](http://localhost:3000)，登入帳號密碼為 `admin/admin`
      1. 使用 [k6](https://k6.io/) 發送 Request

            ```bash
            k6 run --vus 1 --duration 300s k6-script.js
            ```
      
      2. 點擊左上 Menu > Dashboards > OpenTelemetry APM，即可看到透過 Provisioning 建立的 Dashboard
3. 關閉所有服務

    ```bash
    docker-compose down
    ```

### Jaeger SPM

1. 啟動所有服務

    ```bash
    docker-compose -f docker-compose.jaeger.yaml up -d
    ```

2. 檢視服務
   1. 因 Cassandra 需要一些時間初始化，確認 Jaeger Collector 與 Jaeger Query 已啟動後，再繼續下一步

        ```bash
        docker-compose ps
        ```

   2. FastAPI App: [http://localhost:8000](http://localhost:8000)
   3. Spring Boot App: [http://localhost:8080](http://localhost:8080)
   4. Prometheus: [http://localhost:9090](http://localhost:9090)
   5. Jaeger UI: [http://localhost:16686](http://localhost:16686)
      1. 使用 [k6](https://k6.io/) 發送 Request

            ```bash
            k6 run --vus 1 --duration 300s k6-script.js
            ```

      2. 選擇 Jaeger UI 上方選單 Monitor 頁籤，可查看服務儀表板
   
3. 關閉所有服務

    ```bash
    docker-compose -f docker-compose.jaeger.yaml down
    ```

## Goals

### Basic

1. 建立 FastAPI App（fastapi），透過 OpenTelemetry Automatic Instrumentation 產生與收集 Traces，並發送至 OpenTelemetry Collector
2. 建立 Spring Boot App（spring-boot），透過 OpenTelemetry Automatic Instrumentation 產生與收集 Traces，並發送至 OpenTelemetry Collector
3. 建立 OpenTelemetry Collector
   1. 接收 Traces 資料，將 Traces 資料轉送至 Tempo 並透過 Span Metrics Connector 產生 Metrics
   2. 接收 Span Metrics Connector 產生的 Metrics 資料，並揭露於自己的 8889 Port 供 Prometheus 爬取
4. 建立 Tempo，接收 OpenTelemetry Collector 發送的 Traces 資料
5. 建立 Prometheus，爬取 OpenTelemetry Collector 的 Metrics 資料
6. 建立 Grafana，查詢 Tempo 與 Prometheus 資料

### Jaeger SPM

1. 建立 FastAPI App（fastapi），透過 OpenTelemetry Automatic Instrumentation 產生與收集 Traces，並發送至 OpenTelemetry Collector
2. 建立 Spring Boot App（spring-boot），透過 OpenTelemetry Automatic Instrumentation 產生與收集 Traces，並發送至 OpenTelemetry Collector
3. 建立 OpenTelemetry Collector
   1. 接收 Traces 資料，將 Traces 資料轉送至 Tempo 並透過 Span Metrics Connector 產生 Metrics
   2. 接收 Span Metrics Connector 產生的 Metrics 資料，並揭露於自己的 8889 Port 供 Prometheus 爬取
4. 建立 Prometheus，爬取 OpenTelemetry Collector 的 Metrics 資料
5. 建立 Jaeger Components
   1. Jaeger Collector: 接收 OpenTelemetry Collector 發送的 Traces 資料
   2. Jaeger Query: 提供 UI 查看 Trace Data，並從 Prometheus 取得 Metrics 資料供 Jaeger SPM 使用
   3. Cassandra: 儲存 Trace Data
   4. Cassandra Schema: 初始化 Cassandra DB

## 參考資料

1. [FastAPI Tracing with Jaeger through OpenTelemetry](https://github.com/blueswen/fastapi-jaeger)
2. [OpenTelemetry Application Performance Management](https://github.com/blueswen/opentelemetry-apm)
