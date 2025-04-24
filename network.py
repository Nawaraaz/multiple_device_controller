import socket
import threading
import json

class NetworkManager:
    def __init__(self, port=5000):
        self.port = port
        self.server_socket = None
        self.clients = {}
        self.running = False

    def start_server(self, callback):
        """Start a TCP server to accept client connections."""
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(('0.0.0.0', self.port))
        self.server_socket.listen()
        self.running = True

        def accept_connections():
            while self.running:
                try:
                    client, addr = self.server_socket.accept()
                    self.clients[addr] = client
                    threading.Thread(target=self.handle_client, args=(client, addr, callback), daemon=True).start()
                except:
                    break

        threading.Thread(target=accept_connections, daemon=True).start()

    def handle_client(self, client, addr, callback):
        """Handle incoming data from a client."""
        while self.running:
            try:
                data = client.recv(4096)
                if not data:
                    break
                callback(addr, data)
            except:
                break
        client.close()
        del self.clients[addr]

    def connect_to_device(self, ip, port):
        """Connect to a remote device."""
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((ip, port))
        self.clients[(ip, port)] = client
        return client

    def send_data(self, client, data):
        """Send data to a client."""
        client.send(data)

    def stop(self):
        """Stop the server and close all connections."""
        self.running = False
        if self.server_socket:
            self.server_socket.close()
        for client in self.clients.values():
            client.close()
        self.clients.clear()