from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QPushButton, QListWidget
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt
import sys

class RemoteDesktopGUI(QMainWindow):
    def __init__(self, discovery_callback, connect_callback):
        super().__init__()
        self.setWindowTitle("Multi-Desktop Control")
        self.setGeometry(100, 100, 800, 600)
        self.tabs = QTabWidget()
        self.device_list = QListWidget()
        self.connect_button = QPushButton("Connect")
        self.connect_button.clicked.connect(self.on_connect)
        layout = QVBoxLayout()
        layout.addWidget(self.device_list)
        layout.addWidget(self.connect_button)
        container = QWidget()
        container.setLayout(layout)
        self.tabs.addTab(container, "Devices")
        self.setCentralWidget(self.tabs)
        self.discovery_callback = discovery_callback
        self.connect_callback = connect_callback
        self.devices = []

    def update_devices(self, devices):
        """Update the list of discovered devices."""
        self.devices = devices
        self.device_list.clear()
        for device in devices:
            self.device_list.addItem(f"{device['name']} ({device['ip']}:{device['port']})")

    def on_connect(self):
        """Connect to the selected device."""
        selected = self.device_list.currentRow()
        if selected >= 0:
            device = self.devices[selected]
            self.connect_callback(device['ip'], device['port'])

    def add_desktop(self, ip, port):
        """Add a new tab for a remote desktop."""
        widget = QWidget()
        self.tabs.addTab(widget, f"{ip}:{port}")
        return widget

    def update_desktop(self, widget, img):
        """Update the desktop image in a tab."""
        qimg = QImage(img.rgb, img.width, img.height, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qimg)
        # Add rendering logic here (e.g., QLabel to display pixmap)