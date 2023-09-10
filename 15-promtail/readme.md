# Promtail

## Quick Start

1. 啟動所有服務

    ```bash
    docker-compose up -d
    ```

2. 開啟瀏覽器，輸入 `http://localhost:3000` 進入 Grafana，登入帳號密碼為 `admin/admin`
3. 點擊左上 Menu > Explore，左上 Data Source 選擇 `Loki`，在 Label Filter 中 Label 選擇 `container`，Value 選擇 `nginx`，即可看到 Nginx Container 的 Log
4. 瀏覽 `http://localhost:8080`，即可看到 Nginx 的預設頁面，查看 Grafana Explore 中的 Nginx Log 是否有收集到新的 Log
5. 關閉所有服務

    ```bash
    docker-compose down
    ```

## Goals

1. 建立 Promtail，並 Mount Docker Socket 至 Promtail Container，讓 Promtail 可以讀取 Label 為 `logging=promtail` 的 Container 的 Log
2. 建立 Loki，負責收取 Promtail 傳送的 Log
3. 建立 Grafana，讀取 Loki 的資料
