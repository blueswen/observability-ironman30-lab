# Thanos

## Quick Start

### Sidecar

1. 啟動所有服務

    ```bash
    docker-compose up -d
    ```

2. 開啟瀏覽器，輸入 `http://localhost:3000` 進入 Grafana，登入帳號密碼為 `admin/admin`
3. 點擊左上 Menu > Dashboards > Grafana Stats，即可看到透過 Provisioning 建立的 Dashboard

### Receive

1. 啟動所有服務

    ```bash
    docker-compose -f docker-compose.receive.yaml up -d
    ```

2. 開啟瀏覽器，輸入 `http://localhost:3000` 進入 Grafana，登入帳號密碼為 `admin/admin`
3. 點擊左上 Menu > Dashboards > Grafana Stats，即可看到透過 Provisioning 建立的 Dashboard

## Goals

1. 建立 Thanos，供 Grafana 查詢
   1. Sidecar: 使用 docker-compose.yml，透過 Sidecar 的方式直接讀取 Prometheus TSDB 的資料
   2. Receive: 使用 docker-compose.receive.yml，透過 Receive 的方式接收 Prometheus Remote Write 寫入的資料
2. 建立 Prometheus 供 Sidecar 讀取或 Receive 寫入
3. Grafana 使用 Thanos Query Frontend 當作 Metrics Data Source
