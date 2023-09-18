# Prometheus

## Quick Start

1. 啟動所有服務

    ```bash
    docker-compose up -d
    ```

2. 檢視服務
   1. Prometheus: [http://localhost:9090](http://localhost:9090)
   2. FastAPI App: [http://localhost:8000](http://localhost:8000)
      1. 可瀏覽 [http://localhost:8000/metrics](http://localhost:8000/metrics) 確認 Metrics 資料
   3. Spring Boot App: [http://localhost:8080](http://localhost:8080)
      1. 可瀏覽 [http://localhost:8080/actuator/prometheus](http://localhost:8080/actuator/prometheus) 確認 Metrics 資料
   4. Grafana: [http://localhost:3000](http://localhost:3000)，登入帳號密碼為 `admin/admin`
      1. 點擊左上 Menu > Dashboards，即可看到透過 Provisioning 建立的 Dashboard(FastAPI Observability、Spring Boot Observability)
      2. 對 FastAPI App 與 Spring Boot App 發送 HTTP Request，即可看到 Dashboard 的變化
         1. 透過瀏覽器發送 Request
            1. FastAPI App
               1. [http://localhost:8000](http://localhost:8000)
               2. [http://localhost:8000/io_task](http://localhost:8000/io_task)
               3. [http://localhost:8000/cpu_task](http://localhost:8000/cpu_task)
               4. [http://localhost:8000/random_sleep](http://localhost:8000/random_sleep)
               5. [http://localhost:8000/random_status](http://localhost:8000/random_status)
            2. Spring Boot App: 
               1. [http://localhost:8080](http://localhost:8080)
               2. [http://localhost:8080/io_task](http://localhost:8080/io_task)
               3. [http://localhost:8080/cpu_task](http://localhost:8080/cpu_task)
               4. [http://localhost:8080/random_sleep](http://localhost:8080/random_sleep)
               5. [http://localhost:8080/random_status](http://localhost:8080/random_status)
         2. 或是使用 [k6](https://k6.io/) 發送 Request

            ```bash
            k6 run --vus 1 --duration 300s k6-script.js
            ```
3. 關閉所有服務

    ```bash
    docker-compose down
    ```

## Goals

1. 建立 Prometheus，並根據 etc/prometheus/prometheus.yml 設定檔，從 FastAPI App 與 Spring Boot App 爬取 Metrics
2. 檢視 Prometheus UI 的 Targets，確認兩個 App 的 Metrics 都有被爬取

## Tasks

<details><summary>Task 1: 在 <a href="http://localhost:8080/actuator/prometheus">http://localhost:8080/actuator/prometheus</a> 中個找一個 Counter、Gauge、Histogram 指標並使用 PromQL 查詢</summary>

1. 瀏覽 [http://localhost:8080/actuator/prometheus](http://localhost:8080/actuator/prometheus) 根據指標附註挑選一個 Counter、Gauge、Histogram 指標
   1. Counter: `http_server_requests_seconds_count`
   2. Gauge: `jvm_memory_used_bytes`
   3. Histogram: `http_server_requests_seconds_bucket`
2. 於 Prometheus Web UI [http://localhost:9090](http://localhost:9090) 查詢
3. 或於 Grafana [http://localhost:3000](http://localhost:3000) 的 Explore 中選擇 Prometheus Data Source 並查詢

</details>

<details><summary>Task 2: 查詢 fastapi_responses_total 指標中 status_code 為 "200" 的值</summary>

1. 查詢語法為 `fastapi_responses_total{status_code="200"}`

</details>

<details><summary>Task 3: 查詢 logback_events_total 中不同 level 的數量</summary>

1. 查詢語法為 `logback_events_total{}`

</details>

<details><summary>Task 4: 計算 logback_events_total 中 level 為 warn 與 info 的總數，並保留 application label</summary>

1. 查詢語法為 `sum(logback_events_total{level="warn"}) by(application) + sum(logback_events_total{level="info"}) by(application)`
2. 或是 `sum(logback_events_total{level=~"warn|info"}) by(application)`

</details>

<details><summary>Task 5: 計算 logback_events_total 中 level warn 與 info 佔所有 log 的比率，並保留 application label</summary>

1. 查詢語法為 `sum(logback_events_total{level=~"warn|info"}) by(application) / sum(logback_events_total) by(application)`

</details>

<details><summary>Task 6: 計算 http_server_requests_seconds_count 中 uri 為 /cpu_task 的值</summary>

1. 查詢語法為 `http_server_requests_seconds_count{uri="/cpu_task"}`

</details>

<details><summary>Task 7: 呈上，計算該指標 3 分鐘內的每秒變化率</summary>

1. 查詢語法為 `rate(http_server_requests_seconds_count{uri="/cpu_task"}[3m])`

</details>

## 參考資料

1. [FastAPI Observability](https://grafana.com/grafana/dashboards/16110-fastapi-observability/)
2. [Spring Boot Observability](https://grafana.com/grafana/dashboards/17175-spring-boot-observability/)
