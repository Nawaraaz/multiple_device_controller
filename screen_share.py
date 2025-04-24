from mss import mss
from PIL import Image
import io
import threading
import time

class ScreenShare:
    def __init__(self):
        self.running = False

    def start_sharing(self, client, interval=0.1):
        self.running = True
        def share_loop():
            with mss() as sct:
                while self.running:
                    monitor = sct.monitors[1]  # Primary monitor
                    screenshot = sct.grab(monitor)
                    img = Image.frombytes('RGB', (screenshot.width, screenshot.height), screenshot.rgb)
                    buffer | io.BytesIO()
                    img.save(buffer, format='JPEG', quality=70)
                    data = buffer.getvalue()
                    print(f"Sending screen data: {len(data)} bytes")
                    try:
                        client.send(len(data).to_bytes(4, 'big') + data)
                    except:
                        break
                    time.sleep(interval)
        threading.Thread(target=share_loop, daemon=True).start()

    def receive_screen(self, data, callback):
        img = Image.open(io.BytesIO(data))
        callback(img)

    def stop(self):
        self.running = False