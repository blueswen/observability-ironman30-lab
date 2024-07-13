# Faro Web SDK

## Quick Start

1. 啟動所有服務

    ```bash
    docker-compose up -d
    ```

2. 檢視服務
   1. Todo App
      1. Backend App: Swagger UI [http://localhost:8080/docs](http://localhost:8080/docs)，檢視 API
      2. Frontend App: 操作 Todo App，讓 Faro Web SDK 產生資料，供後續查詢
         1. jQuery App: [http://localhost](http://localhost)
         2. Vue App: [http://localhost:8080](http://localhost:8080)
   2. Grafana Alloy: [http://localhost:12345](http://localhost:12345)
   3. Grafana: [http://localhost:3000](http://localhost:3000)，登入帳號密碼為 `admin/admin`
      1. 點擊左上 Menu > Dashboards，即可看到透過 Provisioning 建立的 Dashboard - Frontend Observability
      2. 使用 Explore 檢視 Tempo、Loki 資料
3. 關閉所有服務

    ```bash
    docker-compose down
    ```

## Goals

1. 建立 Frontend App，透過 Faro Web SDK 產生與收集 Web Vital 指標、Console Log、Errors、Session、View、Performance、Tracing 等資訊，並發送至 Grafana Alloy
2. 建立 Backend App，透過 OpenTelemetry Zero-code Instrumentation 產生 Traces，並發送至 Tempo
3. 建立 Grafana Alloy 用於接收 Faro Web SDK 產生的資料，並轉送至 Loki 與 Tempo
4. 建立 Loki 用於收集 Grafana Alloy 傳送的 Log 資料
5. 建立 Tempo 用於收集 Grafana Alloy 與 OpenTelemetry Zero-code Instrumentation 傳送的 Trace 資料
6. 建立 Grafana 用於查詢 Loki 與 Tempo 的資料

## 參考資料

1. [Grafana Faro - Frontend Monitoring](https://grafana.com/grafana/dashboards/17766-frontend-monitoring/)
