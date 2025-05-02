import pytest
from wifi_ble_daemon.nm_manager import provision
import NetworkManager

def test_provision_success(monkeypatch):
    class FakeNM:
        def AddAndActivateConnection(self, *args): return "ok"
    monkeypatch.setattr(NetworkManager, 'NetworkManager', FakeNM())
    assert provision("MySSID", "password123") is True

def test_provision_fail(monkeypatch):
    class FakeNM:
        def AddAndActivateConnection(self, *args): raise Exception("Auth fail")
    monkeypatch.setattr(NetworkManager, 'NetworkManager', FakeNM())
    assert provision("MySSID", "bad") is False
