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

3. 檢視服務
   1. FastAPI App: [http://localhost:8000](http://localhost:8000)
      1. 對 FastAPI App 發送 HTTP Request，會生成 Log
         1. 透過瀏覽器發送 Request
            1. [http://localhost:8000](http://localhost:8000)
            2. [http://localhost:8000/io_task](http://localhost:8000/io_task)
            3. [http://localhost:8000/cpu_task](http://localhost:8000/cpu_task)
            4. [http://localhost:8000/random_sleep](http://localhost:8000/random_sleep)
            5. [http://localhost:8000/random_status](http://localhost:8000/random_status)
            6. [http://localhost:8000/error_test](http://localhost:8000/error_test)
   2. Nginx: [http://localhost:8080](http://localhost:8080)
      1. 瀏覽 Nginx 時會生成 Access Log
   3. Grafana: [http://localhost:3000](http://localhost:3000)，登入帳號密碼為 `admin/admin`
      1. 點擊左上 Menu > Explore，左上 Data Source 選擇 `Loki`，在 Label Filter 中 Label 選擇 `compose_service`，Value 選擇 `fastapi`，即可看到 fastapi Container 的 Log
      2. 瀏覽 `http://localhost:8000/error_test`，產生 Stack Trace 測試輸出多行 Log 後，查看 Grafana Explore 中的 fastapi Log 是否有收集到新的 Log 以及是否有正確合併多行 Log
4. 關閉所有服務

    ```bash
    docker-compose down
    ```

## Goals

1. 建立 Loki，接收 Loki Docker Driver 收集的 Container Log
2. Loki Docker Driver
   1. 設定 `loki-url`，將 Loki Docker Driver 收集的 Log 傳送到 Loki
   2. 設定 `loki-pipeline-stages`，使用正規表示式將多行的 Log 合併成單行
3. 建立 Grafana，讀取 Loki 的資料

## Loki Docker Driver 補充說明

1. Use [YAML anchor and alias](https://support.atlassian.com/bitbucket-cloud/docs/yaml-anchors/) feature to set logging options for each service.
2. Set [Loki Docker Driver options](https://grafana.com/docs/loki/latest/clients/docker-driver/configuration/)
   1. loki-url: loki service endpoint
   2. loki-pipeline-stages: processes multiline log from Spring Boot application with multiline and regex stages ([reference](https://grafana.com/docs/loki/latest/clients/promtail/stages/multiline/))

1. 在 `docker-compose.yml` 中使用了 [YAML anchor and alias](https://support.atlassian.com/bitbucket-cloud/docs/yaml-anchors/)，將 Loki Docker Driver 的設定抽出來，並在每個服務中使用 alias(*) 來引用
2. [Loki Docker Driver options](https://grafana.com/docs/loki/latest/clients/docker-driver/configuration/) 設定
   1. loki-url: Loki 服務的 Endpoint
   2. loki-pipeline-stages: 使用 multiline 和 regex stages 處理 FastAPI App 的多行 Log ([參考](https://grafana.com/docs/loki/latest/clients/promtail/stages/multiline/))

```yaml
x-logging: &default-logging # anchor(&): 'default-logging' 作為這個片段的名稱
  driver: loki
  options:
    loki-url: 'http://localhost:3100/api/prom/push'
    loki-pipeline-stages: |
      - multiline:
          firstline: '^\d{4}-\d{2}-\d{2} \d{1,2}:\d{2}:\d{2}'
          max_wait_time: 3s
      - regex:
          expression: '^(?P<time>\d{4}-\d{2}-\d{2} \d{1,2}:\d{2}:\d{2},d{3}) (?P<message>(?s:.*))$$'
# 在 Compose File 中需使用 $$ (double-dollar sign) 來表示文字中的 $ 符號

version: "3.4"

services:
   foo:
      image: foo
      logging: *default-logging # alias(*): 參照使用前面定義的 default-logging 片段
```

## Tasks

<details><summary>Task 1: 將 fastapi container 的 Log 使用 Pattern 拆解，其中 Level（DEBUG、ERROR 等）解析為 level Label，並將結構調整為只保留時間、Level 與 Log 內容</summary>

1. `{compose_service="fastapi"} | pattern "<date> <timestamp> <level> [<logger>] [<location>:<line>] - <message>" | line_format "{{.date}} {{.timestamp}} {{.level}}\t{{.message}}"`

</details>
