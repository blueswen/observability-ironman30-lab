# Thanos

## Quick Start

### Sidecar

1. 啟動所有服務

    ```bash
    docker-compose up -d
    ```

2. 檢視服務
   1. Prometheus: [http://localhost:9090](http://localhost:9090)
   2. Thanos Query Frontend: [http://localhost:9091](http://localhost:9091)
   3. Grafana: [http://localhost:3000](http://localhost:3000)，登入帳號密碼為 `admin/admin`
      1. 點擊左上 Menu > Dashboards > Grafana Stats，即可看到透過 Provisioning 建立的 Dashboard
3. 關閉所有服務

    ```bash
    docker-compose down
    ```

### Receive

1. 啟動所有服務

    ```bash
    docker-compose -f docker-compose.receive.yaml up -d
    ```

2. 檢視服務
   1. Prometheus: [http://localhost:9090](http://localhost:9090)
   2. Thanos Query Frontend: [http://localhost:9091](http://localhost:9091)
   3. Grafana: [http://localhost:3000](http://localhost:3000)，登入帳號密碼為 `admin/admin`
      1. 點擊左上 Menu > Dashboards > Grafana Stats，即可看到透過 Provisioning 建立的 Dashboard
3. 關閉所有服務

    ```bash
    docker-compose -f docker-compose.receive.yaml down
    ```

## Goals

1. 建立 Thanos，供 Grafana 查詢
   1. Sidecar: 使用 docker-compose.yml，透過 Sidecar 讀取 Prometheus 的資料，並將資料寫入 Object Storage
   2. Receive: 使用 docker-compose.receive.yml，透過 Receive 的方式接收 Prometheus Remote Write 寫入的資料
2. 建立 Prometheus 供 Sidecar 讀取或 Receive 寫入
3. Grafana 使用 Thanos Query Frontend 當作 Metrics Data Source

## 參考資料

1. [thanos-docker-compose](https://github.com/thanos-community/thanos-docker-compose)
