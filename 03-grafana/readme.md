# Grafana

## Quick Start

1. 啟動所有服務

    ```bash
    docker-compose up -d
    ```

2. 開啟瀏覽器，輸入 `http://localhost:3000`，登入帳號密碼為 `admin/admin`
3. 點擊左上 Menu > Dashboards > Grafana Stats，即可看到透過 Provisioning 建立的 Dashboard

## Goals

1. 建立 Grafana，並將資料 Mount 至本機，確保資料不會因 Container 關閉而遺失
2. 使用 Provisioning 的方式建立 Data Source、Dashboard
3. 視覺化呈現 Prometheus Data Source 的資料於 Dashboard
