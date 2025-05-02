import asyncio
import logging
from dbus_next.aio import MessageBus
from .ble_server import register_app, start_advertising

def main():
    logging.basicConfig(level=logging.INFO)
    loop = asyncio.get_event_loop()
    try:
        bus = loop.run_until_complete(MessageBus(system=True).connect())
        loop.run_until_complete(register_app(bus))
        loop.run_until_complete(start_advertising(bus))
        loop.run_forever()
    except KeyboardInterrupt:
        logging.info("Shutting down")