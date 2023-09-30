# Promtail

## Quick Start

1. 啟動所有服務

    ```bash
    docker-compose up -d
    ```

2. 檢視服務
   1. Nginx: [http://localhost:8080](http://localhost:8080)
      1. 瀏覽 Nginx 時會生成 Access Log
   2. Grafana: [http://localhost:3000](http://localhost:3000)，登入帳號密碼為 `admin/admin`
      1. 點擊左上 Menu > Explore，左上 Data Source 選擇 `Loki`，在 Label Filter 中 Label 選擇 `container`，Value 選擇 `nginx`，即可看到 nginx Container 的 Log
      2. 若要生成更多 Log 也可以使用 [k6](https://k6.io/) 發送更多 Request

            ```bash
            k6 run --vus 1 --duration 300s k6-script.js
            ```

3. 關閉所有服務

    ```bash
    docker-compose down
    ```

## Goals

1. 建立 Promtail，並 Mount Docker Socket 至 Promtail Container，讓 Promtail 可以讀取 Label 為 `logging=promtail` 的 Container 的 Log
2. 建立 Loki，負責收取 Promtail 傳送的 Log
3. 建立 Grafana，讀取 Loki 的資料

## Promtail Configuration

```yaml
# ./etc/promtail.yaml
server:
  http_listen_port: 9080 # promtail port，預設為 9080
  grpc_listen_port: 0

positions:
  filename: /tmp/positions.yaml 

clients:
  - url: http://loki:3100/loki/api/v1/push # Loki 的 URL

scrape_configs:
  - job_name: container_scrape # Job Name
    docker_sd_configs: # 使用 Docker Service Discovery
      - host: unix:///var/run/docker.sock # Docker Socket 的位置
        refresh_interval: 5s # 每 5 秒重新掃描一次 Docker Socket
        filters: # 只收集 Label 為 logging=promtail 的 Container
          - name: label
            values: ["logging=promtail"]
    relabel_configs: # 將 Docker 相關的資訊轉換成 Label
      - source_labels: ['__meta_docker_container_name'] # 將 __meta_docker_container_name 轉為新的名為 container 的 Label
        regex: '/(.*)' # 使用正規表達式取出 Container Name
        target_label: 'container'
      - source_labels: ['__meta_docker_container_log_stream'] # 將 __meta_docker_container_log_stream 轉為新的名為 logstream 的 Label
        target_label: 'logstream'
```
