# Jaeger

## Quick Start

1. 啟動所有服務

    ```bash
    docker-compose up -d
    ```

2. 因 Cassandra 需要一些時間初始化，確認 Jaeger Collector 與 Jaeger Query 已啟動後，再繼續下一步
3. 開啟瀏覽器，輸入 [http://localhost:8000/chain](http://localhost:8000/chain)、[http://localhost:8001/chain](http://localhost:8001/chain)、[http://localhost:8002/chain](http://localhost:8002/chain)、[http://localhost:8003/chain](http://localhost:8003/chain) 對 Flask API 發送一些 Request 
4. 開啟瀏覽器，輸入 `http://localhost:16686` 進入 Jaeger UI，選擇 Service 後點選 Find Traces，即可看到 Trace Data
5. 關閉所有服務

    ```bash
    docker-compose down
    ```

## Goals

1. 建立 Jaeger Components
   1. Jaeger Collector: 接收 Application 發送的 Trace Data
   2. Jaeger Query: 提供 UI 查看 Trace Data
   3. Cassandra: 儲存 Trace Data
   4. Cassandra Schema: 初始化 Cassandra DB
2. FastAPI 透過 OpenTelemetry 發送 Trace Data 至 Jaeger Collector
   1. OTLP HTTP: 發送至 Jaeger Collector 的 4317 Port
   2. OTLP gRPC: 發送至 Jaeger Collector 的 4318 Port
   3. Jaeger Protocol Thrift: 發送至 Jaeger Collector 的 14268 Port
   4. Jaeger Protocol gRPC: 發送至 Jaeger Collector 的 14250 Port
