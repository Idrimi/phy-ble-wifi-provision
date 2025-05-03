"""BLE GATT service exposing Wi‑Fi credentials."""
import asyncio
from typing import Dict, Optional
from dbus_next.service import ServiceInterface, method, dbus_property, signal
from dbus_next.constants import PropertyAccess
from dbus_next.aio import MessageBus
from dbus_next import Variant

from .config import (
    WIFI_SERVICE_UUID, SSID_UUID, PSK_UUID, CMD_UUID, STAT_UUID, ADVERTISING_NAME
)
from .nm import add_wifi

_adv_mgr = "org.bluez.LEAdvertisingManager1"
_gatt_mgr = "org.bluez.GattManager1"

class WiFiProvisionService(ServiceInterface):
    """Exports a custom GATT tree for provisioning."""

    def __init__(self, bus: MessageBus, index: int = 0) -> None:
        super().__init__("org.bluez.GattService1")
        self.path = f"/wifi/service{index}"
        self.uuid = WIFI_SERVICE_UUID
        self.primary = True
        self._store: Dict[str, str] = {}
        self._bus = bus
        # Child characteristics
        self.ssid = _SSIDChar(self, self._store)
        self.psk = _PSKChar(self, self._store)
        self.cmd = _CmdChar(self, self._store)
        self.stat = _StatChar(self, self._store)

    @dbus_property(access=PropertyAccess.READ)
    def UUID(self) -> str:
        return self.uuid

    @dbus_property(access=PropertyAccess.READ)
    def Primary(self) -> bool:
        return self.primary

    @dbus_property(access=PropertyAccess.READ)
    def Characteristics(self) -> "ao":
        return [
            self.ssid.path,
            self.psk.path,
            self.cmd.path,
            self.stat.path,
        ]

class _BaseChar(ServiceInterface):
    def __init__(self, parent: WiFiProvisionService, uuid: str, flags):
        super().__init__("org.bluez.GattCharacteristic1")
        self._parent = parent
        self._uuid = uuid
        self._flags = flags
        self.path = parent.path + "/" + uuid.split("-")[0]

    @dbus_property(access=PropertyAccess.READ)
    def UUID(self) -> str:
        return self._uuid

    @dbus_property(access=PropertyAccess.READ)
    def Service(self) -> "o":
        return self._parent.path

    @dbus_property(access=PropertyAccess.READ)
    def Flags(self) -> "as":
        return self._flags

class _SSIDChar(_BaseChar):
    def __init__(self, parent, store):
        super().__init__(parent, SSID_UUID, ["write"])
        self._store = store

    @method()
    def WriteValue(self, value: "ay", options: "a{sv}") -> None:
        self._store["ssid"] = bytes(value).decode()

class _PSKChar(_BaseChar):
    def __init__(self, parent, store):
        super().__init__(parent, PSK_UUID, ["write"])
        self._store = store

    @method()
    def WriteValue(self, value: "ay", options: "a{sv}") -> None:
        self._store["psk"] = bytes(value).decode()

class _CmdChar(_BaseChar):
    def __init__(self, parent, store):
        super().__init__(parent, CMD_UUID, ["write"])
        self._store = store

    @method()
    async def WriteValue(self, value: "ay", options: "a{sv}") -> None:
        cmd = bytes(value).decode()
        if cmd != "commit":
            return
        ssid, psk = self._store.get("ssid"), self._store.get("psk")
        stat_char: _StatChar = self._parent.stat
        if not ssid or not psk:
            await stat_char.notify("fail:missing")
            return
        try:
            await add_wifi(ssid, psk)
            await stat_char.notify("ok")
        except Exception as exc:
            await stat_char.notify(f"fail:{exc.__class__.__name__.lower()}")

class _StatChar(_BaseChar):
    def __init__(self, parent, store):
        super().__init__(parent, STAT_UUID, ["notify"])
        self._store = store
        self._notif_enabled = False

    async def notify(self, message: str):
        if not self._notif_enabled:
            return
        self.PropertiesChanged(
            "org.bluez.GattCharacteristic1",
            {"Value": Variant("ay", list(message.encode()))},
            []
        )

    @method()
    def StartNotify(self):
        self._notif_enabled = True

    @method()
    def StopNotify(self):
        self._notif_enabled = False
