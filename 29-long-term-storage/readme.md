# Long Term Storage

## Quick Start

### Loki Tempo Mimir with MinIO

1. 啟動所有服務

    ```bash
    docker-compose up -d
    ```

2. 檢視服務
   1. FastAPI App
      1. app-a: [http://localhost:8000](http://localhost:8000)
      2. app-b: [http://localhost:8001](http://localhost:8001)
      3. app-c: [http://localhost:8002](http://localhost:8002)
   2. Grafana Agent: [http://localhost:12345](http://localhost:12345)
   3. MinIO: [http://localhost:9000](http://localhost:9000)，登入帳號密碼為 `minio/supersecret`
   4. Grafana: [http://localhost:3000](http://localhost:3000)，登入帳號密碼為 `admin/admin`
      1. 使用 [k6](https://k6.io/) 發送 Request

            ```bash
            k6 run --vus 1 --duration 300s k6-script.js
            ```

      2. 使用 Explore 檢視 Tempo、Loki、Mimir 資料
3. 關閉所有服務

    ```bash
    docker-compose down
    ```

### OpenTelemetry Collector Filter

1. 啟動所有服務

    ```bash
    docker-compose -f docker-compose.otel.yaml up -d
    ```

2. 檢視服務
   1. Grafana: [http://localhost:3000](http://localhost:3000)，登入帳號密碼為 `admin/admin`
      1. 使用 Explore 檢視 Tempo-1 跟 Tempo-2 的資料
3. 關閉所有服務

    ```bash
    docker-compose -f docker-compose.otel.yaml down
    ```

## Goals

### Loki Tempo Mimir with MinIO

1. 建立 FastAPI App（app-a、app-b、app-c）
   1. 透過 OpenTelemetry Code-based Instrumentation 產生與收集 Traces，並發送至 Grafana Agent
   2. 透過 Prometheus Client 產生 Metrics，揭露於 `/metrics` endpoint
2. 建立 Grafana Agent
   1. 爬取 Prometheus Metrics 後 Remote Write 至 Mimir
   2. 爬取 Docker Container Log 後轉送至 Loki
   3. 接收 OTEL 格式的 Trace 資料後轉發至 Tempo
3. 建立 Tempo，接收 Traces 資料
4. 建立 Loki，接收 Grafana Agent 收集的 Container Log
5. 建立 Mimir，收集 Grafana Agent 收集的 Metrics
6. 建立 Grafana，查詢 Tempo、Loki、Mimir 資料

### OpenTelemetry Collector Filter

1. 建立 [xk6-client-tracing](https://github.com/grafana/xk6-client-tracing/tree/main)，Container 啟動後會自動產生 Traces 資料並發送至 OpenTelemetry Collector，模擬真實環境的 Traces 資料
2. 建立 OpenTelemetry Collector，設定兩個 Pipeline，輸入相同，但處理方式和輸出不同
   1. Pipeline `traces/tempo-1`：接收 Traces 資料，只進行 Batch 後輸出至 Tempo-1
   2. Pipeline `traces/tempo-2`：接收 Traces 資料，進行 Batch 和 Filter 排除 attribute `http.method` 為空的 Span，之後輸出至 Tempo-2
3. 建立 Tempo-1 與 Tempo-2，接收 Traces 資料
4. 建立 Grafana，查詢 Tempo-1 與 Tempo-2 顯示 Traces 資料

## 參考資料

1. [Loki SSD Docker Example](https://github.com/grafana/loki/tree/main/examples/getting-started)
2. [Play with Grafana Mimir](https://github.com/grafana/mimir/tree/main/docs/sources/mimir/get-started/play-with-grafana-mimir)
3. [Tempo S3 Example](https://github.com/grafana/tempo/tree/main/example/docker-compose/s3)
