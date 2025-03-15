import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
gi.require_version('Secret', '1')
from gi.repository import Gtk, Adw, GLib

from modem_monitor.tabs.status.view import StatusTabView
from modem_monitor.tabs.connection.view import ConnectionTabView
from modem_monitor.tabs.usage.view import UsageTabView
from modem_monitor.tabs.settings.view import SettingsTabView
from modem_monitor.services.auth import AuthService
from modem_monitor.services.settings import SettingsService

class OpenWRTModemControllerWindow(Adw.ApplicationWindow):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.set_default_size(600, 500)
        
        # Create the auth service
        self.auth_service = AuthService()
        self.settings_service = SettingsService(self.auth_service)
        
        # Create the main box
        self.main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        
        # Create a toast overlay to show notifications
        self.toast_overlay = Adw.ToastOverlay()
        self.toast_overlay.set_child(self.main_box)
        self.set_content(self.toast_overlay)
        
        # Create header bar with view switcher title
        self.header = Adw.HeaderBar()
        self.main_box.append(self.header)
        
        # Create view stack for the different pages
        self.stack = Adw.ViewStack()
        self.stack.set_vexpand(True)
        self.main_box.append(self.stack)
        
        # Create view switcher title (tabs in title bar)
        self.view_switcher_title = Adw.ViewSwitcherTitle()
        self.view_switcher_title.set_stack(self.stack)
        self.view_switcher_title.set_title("OpenWRT Modem Controller")
        self.header.set_title_widget(self.view_switcher_title)
        
        # Initialize tabs
        self.status_tab = StatusTabView(self)
        self.connection_tab = ConnectionTabView(self)
        self.usage_tab = UsageTabView(self)
        self.settings_tab = SettingsTabView(self)
        
        # Add tabs to the stack
        self.stack.add_titled_with_icon(
            self.status_tab.get_view(), 
            "status", 
            "Status", 
            "network-cellular-signal-excellent-symbolic"
        )
        
        self.stack.add_titled_with_icon(
            self.connection_tab.get_view(), 
            "connection", 
            "Connection", 
            "preferences-system-network-symbolic"
        )
        
        self.stack.add_titled_with_icon(
            self.usage_tab.get_view(), 
            "usage", 
            "Usage", 
            "network-transmit-receive-symbolic"
        )
        
        self.stack.add_titled_with_icon(
            self.settings_tab.get_view(), 
            "settings", 
            "Settings", 
            "preferences-system-symbolic"
        )
        
        # Try to load saved credentials and auto-login
        self.auth_service.load_saved_credentials(self)
    
    def show_toast(self, message, timeout=3):
        """Helper method to show toast notifications"""
        toast = Adw.Toast.new(message)
        toast.set_timeout(timeout)
        self.toast_overlay.add_toast(toast) 