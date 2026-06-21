# EasyCon BLE for Home Assistant

English | [繁體中文](README.md)

[![version](https://img.shields.io/github/manifest-json/v/wescom-code/easycon_ble?filename=custom_components%2Feasycon_ble%2Fmanifest.json)](https://github.com/wescom-code/easycon_ble/releases/latest)
[![releases](https://img.shields.io/github/downloads/wescom-code/easycon_ble/total)](https://github.com/wescom-code/easycon_ble/releases)
[![stars](https://img.shields.io/github/stars/wescom-code/easycon_ble)](https://github.com/wescom-code/easycon_ble/stargazers)
[![issues](https://img.shields.io/github/issues/wescom-code/easycon_ble)](https://github.com/wescom-code/easycon_ble/issues)
[![HACS](https://img.shields.io/badge/HACS-Default-orange.svg)](https://hacs.xyz)

<img src="https://github.com/user-attachments/assets/6dd929aa-aff9-4365-8166-99f6d5d6b0a9" alt="EasyCon banner" style="max-height:128px;" />

This project is a Custom Integration for Home Assistant that controls smart devices using the EasyCon (易智控) solution directly via **local Bluetooth Low Energy (BLE)**.

<p>
  <img src="https://github.com/user-attachments/assets/eb2f80e3-1b3b-4154-a370-667702e9f138" height="128" />
  <img src="https://github.com/user-attachments/assets/888dd4d1-a02e-4bd9-883f-f70089909cd4" height="128" />
  <img src="https://github.com/user-attachments/assets/131632ca-c77f-4f47-bb2d-3f111b45f96c" height="128" />
  <img src="https://github.com/user-attachments/assets/85c20ef3-a5f5-4803-a33b-a4a6f0a0eb29" height="128" />
</p>

## Features

* **Local Control**: Communicates directly with the device via Bluetooth, without relying on cloud services or account registration.
* **Low Latency**: Utilizes Bluetooth `Write Without Response` technology to minimize latency when dragging brightness and color temperature sliders, providing instant feedback.
* **Auto Device Identification**: Built-in database of over 500 devices. By parsing the product ID from Bluetooth broadcast packets, it automatically matches and displays the correct device model and name.
* **Protocol Support**: Supports the AES PKCS7 encrypted handshake authentication and plaintext command control required by the devices.
* **Proxy Support**: Compatible with both the host's built-in Bluetooth module and ESPHome Bluetooth Proxies.

<div>
  <img src="https://github.com/user-attachments/assets/7a006ded-1f79-4a58-bbcd-ceda07d537e2" alt="HA Screenshot 1" height="360" />
  <img src="https://github.com/user-attachments/assets/cb835d94-5b98-49d7-83a1-1a6e02aeb30d" alt="HA Screenshot 2" height="360" />
  <img src="https://github.com/user-attachments/assets/0611f180-f7c2-430e-98b1-8b3f4647e2ed" alt="HA Screenshot 3" height="360" />
</div>

## Installation

<a href="https://my.home-assistant.io/redirect/hacs_repository/?owner=wescom-code&repository=easycon_ble&category=integration">
  <img src="https://my.home-assistant.io/badges/hacs_repository.svg" alt="Open in HACS">
</a>
<a href="https://my.home-assistant.io/redirect/config_flow_start/?domain=easycon_ble">
  <img src="https://my.home-assistant.io/badges/config_flow_start.svg" alt="Add Integration">
</a>

### Method 1: Via HACS (Recommended)
1. Open Home Assistant and navigate to the **HACS** panel.
2. Click the menu in the top right corner and select **Custom repositories**.
3. Paste the URL of this GitHub repository, select **Integration** as the category, and click add.
4. Search for `EasyCon BLE` in HACS and install it.
5. **Restart Home Assistant**.

### Method 2: Manual Installation
1. Download the source code of this project.
2. Copy the `custom_components/easycon_ble` folder into the `custom_components` directory in your Home Assistant configuration folder.
3. **Restart Home Assistant**.

## Configuration

1. Go to Home Assistant **Settings** -> **Devices & Services**.
2. Click **Add Integration** and search for `EasyCon BLE`.
3. The system will automatically search for supported nearby Bluetooth devices. Select the corresponding device from the dropdown menu (e.g., `KLT003 (<AA:BB:CC:DD:EE:FF>) [RSSI:-XX]`).
4. Click submit to finish pairing.

## Supported Devices

**Devices that have been deeply adapted and tested:**
- **KLT003 (Model: SD-860P) Monitor Light Bar**: Supports state feedback, power toggle, and continuous brightness/color temperature adjustment. (Note: Battery level display is not supported due to official design limitations).

**Theoretically compatible EasyCon BLE devices:**
- Smart ceiling lights and eye-care desk lamps with dimming and color temperature (CCT) capabilities (unverified).
- *(Support for other device types like smart plugs, massagers, dehumidifiers, etc., may not be fully adapted yet)*

## Notes

- **Exclusive Connection**: The Bluetooth communication for these devices uses an active connection mode, meaning only one client can connect at a time. When the Home Assistant integration is connected to the device, the official mobile App or WeChat mini-program cannot connect and control it simultaneously; and vice versa.

## FAQ

- **Q: Why can't I find my device?**
  A: Please ensure the device is powered on and within the signal range of your Home Assistant Bluetooth antenna or ESPHome Bluetooth Proxy. You can use the `nRF Connect` app on your phone to verify if you can scan the device's MAC address.
  
- **Q: Why does the device name show as a MAC address instead of the correct model?**
  A: When the device broadcasts Bluetooth packets, some short packets may not contain the model information. The integration has a built-in name caching mechanism; please wait a moment or restart Home Assistant. Once the system receives a broadcast packet with complete information, it will automatically update and remember the correct name.

## Disclaimer

This project is a third-party open-source integration for non-profit academic research purposes only and is not affiliated with the official EasyCon (易智控). The "EasyCon" name, trademarks, and related product identities mentioned herein belong to their respective official owners or rights holders.

## License
This project is licensed under the MIT License.
