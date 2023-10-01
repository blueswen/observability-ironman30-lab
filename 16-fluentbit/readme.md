# Fluent Bit

## Quick Start

### Basic

1. 啟動所有服務

    ```bash
    docker-compose up -d
    ```

2. 檢視 `fluent-bit` Container log

    ```bash
    docker logs -f fluent-bit
    ```

3. 關閉所有服務

    ```bash
    docker-compose down
    ```

### Container Log with Loki

1. 啟動所有服務

    ```bash
    docker-compose -f docker-compose.loki.yaml up -d
    ```

2. 檢視服務
   1. Nginx: [http://localhost:8080](http://localhost:8080)
      1. 瀏覽 Nginx 時會生成 Access Log
   2. Grafana: [http://localhost:3000](http://localhost:3000)，登入帳號密碼為 `admin/admin`
      1. 點擊左上 Menu > Explore，左上 Data Source 選擇 `Loki`，在 Label Filter 中 Label 選擇 `app`，Value 選擇 `nginx`，即可看到 nginx Container 的 Log
      2. 若要生成更多 Log 也可以使用 [k6](https://k6.io/) 發送更多 Request

            ```bash
            k6 run --vus 1 --duration 300s k6-script.js
            ```

3. 關閉所有服務

    ```bash
    docker-compose down
    ```

### Container Log with Vivo

1. 啟動所有服務

    ```bash
    docker-compose -f docker-compose.vivo.yaml up -d
    ```

2. 檢視服務
   1. Nginx: [http://localhost:8080](http://localhost:8080)
      1. 瀏覽 Nginx 時會生成 Access Log
   2. Vivo: [localhost:8000](localhost:8000)
      1. 點選左側 Logs 可以看到 Fluent Bit 收集到的 Nginx Log
3. 關閉所有服務

    ```bash
    docker-compose -f docker-compose.vivo.yaml down
    ```

## Goals

### Basic

1. 建立 Fluent Bit，使用 [Dummy](https://docs.fluentbit.io/manual/pipeline/inputs/dummy) 與 [Random](https://docs.fluentbit.io/manual/pipeline/inputs/random) Input，將資料送至 [Standard Output](https://docs.fluentbit.io/manual/pipeline/outputs/standard-output) 呈現

### Container Log with Loki

1. 建立 Fluent Bit，使用 [Forward](https://docs.fluentbit.io/manual/pipeline/inputs/forward) 作為 Input 搭配 [Fluentd Logging Driver](https://docs.docker.com/config/containers/logging/fluentd/) 接收 Container Log，使用 [Loki](https://docs.fluentbit.io/manual/pipeline/outputs/loki) 作為 Output 將資料送至 Loki
2. 建立 Loki，負責收取 Fluent Bit 傳送的 Log
3. 建立 Grafana，讀取 Loki 的資料
4. 建立 Nginx，產生 Log

### Container Log with Vivo

1. 建立 Fluent Bit，使用 [Forward](https://docs.fluentbit.io/manual/pipeline/inputs/forward) 作為 Input 搭配 [Fluentd Logging Driver](https://docs.docker.com/config/containers/logging/fluentd/) 接收 Container Log，將資料透過 [Forward](https://docs.fluentbit.io/manual/pipeline/outputs/forward) 送至 [Vivo](https://github.com/calyptia/vivo)
2. 建立 Vivo，負責收取 Fluent Bit 傳送的 Log
3. 建立 Nginx，產生 Log

## Fluentd Logging Driver 補充說明

1. 在 `docker-compose.yml` 中使用了 [YAML anchor and alias](https://support.atlassian.com/bitbucket-cloud/docs/yaml-anchors/)，將 Loki Docker Driver 的設定抽出來，並在每個服務中使用 alias(*) 來引用
2. [Fluentd Logging Driver](https://docs.docker.com/config/containers/logging/fluentd/#options) 設定
   1. fluentd-address: Fluentd 或 Fluent Bit 的 Endpoint
   2. labels: 將指定的 Container Label 加入到 Log 中

```yaml
x-logging: &default-logging # anchor(&): 'default-logging' 作為這個片段的名稱
  driver: fluentd
  options:
    fluentd-address: localhost:24224 # 使用 localhost 是因為 Logging Driver 不是 Container，所以不能使用 Container Name
    labels: "app" # 將 Container Label 'app' 加入到提供給 Fluentd 或 Fluent Bit 的資料中

version: "3.4"

services:
   foo:
      image: foo
      labels:
        app: foo # 提供給 Fluentd 或 Fluent Bit 的資料中會有 app 的資訊，值為 foo
      logging: *default-logging # alias(*): 參照使用前面定義的 default-logging 片段
```

## 參考資料

1. [Docker centralized logging using Fluent Bit, Grafana and Loki](https://medium.com/@thakkaryash94/docker-centralized-logging-using-fluent-bit-grafana-and-loki-bc6784406432)
2. [Vivo](https://github.com/calyptia/vivo)
