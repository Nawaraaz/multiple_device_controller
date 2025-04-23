import pyautogui
import json

class InputControl:
    def send_input(self, client, event_type, data):
        """Send input event to a remote device."""
        message = json.dumps({"type": event_type, "data": data}).encode()
        client.send(message)

    def process_input(self, data):
        """Process received input event."""
        event = json.loads(data.decode())
        if event["type"] == "mouse_move":
            pyautogui.moveTo(event["data"]["x"], event["data"]["y"])
        elif event["type"] == "mouse_click":
            pyautogui.click()
        elif event["type"] == "key_press":
            pyautogui.press(event["data"]["key"])