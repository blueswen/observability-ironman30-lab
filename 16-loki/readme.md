# Promtail

## Quick Start

1. 安裝 [Loki Docker Driver](https://grafana.com/docs/loki/latest/clients/docker-driver/)

    ```bash
    docker plugin install grafana/loki-docker-driver:latest --alias loki --grant-all-permissions
    ```

2. 啟動所有服務

    ```bash
    docker-compose up -d
    ```

3. 開啟瀏覽器，輸入 `http://localhost:3000` 進入 Grafana，登入帳號密碼為 `admin/admin`
4. 點擊左上 Menu > Explore，左上 Data Source 選擇 `Loki`，在 Label Filter 中 Label 選擇 `compose_service`，Value 選擇 `fastapi`，即可看到 fastapi Container 的 Log
5. 瀏覽 `http://localhost:8000/error_test`，產生 Stack Trace 測試輸出多行 Log 後，查看 Grafana Explore 中的 fastapi Log 是否有收集到新的 Log 以及是否有正確合併多行 Log
6. 關閉所有服務

    ```bash
    docker-compose down
    ```

## Goals

1. 建立 Loki，透過 Loki Docker Driver 收集 Container 的 Log
2. Loki Docker Driver 設定 loki-pipeline-stages，使用正規表示式將多行的 Log 合併成單行
3. 建立 Grafana，讀取 Loki 的資料
