from gi.repository import Adw
from modem_monitor.services.settings import SettingsService

class SettingsTabController:
    def __init__(self, view, window):
        self.view = view
        self.window = window
        self.settings_service = SettingsService(window.auth_service)
    
    def on_login_clicked(self, button):
        username = self.view.username_row.get_text()
        password = self.view.password_row.get_text()
        url = self.view.router_url_row.get_text()
        
        if not username or not password or not url:
            dialog = Adw.MessageDialog(
                transient_for=self.window,
                heading="Missing Information",
                body="Please enter username, password, and router URL."
            )
            dialog.add_response("ok", "OK")
            dialog.set_default_response("ok")
            dialog.set_close_response("ok")
            dialog.present()
            return
        
        # Update router URL
        self.window.auth_service.router_url = url
        
        # Show loading indicator
        self.window.show_toast("Connecting to router...", 1)
        
        # Attempt to login in background
        self.window.auth_service.login(username, password, self.window)
    
    def on_settings_save_clicked(self, button):
        # Get app settings
        auto_refresh = self.view.refresh_row.get_active()
        refresh_interval = int(self.view.interval_row.get_value())
        notifications_enabled = self.view.notify_row.get_active()
        
        # Get data plan settings
        unlimited_plan = self.view.unlimited_plan_row.get_active()
        data_plan_amount = int(self.view.data_plan_row.get_value())
        
        # Save app settings
        success = self.settings_service.save_app_settings(
            auto_refresh, refresh_interval, notifications_enabled,
            unlimited_plan, data_plan_amount
        )
        
        # Also save credentials if needed
        username = self.view.username_row.get_text()
        password = self.view.password_row.get_text()
        url = self.view.router_url_row.get_text()
        
        # Update router URL
        self.window.auth_service.router_url = url
        
        # Save credentials if requested
        if self.view.remember_row.get_active() and username and password and url:
            self.window.auth_service.save_credentials(username, password, url)
        
        # Refresh usage tab if it exists and has a controller
        try:
            usage_tab = self.window.usage_tab
            if hasattr(usage_tab, 'controller'):
                usage_tab.controller.refresh_usage_data()
        except Exception as e:
            print(f"Error refreshing usage tab: {e}")
        
        # Show result
        if success:
            dialog = Adw.MessageDialog(
                transient_for=self.window,
                heading="Settings Saved",
                body="Your settings have been saved successfully."
            )
            dialog.add_response("ok", "OK")
            dialog.set_default_response("ok")
            dialog.set_close_response("ok")
            dialog.present()
        else:
            dialog = Adw.MessageDialog(
                transient_for=self.window,
                heading="Error",
                body="Failed to save application settings."
            )
            dialog.add_response("ok", "OK")
            dialog.set_default_response("ok")
            dialog.set_close_response("ok")
            dialog.present() 