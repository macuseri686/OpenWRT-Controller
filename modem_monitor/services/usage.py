import requests
import json
import time
import threading
from gi.repository import GLib

class UsageService:
    def __init__(self, auth_service):
        self.auth_service = auth_service
    
    def fetch_usage_data(self, window):
        if not self.auth_service.is_authenticated:
            window.show_toast("Not authenticated. Please login first.")
            return
            
        # Start a background thread to fetch data
        threading.Thread(target=self._fetch_usage_data, args=(window,), daemon=True).start()
    
    def _fetch_usage_data(self, window):
        try:
            # Use the bandwidth usage API endpoint
            usage_url = f"{self.auth_service.router_url}/cgi-bin/luci/admin/nlbw/check_bw"
            
            # Add a timestamp parameter to prevent caching
            timestamp = int(time.time() * 1000)
            usage_url = f"{usage_url}?{timestamp}"
            
            response = self.auth_service.session.get(
                usage_url,
                verify=False,
                headers={
                    'User-Agent': 'ModemMonitor/1.0',
                    'Accept': '*/*',
                    'Referer': f"{self.auth_service.router_url}/cgi-bin/luci/admin/nlbw/bwmon"
                }
            )
            
            if response.status_code == 200:
                try:
                    # Parse the JSON response
                    data = response.json()
                    GLib.idle_add(window.usage_tab.controller.update_usage_ui_with_data, data)
                except json.JSONDecodeError:
                    GLib.idle_add(window.show_toast, "Error: Invalid usage data format")
            else:
                GLib.idle_add(window.show_toast, f"Error: HTTP {response.status_code}")
                
        except Exception as e:
            GLib.idle_add(window.show_toast, f"Error: {str(e)}") 