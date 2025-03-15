import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw

from modem_monitor.tabs.connection.controller import ConnectionTabController

class ConnectionTabView:
    def __init__(self, window):
        self.window = window
        self.controller = ConnectionTabController(self, window)
        
        # Create a scrolled window for the connection tab
        self.scroll = Gtk.ScrolledWindow()
        self.scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        self.scroll.set_vexpand(True)
        
        # Create a box for the connection content
        self.box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.box.set_margin_top(20)
        self.box.set_margin_bottom(20)
        self.box.set_margin_start(20)
        self.box.set_margin_end(20)
        self.scroll.set_child(self.box)
        
        # Add a title
        title = Gtk.Label()
        title.set_markup("<span size='x-large' weight='bold'>Connection Settings</span>")
        title.set_halign(Gtk.Align.START)
        self.box.append(title)
        
        # APN Settings
        self.apn_group = Adw.PreferencesGroup(title="APN Settings")
        self.box.append(self.apn_group)
        
        self.apn_row = Adw.EntryRow(title="APN")
        self.apn_row.set_text("internet")
        self.apn_group.add(self.apn_row)
        
        self.username_row = Adw.EntryRow(title="Username")
        self.username_row.set_text("")
        self.apn_group.add(self.username_row)
        
        self.password_row = Adw.PasswordEntryRow(title="Password")
        self.password_row.set_text("")
        self.apn_group.add(self.password_row)
        
        # Network Settings
        self.network_group = Adw.PreferencesGroup(title="Network Settings")
        self.box.append(self.network_group)
        
        # Network mode dropdown
        self.mode_row = Adw.ComboRow(title="Network Mode")
        mode_model = Gtk.StringList()
        for mode in ["Automatic", "LTE Only", "5G Only", "LTE/5G"]:
            mode_model.append(mode)
        self.mode_row.set_model(mode_model)
        self.mode_row.set_selected(3)  # LTE/5G
        self.network_group.add(self.mode_row)
        
        # Roaming switch
        self.roaming_row = Adw.SwitchRow(title="Enable Roaming")
        self.roaming_row.set_subtitle("Allow connection to roaming networks")
        self.network_group.add(self.roaming_row)
        
        # Band selection
        self.band_row = Adw.ActionRow(title="Band Selection")
        self.band_row.set_subtitle("Configure preferred network bands")
        self.band_button = Gtk.Button(label="Configure")
        self.band_button.connect("clicked", self.controller.on_band_configure_clicked)
        self.band_row.add_suffix(self.band_button)
        self.network_group.add(self.band_row)
        
        # Save button
        self.save_button = Gtk.Button(label="Save Settings")
        self.save_button.set_halign(Gtk.Align.CENTER)
        self.save_button.set_margin_top(20)
        self.save_button.add_css_class("suggested-action")
        self.save_button.connect("clicked", self.controller.on_save_clicked)
        self.box.append(self.save_button)
    
    def get_view(self):
        return self.scroll 