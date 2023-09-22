# Mimir

此範例僅建立單一 Mimir，並將資料儲存於 Local Disk 中，若要建立多實體的 Mimir 並搭配 [MinIO](https://min.io/) 的版本，可以參考官方提供的範例 [Play with Mimir](https://grafana.com/tutorials/play-with-grafana-mimir/)。

## Quick Start

1. 啟動所有服務

    ```bash
    docker-compose up -d
    ```

2. 檢視服務
   1. Prometheus: [http://localhost:9090](http://localhost:9090)
   2. Mimir: [http://localhost:9009](http://localhost:9009)
      1. 可檢視 Mimir 各 Component 的狀態
   3. Grafana: [http://localhost:3000](http://localhost:3000)，登入帳號密碼為 `admin/admin`
      1. 點擊左上 Menu > Dashboards，即可看到透過 Provisioning 建立的 Dashboard(Grafana Stats、Mimir / Overview)
3. 關閉所有服務

    ```bash
    docker-compose down
    ```

## Goals

1. 建立 Mimir，供 Grafana 查詢與 Prometheus 寫入
2. 建立 Prometheus，並根據 `etc/prometheus/prometheus.yml` 設定檔，透過 remote write 的方式將資料寫入 Mimir
3. Grafana 使用 Mimir 當作 Prometheus Data Source

## 參考資料

1. [Grafana Internals](https://grafana.com/grafana/dashboards/3590-grafana-internals/)
2. [Mimir / Overview](https://grafana.com/grafana/dashboards/17607-mimir-overview/)
