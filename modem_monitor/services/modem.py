import requests
import json
import time
import threading
from gi.repository import GLib

class ModemService:
    def __init__(self, auth_service):
        self.auth_service = auth_service
    
    def fetch_modem_status(self, window):
        if not self.auth_service.is_authenticated:
            window.show_toast("Not authenticated. Please login first.")
            return
            
        # Start a background thread to fetch data
        threading.Thread(target=self._fetch_modem_data, args=(window,), daemon=True).start()
    
    def _fetch_modem_data(self, window):
        try:
            # Use the actual modem status API endpoint
            status_url = f"{self.auth_service.router_url}/cgi-bin/luci/admin/modem/get_csq"
            
            # Add a timestamp parameter to prevent caching
            timestamp = int(time.time() * 1000)
            status_url = f"{status_url}?{timestamp}"
            
            response = self.auth_service.session.get(
                status_url,
                verify=False,
                headers={
                    'User-Agent': 'ModemMonitor/1.0',
                    'Accept': '*/*',
                    'Referer': f"{self.auth_service.router_url}/cgi-bin/luci/admin/modem/nets"
                }
            )
            
            if response.status_code == 200:
                try:
                    # Parse the JSON response
                    data = response.json()
                    GLib.idle_add(window.status_tab.controller.update_status_ui_with_data, data)
                except json.JSONDecodeError:
                    GLib.idle_add(window.show_toast, "Error: Invalid response format")
            else:
                GLib.idle_add(window.show_toast, f"Error: HTTP {response.status_code}")
                
        except Exception as e:
            GLib.idle_add(window.show_toast, f"Error: {str(e)}") 