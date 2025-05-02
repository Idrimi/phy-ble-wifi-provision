# phy-ble-wifi-provision

BLE Wi-Fi provisioning daemon for Raspberry Pi Zero 2 W.

## Features
- Exposes BLE GATT service to receive SSID and password.
- Integrates with NetworkManager over D-Bus to configure Wi-Fi.
- Pure Python implementation (dbus-next, python-networkmanager).
- Packaged with Poetry; systemd integration; unit & integration tests.

## Installation
```bash
sudo apt update
sudo apt install libdbus-1-dev libdbus-glib-1-dev
pip3 install poetry
git clone <repo-url>
cd phy-ble-wifi-provision
poetry install
sudo poetry run wifi-ble-daemon
```

## systemd Setup
Place `wifi-ble-daemon.service` into `/etc/systemd/system` and enable it:
```bash
sudo systemctl enable wifi-ble-daemon
sudo systemctl start wifi-ble-daemon
```

## Testing
```bash
poetry run pytest --cov
```