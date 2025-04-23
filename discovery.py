from zeroconf import ServiceInfo, Zeroconf, ServiceBrowser, ServiceStateChange
import socket
import time

class DeviceDiscovery:
    def __init__(self, service_name="_multidesktop._tcp.local."):
        self.zeroconf = Zeroconf()
        self.service_name = service_name
        self.devices = []

    def register_service(self, port=5000):
        """Register this device as a service on the network."""
        ip = socket.gethostbyname(socket.gethostname())
        info = ServiceInfo(
            type_=self.service_name,
            name=f"{socket.gethostname()}.{self.service_name}",
            addresses=[socket.inet_aton(ip)],
            port=port,
            properties={b"name": socket.gethostname().encode()},
        )
        self.zeroconf.register_service(info)
        return info

    def discover_devices(self, callback):
        """Discover other devices on the network."""
        def on_service_state_change(zeroconf, service_type, name, state_change):
            if state_change == ServiceStateChange.Added:
                info = zeroconf.get_service_info(service_type, name)
                if info and info.addresses:  # Ensure info and addresses are valid
                    ip = socket.inet_ntoa(info.addresses[0])
                    device_name = info.properties.get(b"name", b"Unknown").decode()
                    self.devices.append({"name": device_name, "ip": ip, "port": info.port})
                    callback(self.devices)

        browser = ServiceBrowser(self.zeroconf, self.service_name, handlers=[on_service_state_change])
        return browser

    def close(self):
        """Close the zeroconf instance."""
        self.zeroconf.close()