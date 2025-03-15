from gi.repository import Gtk, Adw
from modem_monitor.services.settings import SettingsService

class ConnectionTabController:
    def __init__(self, view, window):
        self.view = view
        self.window = window
        self.settings_service = SettingsService(window.auth_service)
    
    def on_band_configure_clicked(self, button):
        # Show a dialog for band configuration
        dialog = Adw.Dialog()
        dialog.set_title("Band Configuration")
        dialog.set_default_size(400, 300)
        dialog.set_transient_for(self.window)
        
        content = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        content.set_margin_top(20)
        content.set_margin_bottom(20)
        content.set_margin_start(20)
        content.set_margin_end(20)
        content.set_spacing(10)
        
        title = Gtk.Label()
        title.set_markup("<span size='large' weight='bold'>Configure Network Bands</span>")
        title.set_halign(Gtk.Align.START)
        content.append(title)
        
        # LTE Bands
        lte_group = Adw.PreferencesGroup(title="LTE Bands")
        content.append(lte_group)
        
        for band in ["B1 (2100 MHz)", "B2 (1900 MHz)", "B3 (1800 MHz)", "B4 (1700 MHz)", "B66 (1700 MHz)"]:
            row = Adw.SwitchRow(title=band)
            if "B66" in band:
                row.set_active(True)
            lte_group.add(row)
        
        # 5G Bands
        nr_group = Adw.PreferencesGroup(title="5G Bands")
        content.append(nr_group)
        
        for band in ["N41 (2500 MHz)", "N71 (600 MHz)", "N77 (3700 MHz)", "N78 (3500 MHz)"]:
            row = Adw.SwitchRow(title=band)
            if "N77" in band:
                row.set_active(True)
            nr_group.add(row)
        
        # Buttons
        button_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        button_box.set_halign(Gtk.Align.END)
        button_box.set_margin_top(20)
        
        cancel_button = Gtk.Button(label="Cancel")
        cancel_button.connect("clicked", lambda _: dialog.close())
        button_box.append(cancel_button)
        
        apply_button = Gtk.Button(label="Apply")
        apply_button.add_css_class("suggested-action")
        apply_button.connect("clicked", lambda _: dialog.close())
        button_box.append(apply_button)
        
        content.append(button_box)
        
        dialog.set_content(content)
        dialog.present()
    
    def on_save_clicked(self, button):
        # Get values from UI
        apn = self.view.apn_row.get_text()
        username = self.view.username_row.get_text()
        password = self.view.password_row.get_text()
        network_mode = self.view.mode_row.get_selected()
        roaming_enabled = self.view.roaming_row.get_active()
        
        # Save settings
        success = self.settings_service.save_connection_settings(
            apn, username, password, network_mode, roaming_enabled
        )
        
        # Show result
        if success:
            dialog = Adw.MessageDialog(
                transient_for=self.window,
                heading="Settings Saved",
                body="Your connection settings have been saved."
            )
            dialog.add_response("ok", "OK")
            dialog.set_default_response("ok")
            dialog.set_close_response("ok")
            dialog.present()
        else:
            dialog = Adw.MessageDialog(
                transient_for=self.window,
                heading="Error",
                body="Failed to save connection settings."
            )
            dialog.add_response("ok", "OK")
            dialog.set_default_response("ok")
            dialog.set_close_response("ok")
            dialog.present() 