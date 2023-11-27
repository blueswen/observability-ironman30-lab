# Profiles and eBPF

## Quick Start

### Pyroscope

1. 啟動所有服務

    ```bash
    docker-compose up -d
    ```

2. 檢視服務
   1. FastAPI App: [http://localhost:8000](http://localhost:8000)
   2. Spring Boot App: [http://localhost:8080](http://localhost:8080)
   3. 使用 [k6](https://k6.io/) 發送 Request

        ```bash
        k6 run --vus 1 --duration 300s k6-script.js
        ```

   4. Pyroscope: [http://localhost:4040](http://localhost:4040)
      1. 左上下拉選單可查看不同服務的 Profile
         1. fastapi：FastAPI App 使用 SDK 取得的 Profile
         2. spring-boot：Spring Boot App 使用 SDK 取得的 Profile
         3. compose-example：Grafana Agent 透過 eBPF 取得的所有 Container Profile
         4. pyroscope：Pyroscope 服務本身的 Profile
   5. Grafana: [http://localhost:3000](http://localhost:3000)，登入帳號密碼為 `admin/admin`
      1. 點擊左上 Menu > Explore，左上 Data Source 選擇 `Pyroscope`
         1. 查詢條件選擇 `process_cpu - cpu`，查詢語法輸入
            1. `{service_name="fastapi"}` 可以查看 FastAPI App 使用 SDK 取得的 CPU Profile
            2. `{service_name="spring-boot"}` 可以查看 Spring Boot App 使用 SDK 取得的 CPU Profile
            3. `{service_name="compose-example"}` 可以查看 Grafana Agent 透過 eBPF 取得的所有 Container CPU Profile
            4. `{service_name="pyroscope"}` 可以查看 Pyroscope 服務本身的 CPU Profile
3. 關閉所有服務

    ```bash
    docker-compose down
    ```

### Beyla

若使用 Docker Desktop 且非使用 WSL2（即使用 linuxkit），Docker Desktop 需更新至 `24.0.6` 版以上，才有支援 Beyla 需要的 BTF 功能（[Enabling BTF support in kernel image](https://github.com/linuxkit/linuxkit/issues/3755#issuecomment-1821702440)），否則會出現以下錯誤：

```txt
loading and assigning BPF objects: field KprobeSysExit: program kprobe_sys_exit: apply CO-RE relocations: load kernel spec: no BTF found for kernel version 6.4.16-linuxkit: not supported
```

1. 啟動所有服務

    ```bash
    docker-compose -f docker-compose.beyla.yaml up -d
    ```

2. 檢視服務
   1. FastAPI App: [http://localhost:8000](http://localhost:8000)
   2. Spring Boot App: [http://localhost:8080](http://localhost:8080)
   3. 使用 [k6](https://k6.io/) 發送 Request

        ```bash
        k6 run --vus 1 --duration 300s k6-script.js
        ```

   4. Grafana: [http://localhost:3000](http://localhost:3000)，登入帳號密碼為 `admin/admin`
      1. 點擊左上 Menu > Explore，左上 Data Source 選擇 `Prometheus`
         1. 查詢語法輸入 `http_server_duration_seconds_count{job="fastapi-beyla"}` 可以查詢 FastAPI App 的 Metrics
         2. 查詢語法輸入 `http_server_duration_seconds_count{job="spring-boot-beyla"}` 可以查詢 Spring Boot App 的 Metrics
      2. 點擊左上 Menu > Explore，左上 Data Source 選擇 `Tempo`
         1. Query Type：Search 可以查詢 Traces
3. 關閉所有服務

    ```bash
    docker-compose -f docker-compose.beyla.yaml down
    ```

## Goals

### Pyroscope

1. 建立 FastAPI App（fastapi），透過 [Pyroscope Python SDK](https://github.com/grafana/pyroscope/tree/main) 收集 Profile 資料，並發送至 Pyroscope
2. 建立 Spring Boot App（spring-boot），透過 [Agent Jar](https://grafana.com/docs/pyroscope/next/configure-client/language-sdks/java/#start-pyroscope-as-javaagent) 的方式使用 [Pyroscope Java SDK](https://github.com/grafana/pyroscope-java) 收集 Profile 資料，並發送至 Pyroscope
3. 建立 [Grafana Agent](https://grafana.com/oss/agent/)，透過 eBPF 收集 Container 的 Profile 資料，並發送至 Pyroscope
4. 建立 Pyroscope，接收 Profile 資料，並提供 Web UI 查詢
5. 建立 Grafana，查詢 Pyroscope 資料

### Beyla

1. 建立 FastAPI App（fastapi）與其專用的 Beyla Instance（fastapi-beyla），Beyla Instance 會監控 FastAPI App 的 8000 port，並透過 eBPF 收集 Metrics 與 Traces 資料，Metrics 以 Prometheus 格式揭露，Traces 發送至 Tempo
2. 建立 Spring Boot App（spring-boot）與其專用的 Beyla Instance（spring-boot-beyla），Beyla Instance 會監控 Spring Boot App 的 8080 port，並透過 eBPF 收集 Metrics 與 Traces 資料，Metrics 以 Prometheus 格式揭露，Traces 發送至 Tempo
3. 建立 Prometheus，爬取 fastapi-beyla 與 spring-boot-beyla 的 Metrics 資料
4. 建立 Tempo，接收 fastapi-beyla 與 spring-boot-beyl 發送的 Traces 資料
5. 建立 Grafana，查詢 Tempo、Prometheus 資料

> [!WARNING]  
> 目前 Beyla(1.0.1) 尚不支援分散式追蹤，但該功能已在進行開發中

## 參考資料

1. [Grafana Pyroscope documentation](https://grafana.com/docs/pyroscope/latest/)
2. [Grafana Agent Pull Mode Integration](https://github.com/grafana/pyroscope/tree/main/examples/grafana-agent)
