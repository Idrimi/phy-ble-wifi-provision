# rpi‑wifi‑provision

Wi‑Fi provisioning over Bluetooth Low Energy for Raspberry Pi Zero 2 W.

* BLE custom GATT peripheral exposes SSID + PSK characteristics
* Writes translate into NetworkManager profiles via D‑Bus
* Ships as a `systemd` service
* Pure Python 3.11, no shell or JavaScript

## Quickstart

```bash
git clone https://github.com/yourname/rpi-wifi-provision.git
cd rpi-wifi-provision
poetry install --only main
sudo cp systemd/wifi-provisiond.service /etc/systemd/system/
sudo systemctl enable --now wifi-provisiond
```

Then use **nRF Connect** or **LightBlue** on your phone to:

1. Discover the `RPI-Setup` device.
2. Write your Wi‑Fi SSID to *SSID* characteristic.
3. Write your WPA2 passphrase to *PSK* characteristic.
4. Write `"commit"` to *Cmd* characteristic and watch Status.

The Pi will join the network and acknowledge with `"ok"`.
