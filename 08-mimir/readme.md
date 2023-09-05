# Mimir

## Quick Start

1. 啟動所有服務

    ```bash
    docker-compose up -d
    ```

2. 開啟瀏覽器，輸入 `http://localhost:3000` 進入 Grafana，登入帳號密碼為 `admin/admin`
3. 點擊左上 Menu > Dashboards > Grafana Stats，即可看到透過 Provisioning 建立的 Dashboard

## Goals

1. 建立 Mimir，供 Grafana 使用
2. 建立 Prometheus 透過 remote write 的方式將資料寫入 Mimir
3. Grafana 使用 Mimir 當作 Metrics Data Source
