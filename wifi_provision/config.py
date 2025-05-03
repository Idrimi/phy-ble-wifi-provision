import os

# 128‑bit UUID base—replace with randomly generated UUIDs for production
BASE_UUID = "a1b2c3d4-{short}-4444-9999-aabbccddeeff"

WIFI_SERVICE_UUID = BASE_UUID.format(short="1111")
SSID_UUID         = BASE_UUID.format(short="2222")
PSK_UUID          = BASE_UUID.format(short="3333")
CMD_UUID          = BASE_UUID.format(short="4444")
STAT_UUID         = BASE_UUID.format(short="5555")

ADVERTISING_NAME  = os.getenv("ADVERTISING_NAME", "RPI-Setup")
WLAN_IFACE        = os.getenv("WLAN_IFACE", "wlan0")
