import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

from src.discovery import DeviceDiscovery
from src.network import NetworkManager
from src.screen_share import ScreenShare
from src.input_control import InputControl
from src.gui import RemoteDesktopGUI
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QThread, pyqtSignal
# ... rest of the code remains unchanged ...
class DiscoveryThread(QThread):
    devices_discovered = pyqtSignal(list)

    def __init__(self, discovery):
        super().__init__()
        self.discovery = discovery

    def run(self):
        self.discovery.discover_devices(self.devices_discovered.emit)

class MultiDesktopControl:
    def __init__(self):
        self.discovery = DeviceDiscovery()
        self.network = NetworkManager()
        self.screen_share = ScreenShare()
        self.input_control = InputControl()
        self.app = QApplication(sys.argv)
        self.gui = RemoteDesktopGUI(self.on_devices_discovered, self.on_connect)
        self.network.start_server(self.on_network_data)
        self.discovery_thread = DiscoveryThread(self.discovery)
        self.discovery_thread.devices_discovered.connect(self.gui.update_devices)
        self.discovery_thread.start()

    def on_devices_discovered(self, devices):
        self.gui.update_devices(devices)

    def on_connect(self, ip, port):
        client = self.network.connect_to_device(ip, port)
        widget = self.gui.add_desktop(ip, port)
        self.screen_share.start_sharing(client)

    def on_network_data(self, addr, data):
        self.screen_share.receive_screen(data, lambda img: self.gui.update_desktop(None, img))

    def run(self):
        self.discovery.register_service()
        self.gui.show()
        sys.exit(self.app.exec_())

    def stop(self):
        self.discovery.close()
        self.network.stop()
        self.screen_share.stop()
        self.discovery_thread.quit()
        self.discovery_thread.wait()

if __name__ == "__main__":
    app = MultiDesktopControl()
    try:
        app.run()
    finally:
        app.stop()