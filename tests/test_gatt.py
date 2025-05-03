import pytest
from wifi_provision.gatt import WiFiProvisionService
import asyncio

@pytest.mark.asyncio
async def test_store_roundtrip():
    class DummyBus:
        async def connect(self): ...
    svc = WiFiProvisionService(DummyBus())
    svc.ssid.WriteValue(list(b"TestSSID"), {})
    svc.psk.WriteValue(list(b"password123"), {})
    assert svc._store["ssid"] == "TestSSID"
    assert svc._store["psk"] == "password123"
