"""Thin async wrapper around NetworkManager D‑Bus API."""
import asyncio
from typing import Dict, Any
from dbus_next.aio import MessageBus

async def add_wifi(ssid: str, psk: str, iface: str = "wlan0") -> str:
    """Create or update a Wi‑Fi connection profile and return the D‑Bus path."""
    ssid_raw = list(ssid.encode())
    settings: Dict[str, Any] = {
        "connection": {
            "id": f"prov-{ssid}",
            "type": "802-11-wireless",
            "interface-name": iface,
            "autoconnect": True,
        },
        "802-11-wireless": {
            "ssid": ssid_raw,
            "mode": "infrastructure",
        },
        "802-11-wireless-security": {
            "key-mgmt": "wpa-psk",
            "psk": psk,
        },
        "ipv4": {"method": "auto"},
        "ipv6": {"method": "ignore"},
    }

    bus = await MessageBus().connect()
    proxy = await bus.introspect(
        "org.freedesktop.NetworkManager",
        "/org/freedesktop/NetworkManager/Settings",
    )
    settings_obj = bus.get_proxy_object(
        "org.freedesktop.NetworkManager",
        "/org/freedesktop/NetworkManager/Settings",
        proxy,
    )
    iface_settings = settings_obj.get_interface("org.freedesktop.NetworkManager.Settings")

    try:
        path = await iface_settings.call_add_connection(settings)
    except Exception as exc:
        # Duplicate? Try modify
        for c_path in await iface_settings.call_list_connections():
            c_proxy = await bus.introspect("org.freedesktop.NetworkManager", c_path)
            c_obj = bus.get_proxy_object("org.freedesktop.NetworkManager", c_path, c_proxy)
            con = c_obj.get_interface("org.freedesktop.NetworkManager.Settings.Connection")
            details = await con.call_get_settings()
            if details["connection"]["id"].value == f"prov-{ssid}":
                await con.call_update(settings)
                path = c_path
                break
        else:
            raise
    return path
