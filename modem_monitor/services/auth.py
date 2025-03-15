import gi
gi.require_version('Secret', '1')
from gi.repository import Secret, GLib
import requests
import urllib3
import threading

# Disable SSL warnings for self-signed certificates
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class AuthService:
    def __init__(self):
        self.router_url = "https://192.168.1.1"
        self.session = requests.Session()
        self.session_cookie = None
        self.is_authenticated = False
    
    def load_saved_credentials(self, window):
        try:
            # Fix the schema to include both attributes we're using
            schema = Secret.Schema.new("org.example.openwrt",
                                      Secret.SchemaFlags.NONE,
                                      {
                                          "application": Secret.SchemaAttributeType.STRING,
                                          "key": Secret.SchemaAttributeType.STRING
                                      })
            
            # Get username
            username_attributes = {"application": "openwrt_modem_controller", "key": "router_username"}
            username = Secret.password_lookup_sync(schema, username_attributes, None)
            
            # Get password
            password_attributes = {"application": "openwrt_modem_controller", "key": "router_password"}
            password = Secret.password_lookup_sync(schema, password_attributes, None)
            
            # Get URL
            url_attributes = {"application": "openwrt_modem_controller", "key": "router_url"}
            url = Secret.password_lookup_sync(schema, url_attributes, None)
            
            if username and password and url:
                self.router_url = url
                
                # We need to wait until the UI is fully initialized before setting these values
                def populate_fields():
                    # Populate settings tab fields
                    window.settings_tab.populate_credentials(username, password, url)
                    return False  # Remove this idle source
                
                # Schedule this to run after UI initialization
                GLib.idle_add(populate_fields)
                
                # Attempt to login in background
                threading.Thread(target=self.login, args=(username, password, window), daemon=True).start()
        except Exception as e:
            print(f"Error loading saved credentials: {e}")
    
    def login(self, username, password, window):
        try:
            login_url = f"{self.router_url}/cgi-bin/luci"
            
            # Prepare login data
            login_data = {
                'luci_username': username,
                'luci_password': password
            }
            
            # Make login request
            response = self.session.post(
                login_url,
                data=login_data,
                verify=False,  # Skip SSL verification for self-signed certs
                headers={
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'User-Agent': 'ModemMonitor/1.0'
                }
            )
            
            # Check if login was successful by looking for the sysauth cookie
            if 'sysauth' in self.session.cookies:
                self.session_cookie = self.session.cookies.get('sysauth')
                self.is_authenticated = True
                
                # Update UI on the main thread
                GLib.idle_add(self.on_login_success, window, username, password)
                return True
            else:
                # Update UI on the main thread
                GLib.idle_add(self.on_login_failure, window, "No authentication cookie received")
                return False
                
        except Exception as e:
            # Update UI on the main thread
            GLib.idle_add(self.on_login_failure, window, str(e))
            return False
    
    def on_login_success(self, window, username=None, password=None):
        # Update UI to show logged-in state
        window.show_toast("Successfully connected to router")
        
        # Save credentials if remember option is enabled
        if window.settings_tab.should_remember_credentials():
            # If username/password not provided, try to get from UI
            if username is None and password is None:
                username, password = window.settings_tab.get_credentials()
            
            url = self.router_url
            
            if username and password and url:
                self.save_credentials(username, password, url)
        
        # Refresh modem status
        window.status_tab.controller.refresh_modem_status()
    
    def on_login_failure(self, window, error_message):
        # Show error dialog
        dialog = Adw.MessageDialog(
            transient_for=window,
            heading="Login Failed",
            body=f"Could not connect to the router: {error_message}"
        )
        dialog.add_response("ok", "OK")
        dialog.set_default_response("ok")
        dialog.set_close_response("ok")
        dialog.present()
    
    def save_credentials(self, username, password, url):
        try:
            # Use Secret Service directly
            schema = Secret.Schema.new("org.example.openwrt",
                                      Secret.SchemaFlags.NONE,
                                      {"application": Secret.SchemaAttributeType.STRING,
                                       "key": Secret.SchemaAttributeType.STRING})
            
            # Store username
            username_attributes = {"application": "openwrt_modem_controller", "key": "router_username"}
            Secret.password_store_sync(schema, username_attributes, Secret.COLLECTION_DEFAULT,
                                      "OpenWRT Router Username", username, None)
            
            # Store password
            password_attributes = {"application": "openwrt_modem_controller", "key": "router_password"}
            Secret.password_store_sync(schema, password_attributes, Secret.COLLECTION_DEFAULT,
                                      "OpenWRT Router Password", password, None)
            
            # Store URL
            url_attributes = {"application": "openwrt_modem_controller", "key": "router_url"}
            Secret.password_store_sync(schema, url_attributes, Secret.COLLECTION_DEFAULT,
                                      "OpenWRT Router URL", url, None)
        except Exception as e:
            print(f"Error saving credentials: {e}") 