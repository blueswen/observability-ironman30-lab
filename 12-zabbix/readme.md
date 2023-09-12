# Zabbix

## Quick Start

1. 啟動所有服務

    ```bash
    docker-compose up -d
    ```

2. 進入 Zabbix Server Container，並啟動 Zabbix Agent

    ```bash
    docker exec -it zabbix-server-mysql /bin/bash
    service zabbix-agent start
    ```

3. 開啟瀏覽器，輸入 `http://localhost:` 進入 Zabbix，登入帳號密碼為 `Admin/zabbix`，如果出現 DB 相關的錯誤訊息，請等待一段時間
4. 使用 Grafana 連接 Zabbix Data Source
   1. 進入 Grafana Container，並安裝 Zabbix Data Source Plugin

        ```bash
        docker exec -it grafana /bin/bash
        grafana-cli plugins install alexanderzobnin-zabbix-app
        ```
    2. 重啟 Grafana
    
        ```bash
        docker-compose restart grafana
        ```

    3. 開啟瀏覽器，輸入 `http://localhost:3000` 進入 Grafana，登入帳號密碼為 `admin/admin`    
    4. 點擊左上 Menu > Administration > Plugins > Zabbix，點擊 Enable 啟用 Zabbix Data Source
    5. 點擊左上 Menu > Explore > Zabbix，即可看到 Zabbix Data Source 的資料
5. 關閉所有服務

    ```bash
    docker-compose down
    ```

## Goals

1. 建立 Zabbix 完整服務
2. 建立 Zabbix Agent，並連接至 Zabbix Server
3. 建立 FastAPI，並連接至 Zabbix Server 使用 WEB Scenario 監控服務
4. 使用 Grafana 連接 Zabbix Data Source
