import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw

from modem_monitor.tabs.settings.controller import SettingsTabController

class SettingsTabView:
    def __init__(self, window):
        self.window = window
        self.controller = SettingsTabController(self, window)
        
        # Load current settings
        settings = window.settings_service.get_app_settings()
        
        # Create a scrolled window for the settings tab
        self.scroll = Gtk.ScrolledWindow()
        self.scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        self.scroll.set_vexpand(True)
        
        # Create a box for the settings content
        self.box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.box.set_margin_top(20)
        self.box.set_margin_bottom(20)
        self.box.set_margin_start(20)
        self.box.set_margin_end(20)
        self.scroll.set_child(self.box)
        
        # Add a title
        title = Gtk.Label()
        title.set_markup("<span size='x-large' weight='bold'>Settings</span>")
        title.set_halign(Gtk.Align.START)
        self.box.append(title)
        
        # Router Login Settings
        self.login_group = Adw.PreferencesGroup(title="Router Login Credentials")
        self.login_group.set_description("Credentials used to access the router's web interface")
        self.box.append(self.login_group)
        
        # Router URL
        self.router_url_row = Adw.EntryRow(title="Router URL")
        self.router_url_row.set_text(window.auth_service.router_url)
        self.login_group.add(self.router_url_row)
        
        # Username field
        self.username_row = Adw.EntryRow(title="Username")
        self.username_row.set_text("")
        self.login_group.add(self.username_row)
        
        # Password field
        self.password_row = Adw.PasswordEntryRow(title="Password")
        self.password_row.set_text("")
        self.login_group.add(self.password_row)
        
        # Remember credentials switch
        self.remember_row = Adw.SwitchRow(title="Remember Credentials")
        self.remember_row.set_subtitle("Store login information securely")
        self.remember_row.set_active(True)
        self.login_group.add(self.remember_row)
        
        # Login button
        self.login_button = Gtk.Button(label="Login")
        self.login_button.set_halign(Gtk.Align.CENTER)
        self.login_button.set_margin_top(20)
        self.login_button.add_css_class("suggested-action")
        self.login_button.connect("clicked", self.controller.on_login_clicked)
        self.login_group.add(self.login_button)
        
        # Application Settings
        self.app_group = Adw.PreferencesGroup(title="Application Settings")
        self.box.append(self.app_group)
        
        # Auto-refresh switch
        self.refresh_row = Adw.SwitchRow(title="Auto-refresh")
        self.refresh_row.set_subtitle("Automatically refresh modem status")
        self.refresh_row.set_active(settings.get('auto_refresh', True))
        self.app_group.add(self.refresh_row)
        
        # Refresh interval
        self.interval_row = Adw.SpinRow(title="Refresh Interval")
        self.interval_row.set_subtitle("Time between refreshes (seconds)")
        self.interval_row.set_range(5, 300)
        self.interval_row.set_value(settings.get('refresh_interval', 30))
        self.interval_row.set_digits(0)
        self.app_group.add(self.interval_row)
        
        # Data Plan Settings
        self.data_plan_group = Adw.PreferencesGroup(title="Data Plan Settings")
        self.data_plan_group.set_description("Configure your monthly data plan")
        self.data_plan_group.set_margin_top(10)
        self.box.append(self.data_plan_group)
        
        # Unlimited data plan switch
        self.unlimited_plan_row = Adw.SwitchRow(title="Unlimited Data Plan")
        self.unlimited_plan_row.set_subtitle("Toggle if you have an unlimited data plan")
        self.unlimited_plan_row.set_active(settings.get('unlimited_plan', False))
        self.unlimited_plan_row.connect("notify::active", self.on_unlimited_toggled)
        self.data_plan_group.add(self.unlimited_plan_row)
        
        # Data plan amount
        self.data_plan_row = Adw.SpinRow(title="Data Plan Amount (GB)")
        self.data_plan_row.set_subtitle("Your monthly data allowance in gigabytes")
        self.data_plan_row.set_range(1, 10000)  # 1GB to 10TB
        self.data_plan_row.set_value(settings.get('data_plan_amount', 1000))
        self.data_plan_row.set_digits(0)
        self.data_plan_row.set_sensitive(not settings.get('unlimited_plan', False))
        self.data_plan_group.add(self.data_plan_row)
        
        # Notifications switch
        self.notify_row = Adw.SwitchRow(title="Enable Notifications")
        self.notify_row.set_subtitle("Show notifications for important events")
        self.notify_row.set_active(settings.get('notifications_enabled', True))
        self.app_group.add(self.notify_row)
        
        # Save button
        self.save_button = Gtk.Button(label="Save Settings")
        self.save_button.set_halign(Gtk.Align.CENTER)
        self.save_button.set_margin_top(10)
        self.save_button.add_css_class("suggested-action")
        self.save_button.connect("clicked", self.controller.on_settings_save_clicked)
        self.box.append(self.save_button)
    
    def get_view(self):
        return self.scroll
    
    def populate_credentials(self, username, password, url):
        """Populate the credential fields with saved values"""
        self.username_row.set_text(username)
        self.password_row.set_text(password)
        self.router_url_row.set_text(url)
    
    def get_credentials(self):
        """Get the current credentials from the UI"""
        return self.username_row.get_text(), self.password_row.get_text()
    
    def should_remember_credentials(self):
        """Check if credentials should be remembered"""
        return self.remember_row.get_active()
    
    def on_unlimited_toggled(self, switch, param):
        """Enable/disable data plan amount based on unlimited toggle"""
        is_unlimited = switch.get_active()
        self.data_plan_row.set_sensitive(not is_unlimited) 