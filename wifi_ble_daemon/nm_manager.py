import logging
import NetworkManager

def provision(ssid: str, psk: str) -> bool:
    nm = NetworkManager.NetworkManager
    connection = {
      '802-11-wireless': {
         'mode': 'infrastructure',
         'security': '802-11-wireless-security',
         'ssid': bytes(ssid, 'utf-8')
      },
      '802-11-wireless-security': {
         'key-mgmt': 'wpa-psk',
         'psk': psk
      },
      'connection': {
         'id': f'ble-{ssid}',
         'type': '802-11-wireless',
         'autoconnect': False
      },
      'ipv4': {'method':'auto'},
      'ipv6': {'method':'ignore'}
    }
    try:
        nm.AddAndActivateConnection(connection, '/org/freedesktop/NetworkManager/Devices/0', '/')
        logging.info(f"Activated connection for SSID {ssid}")
        return True
    except Exception as e:
        logging.error(f"Provisioning failed: {e}")
        return False
