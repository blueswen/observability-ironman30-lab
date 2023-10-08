# 時光之鏡：透視過去、現在與未來的 Observability

此 Project 為 iThome 鐵人賽 2023 [「時光之鏡：透視過去、現在與未來的 Observability」](https://ithelp.ithome.com.tw/users/20162175/ironman/6445) 的 Repo，用來存放文章中的範例程式碼。

## 常見問題排除

1. 已安裝 Docker Loki Driver，但使用時出現 `Error response from daemon: error looking up logging plugin loki: plugin loki found but disabled` 錯誤訊息
   1. 重新啟用 Loki Driver，執行指令 `docker plugin enable loki`
