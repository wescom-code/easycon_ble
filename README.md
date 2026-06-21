# EasyCon BLE for Home Assistant

[![version](https://img.shields.io/github/manifest-json/v/wescom-code/easycon_ble?filename=custom_components%2Feasycon_ble%2Fmanifest.json)](https://github.com/wescom-code/easycon_ble/releases/latest)
[![releases](https://img.shields.io/github/downloads/wescom-code/easycon_ble/total)](https://github.com/wescom-code/easycon_ble/releases)
[![stars](https://img.shields.io/github/stars/wescom-code/easycon_ble)](https://github.com/wescom-code/easycon_ble/stargazers)
[![issues](https://img.shields.io/github/issues/wescom-code/easycon_ble)](https://github.com/wescom-code/easycon_ble/issues)
[![HACS](https://img.shields.io/badge/HACS-Default-orange.svg)](https://hacs.xyz)

<img src="https://private-user-images.githubusercontent.com/89567811/610841370-6dd929aa-aff9-4365-8166-99f6d5d6b0a9.png?jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3ODIwMjE5NzgsIm5iZiI6MTc4MjAyMTY3OCwicGF0aCI6Ii84OTU2NzgxMS82MTA4NDEzNzAtNmRkOTI5YWEtYWZmOS00MzY1LTgxNjYtOTlmNmQ1ZDZiMGE5LnBuZz9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFLSUFWQ09EWUxTQTUzUFFLNFpBJTJGMjAyNjA2MjElMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjYwNjIxVDA2MDExOFomWC1BbXotRXhwaXJlcz0zMDAmWC1BbXotU2lnbmF0dXJlPTY0MzRiZmM3NjI5MWE4OTc4ZTBlMGYwZjM1ZmY5OTI1OTA4NjhmZDI4ZTYxZTM4ODUyMjY2NmZlNjc3NmQ0NDQmWC1BbXotU2lnbmVkSGVhZGVycz1ob3N0JnJlc3BvbnNlLWNvbnRlbnQtdHlwZT1pbWFnZSUyRnBuZyJ9.E65xcr7OS_SryXiyYs2nBiEJtY_Ay9RiaoRWgg8Dj2U" alt="EasyCon banner" style="max-height:128px;" />

本專案為 Home Assistant 的自訂整合（Custom Integration），透過本地藍牙（Bluetooth Low Energy）控制使用 EasyCon(易智控)方案之智慧設備。

<div>
  <img src="https://private-user-images.githubusercontent.com/89567811/610841385-eb2f80e3-1b3b-4154-a370-667702e9f138.jpg?jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3ODIwMjIyODIsIm5iZiI6MTc4MjAyMTk4MiwicGF0aCI6Ii84OTU2NzgxMS82MTA4NDEzODUtZWIyZjgwZTMtMWIzYi00MTU0LWEzNzAtNjY3NzAyZTlmMTM4LmpwZz9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFLSUFWQ09EWUxTQTUzUFFLNFpBJTJGMjAyNjA2MjElMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjYwNjIxVDA2MDYyMlomWC1BbXotRXhwaXJlcz0zMDAmWC1BbXotU2lnbmF0dXJlPTI3MWJlYTBmN2U2MTJkNjM3Y2EyY2VhMzU5MmU3OGVmOWEzY2MyYmU4N2UxZTA5ZDIxNjY1OTBjOGU3MDllNTkmWC1BbXotU2lnbmVkSGVhZGVycz1ob3N0JnJlc3BvbnNlLWNvbnRlbnQtdHlwZT1pbWFnZSUyRmpwZWcifQ.hj83_pnQ0R5JVmtg8mwRD5oKndMxRMn7TRbBjv5GN8w" height="128" />
  <img src="https://private-user-images.githubusercontent.com/89567811/610841384-888dd4d1-a02e-4bd9-883f-f70089909cd4.jpg?jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3ODIwMjUwOTcsIm5iZiI6MTc4MjAyNDc5NywicGF0aCI6Ii84OTU2NzgxMS82MTA4NDEzODQtODg4ZGQ0ZDEtYTAyZS00YmQ5LTg4M2YtZjcwMDg5OTA5Y2Q0LmpwZz9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFLSUFWQ09EWUxTQTUzUFFLNFpBJTJGMjAyNjA2MjElMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjYwNjIxVDA2NTMxN1omWC1BbXotRXhwaXJlcz0zMDAmWC1BbXotU2lnbmF0dXJlPTMwOGVhNDgzMTlhNTZkNjhlYWY2ODg4Nzc3OGRiOTEwOTBiNGZlOTczMjJkMzUyM2Q5MmY0MmI2YjIwZDY0NzMmWC1BbXotU2lnbmVkSGVhZGVycz1ob3N0JnJlc3BvbnNlLWNvbnRlbnQtdHlwZT1pbWFnZSUyRmpwZWcifQ.qID0adneAlHdq07EuP5dCE8H7MIa_eCuIyEICjuzzy4" height="128" />
  <img src="https://private-user-images.githubusercontent.com/89567811/610841382-131632ca-c77f-4f47-bb2d-3f111b45f96c.jpg?jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3ODIwMjUwOTcsIm5iZiI6MTc4MjAyNDc5NywicGF0aCI6Ii84OTU2NzgxMS82MTA4NDEzODItMTMxNjMyY2EtYzc3Zi00ZjQ3LWJiMmQtM2YxMTFiNDVmOTZjLmpwZz9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFLSUFWQ09EWUxTQTUzUFFLNFpBJTJGMjAyNjA2MjElMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjYwNjIxVDA2NTMxN1omWC1BbXotRXhwaXJlcz0zMDAmWC1BbXotU2lnbmF0dXJlPWMyYTkxODg3ZGJiNDY1MGMyYjY3MjI0YWVlODk4NDFhZTJjYWE5OTQwM2QzODMyNGI5YTk2Y2RmNWM2ZDhiNmMmWC1BbXotU2lnbmVkSGVhZGVycz1ob3N0JnJlc3BvbnNlLWNvbnRlbnQtdHlwZT1pbWFnZSUyRmpwZWcifQ.DHHr1TOrfFYfKGgvbYHTT8l9HrU0l3k4O2B3OTvaHqg" height="128" />
  <img src="https://private-user-images.githubusercontent.com/89567811/610841383-85c20ef3-a5f5-4803-a33b-a4a6f0a0eb29.jpg?jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3ODIwMjUwOTcsIm5iZiI6MTc4MjAyNDc5NywicGF0aCI6Ii84OTU2NzgxMS82MTA4NDEzODMtODVjMjBlZjMtYTVmNS00ODAzLWEzM2ItYTRhNmYwYTBlYjI5LmpwZz9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFLSUFWQ09EWUxTQTUzUFFLNFpBJTJGMjAyNjA2MjElMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjYwNjIxVDA2NTMxN1omWC1BbXotRXhwaXJlcz0zMDAmWC1BbXotU2lnbmF0dXJlPTYwNDBmYzMzOGY1YTQ2MTllZDJlNDdmNzQ0YmRlNGJiMTBmNmZhOGNlYTg0YTI0NjIzM2JmZGFlOTBhNGE1NWEmWC1BbXotU2lnbmVkSGVhZGVycz1ob3N0JnJlc3BvbnNlLWNvbnRlbnQtdHlwZT1pbWFnZSUyRmpwZWcifQ.4NSNbIiMJOY9TS9iD7BEgeBRSsXLM9BRWsnXPDzOZdw" height="128" />
</div>

## 功能特點

* **本地控制**：透過藍牙直接與設備連線通訊，無需依賴雲端服務或註冊帳號。
* **低延遲控制**：採用藍牙 `Write Without Response` 技術，減少拖動亮度與色溫滑桿時的操作延遲，提升即時反應。
* **設備自動識別**：內建超過 500 款設備之資料庫，透過解析藍牙廣播封包的產品 ID，自動對應並顯示正確的設備型號與名稱。
* **通訊協議支援**：支援設備端要求的 AES PKCS7 加密握手認證與明文指令控制。
* **代理支援**：相容於主機內建藍牙模組以及 ESPHome Bluetooth Proxy。

<div>
  <img src="https://private-user-images.githubusercontent.com/89567811/610841376-7a006ded-1f79-4a58-bbcd-ceda07d537e2.png?jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3ODIwMjIyODIsIm5iZiI6MTc4MjAyMTk4MiwicGF0aCI6Ii84OTU2NzgxMS82MTA4NDEzNzYtN2EwMDZkZWQtMWY3OS00YTU4LWJiY2QtY2VkYTA3ZDUzN2UyLnBuZz9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFLSUFWQ09EWUxTQTUzUFFLNFpBJTJGMjAyNjA2MjElMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjYwNjIxVDA2MDYyMlomWC1BbXotRXhwaXJlcz0zMDAmWC1BbXotU2lnbmF0dXJlPWUxZmJjMmE2YTg2MjJjNGQ4YWViMWMxZWZkOTBmMzVlNGM1YTFjZjdlMjVmMWQwMjE2YWZmMTlhNDlhMjlhMWEmWC1BbXotU2lnbmVkSGVhZGVycz1ob3N0JnJlc3BvbnNlLWNvbnRlbnQtdHlwZT1pbWFnZSUyRnBuZyJ9.EeA0vUib5YRZ22YNxADEKJJgV7xECvVyq26OFUMNHnQ" alt="HA Screenshot 1" height="360" />
  <img src="https://private-user-images.githubusercontent.com/89567811/610841378-cb835d94-5b98-49d7-83a1-1a6e02aeb30d.png?jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3ODIwMjIyODIsIm5iZiI6MTc4MjAyMTk4MiwicGF0aCI6Ii84OTU2NzgxMS82MTA4NDEzNzgtY2I4MzVkOTQtNWI5OC00OWQ3LTgzYTEtMWE2ZTAyYWViMzBkLnBuZz9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFLSUFWQ09EWUxTQTUzUFFLNFpBJTJGMjAyNjA2MjElMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjYwNjIxVDA2MDYyMlomWC1BbXotRXhwaXJlcz0zMDAmWC1BbXotU2lnbmF0dXJlPTBjYjZkNThmMDFjOTA1ZDc2YThiOTdmY2U4NTBmMDM0OWI3MjE5YWQ2NWZlMTE2N2ZhYjQ0YTUwNThlODdjYmQmWC1BbXotU2lnbmVkSGVhZGVycz1ob3N0JnJlc3BvbnNlLWNvbnRlbnQtdHlwZT1pbWFnZSUyRnBuZyJ9.MMc2jqcYYaHnf6nfh1RvaTeVnKQeVHGdCSDmPBN311M" alt="HA Screenshot 2" height="360" />
  <img src="https://private-user-images.githubusercontent.com/89567811/610841377-0611f180-f7c2-430e-98b1-8b3f4647e2ed.png?jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3ODIwMjIyODIsIm5iZiI6MTc4MjAyMTk4MiwicGF0aCI6Ii84OTU2NzgxMS82MTA4NDEzNzctMDYxMWYxODAtZjdjMi00MzBlLTk4YjEtOGIzZjQ2NDdlMmVkLnBuZz9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFLSUFWQ09EWUxTQTUzUFFLNFpBJTJGMjAyNjA2MjElMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjYwNjIxVDA2MDYyMlomWC1BbXotRXhwaXJlcz0zMDAmWC1BbXotU2lnbmF0dXJlPWM3ZWE5MDg5Y2QzNjE4ZmRhY2FjZTIxZjgwOTBmOTdkZGNmMjM0OGM3YTk3MzkzZTBlOGE1NGZlYTU1YjFkNGQmWC1BbXotU2lnbmVkSGVhZGVycz1ob3N0JnJlc3BvbnNlLWNvbnRlbnQtdHlwZT1pbWFnZSUyRnBuZyJ9.mSvalUWi59syZojtxthSl_ZIKtjrCnZbNZAhBG_fCsc" alt="HA Screenshot 3" height="360" />
</div>

## 安裝方式
<a href="https://my.home-assistant.io/redirect/hacs_repository/?owner=wescom-code&repository=easycon_ble&category=integration">
  <img src="https://my.home-assistant.io/badges/hacs_repository.svg" alt="Open in HACS">
</a>
<a href="https://my.home-assistant.io/redirect/config_flow_start/?domain=easycon_ble">
  <img src="https://my.home-assistant.io/badges/config_flow_start.svg" alt="Add Integration">
</a>

### 方法一：透過 HACS (推薦)
1. 進入 Home Assistant 的 **HACS** 面板。
2. 點選右上角選單，選擇 **自訂儲存庫 (Custom repositories)**。
3. 貼上本 GitHub 專案網址，類別選擇 **整合 (Integration)**，點擊新增。
4. 於 HACS 中搜尋 `EasyCon BLE` 並進行安裝。
5. **重新啟動 Home Assistant**。

### 方法二：手動安裝
1. 下載本專案原始碼。
2. 將 `custom_components/easycon_ble` 資料夾複製至 Home Assistant 設定目錄下的 `custom_components` 資料夾內。
3. **重新啟動 Home Assistant**。

## 設置方式

1. 進入 Home Assistant 的 **設定** -> **裝置與服務**。
2. 點擊 **新增整合**，搜尋 `EasyCon BLE`。
3. 系統將自動搜尋附近支援的藍牙設備，請從下拉選單中選擇對應設備（例如 `KLT003 (<AA:BB:CC:DD:EE:FF>) [RSSI:-XX]`）。
4. 點擊送出完成配對。

## 支援設備

**目前已進行深度適配與測試的設備：**
- **KLT003 (機器型號：SD-860P) 酷斃燈**：支援狀態回報、開關控制、無段調光與調色溫。（註：因原廠設計限制，無提供電量顯示功能）

**理論上相容之其他 EasyCon 藍牙設備：**
- 具備調光、調色溫 (CCT) 功能之智慧吸頂燈及護眼檯燈等(未驗證)。
- *(可能尚未適配包含插座、按摩儀、除濕機等其他類型設備)*

## 注意事項

- **獨佔性連接**：此類設備的藍牙通訊採主動連接模式，同一時間僅允許單一裝置進行連接。當 Home Assistant 整合連線至設備時，原廠手機 App 或微信小程序將無法同時連線控制；反之亦然。

## 常見問題

- **問：為什麼搜尋不到設備？**
  答：請確認設備已接通電源，且位於 Home Assistant 藍牙天線或 ESPHome 藍牙代理的訊號覆蓋範圍內。可先使用手機端 `nRF Connect` 應用程式確認是否能掃描到該設備的 MAC 地址。
  
- **問：為什麼設備名稱顯示 MAC 地址，而非正確型號？**
  答：設備在進行藍牙廣播時，部分封包可能未包含型號資訊。整合本身具備名稱快取機制，請稍候片刻或重新啟動 Home Assistant，待系統接收到包含完整資訊的廣播封包後，即會自動更新並記憶正確名稱。

## 免責聲明

本專案為第三方開源整合，僅供非盈利學術研究用途，與 EasyCon(易智控)官方無任何關聯。文中所提及之「EasyCon」名稱、商標及相關產品識別，其版權及商標權均屬於原官方或其各自之權利人所有。

## 授權條款
本專案採用 MIT License 授權。
