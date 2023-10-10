# Profiles and eBPF

## Quick Start

1. 啟動所有服務

    ```bash
    docker-compose up -d
    ```

2. 檢視服務
   1. FastAPI App: [http://localhost:8000](http://localhost:8000)
   2. Spring Boot App: [http://localhost:8080](http://localhost:8080)
   3. 使用 [k6](https://k6.io/) 發送 Request

        ```bash
        k6 run --vus 1 --duration 300s k6-script.js
        ```

   4. Pyroscope: [http://localhost:4040](http://localhost:4040)
      1. 左上下拉選單可查看不同服務的 Profile
         1. fastapi：FastAPI App 使用 SDK 取得的 Profile
         2. spring-boot：Spring Boot App 使用 SDK 取得的 Profile
         3. compose-example：Grafana Agent 透過 eBPF 取得的所有 Container Profile
         4. pyroscope：Pyroscope 服務本身的 Profile
   5. Grafana: [http://localhost:3000](http://localhost:3000)，登入帳號密碼為 `admin/admin`
      1. 點擊左上 Menu > Explore，左上 Data Source 選擇 `Pyroscope`
         1. 查詢條件選擇 `process_cpu - cpu`，查詢語法輸入
            1. `{service_name="fastapi"}` 可以查看 FastAPI App 使用 SDK 取得的 CPU Profile
            2. `{service_name="spring-boot"}` 可以查看 Spring Boot App 使用 SDK 取得的 CPU Profile
            3. `{service_name="compose-example"}` 可以查看 Grafana Agent 透過 eBPF 取得的所有 Container CPU Profile
            4. `{service_name="pyroscope"}` 可以查看 Pyroscope 服務本身的 CPU Profile
3. 關閉所有服務

    ```bash
    docker-compose down
    ```

## Goals

1. 建立 FastAPI App（fastapi），透過 [Pyroscope Python SDK](https://github.com/grafana/pyroscope/tree/main) 收集 Profile 資料，並發送至 Pyroscope
2. 建立 Spring Boot App（spring-boot），透過 [Agent Jar](https://grafana.com/docs/pyroscope/next/configure-client/language-sdks/java/#start-pyroscope-as-javaagent) 的方式使用 [Pyroscope Java SDK](https://github.com/grafana/pyroscope-java) 收集 Profile 資料，並發送至 Pyroscope
3. 建立 [Grafana Agent](https://grafana.com/oss/agent/)，透過 eBPF 收集 Container 的 Profile 資料，並發送至 Pyroscope
4. 建立 Pyroscope，接收 Profile 資料，並提供 Web UI 查詢
5. 建立 Grafana，查詢 Pyroscope 資料

## 參考資料

1. [Grafana Pyroscope documentation](https://grafana.com/docs/pyroscope/latest/)
2. [Grafana Agent Pull Mode Integration](https://github.com/grafana/pyroscope/tree/main/examples/grafana-agent)
