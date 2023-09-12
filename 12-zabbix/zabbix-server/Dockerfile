FROM zabbix/zabbix-server-mysql:ubuntu-6.4-latest

USER root

RUN apt-get update && \
    apt-get install -y zabbix-agent && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

USER zabbix
