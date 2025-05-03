"""Entrypoint for systemd service."""
import asyncio
import logging
import sys
from dbus_next.aio import MessageBus
from dbus_next.service import ServiceInterface
from .gatt import WiFiProvisionService
from .config import ADVERTISING_NAME

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

async def _main():
    bus = await MessageBus().connect()
    svc = WiFiProvisionService(bus)
    # Register service and advertisement
    # (BlueZ registration calls omitted for brevity; add if needed.)

    logging.info("Wi‑Fi provisioning service ready as BLE peripheral '%s'", ADVERTISING_NAME)
    while True:
        await asyncio.sleep(3600)

def main():
    try:
        asyncio.run(_main())
    except KeyboardInterrupt:
        sys.exit(0)

if __name__ == "__main__":
    main()
