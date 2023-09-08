# StatsD

## Quick Start

### StatsD + Graphite

1. 啟動所有服務

    ```bash
    docker-compose up -d
    ```

2. 開啟瀏覽器，輸入 [http://localhost:8000/cpu_task](http://localhost:8000/cpu_task) 對 Flask API 發送一些 Request 
3. 開啟瀏覽器，於 Graphite web UI([http://localhost](http://localhost)) 確認指標收集結果，或是直接輸入 [http://localhost/render?from=-10mins&until=now&target=stats.flask.request_total.get.-cpu_task](http://localhost/render?from=-10mins&until=now&target=stats.flask.request_total.get.-cpu_task)
4. 關閉所有服務

    ```bash
    docker-compose down
    ```

### StatsD Exporter + Prometheus

1. 啟動所有服務

    ```bash
    docker-compose -f docker-compose.exporter.yaml up -d
    ```

2. 開啟瀏覽器，輸入 [http://localhost:8000/cpu_task](http://localhost:8000/cpu_task) 對 Flask API 發送一些 Request 
3. 開啟瀏覽器，輸入 `http://localhost:3000` 進入 Grafana，登入帳號密碼為 `admin/admin`
4. 點擊左上 Menu > Dashboards > Flask Monitoring，即可看到透過 Provisioning 建立的 Dashboard
5. 關閉所有服務

    ```bash
    docker-compose -f docker-compose.exporter.yaml down
    ```

## Goals

透過 StatsD 收集 Flask API 的 Metrics

1. StatsD + Graphite: 使用 docker-compose.yml
   1. 使用 All in One Image: graphiteapp/docker-graphite-statsd 將 StatsD 與 Graphite 一起啟動
   2. 使用 Graphite web UI 確認指標收集結果
2. StatsD Exporter + Prometheus: 使用 docker-compose.exporter.yml
   1. 使用 StatsD Exporter 將 StatsD 資料轉換成 Prometheus Metrics
   2. 使用 Prometheus 收集 Metrics
   3. 使用 Grafana 查詢 Prometheus Metrics
