import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw

from modem_monitor.tabs.status.controller import StatusTabController

class StatusTabView:
    def __init__(self, window):
        self.window = window
        self.controller = StatusTabController(self, window)
        
        # Create a scrolled window for the status tab
        self.scroll = Gtk.ScrolledWindow()
        self.scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        self.scroll.set_vexpand(True)
        
        # Create a box for the status content
        self.box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.box.set_margin_top(20)
        self.box.set_margin_bottom(20)
        self.box.set_margin_start(20)
        self.box.set_margin_end(20)
        self.scroll.set_child(self.box)
        
        # Add a title
        title = Gtk.Label()
        title.set_markup("<span size='x-large' weight='bold'>Modem Status</span>")
        title.set_halign(Gtk.Align.START)
        self.box.append(title)
        
        # Modem Information Group
        self.modem_group = Adw.PreferencesGroup(title="Modem Information")
        self.box.append(self.modem_group)
        
        # Add modem model row
        self.modem_row = Adw.ActionRow(title="Modem")
        self.modem_row.set_subtitle("-")
        self.modem_group.add(self.modem_row)
        
        # Add IMEI row
        self.imei_row = Adw.ActionRow(title="Modem IMEI")
        self.imei_row.set_subtitle("-")
        self.modem_group.add(self.imei_row)
        
        # Add protocol row
        self.protocol_row = Adw.ActionRow(title="Protocol")
        self.protocol_row.set_subtitle("-")
        self.modem_group.add(self.protocol_row)
        
        # Provider Information Group
        self.provider_group = Adw.PreferencesGroup(title="Provider Information")
        self.box.append(self.provider_group)
        
        # Add provider row
        self.provider_row = Adw.ActionRow(title="Provider")
        self.provider_row.set_subtitle("-")
        self.provider_group.add(self.provider_row)
        
        # Add phone number row
        self.phone_row = Adw.ActionRow(title="SIM Phone Number")
        self.phone_row.set_subtitle("-")
        self.provider_group.add(self.phone_row)
        
        # Connection Status Group
        self.connection_group = Adw.PreferencesGroup(title="Connection Status")
        self.box.append(self.connection_group)
        
        # Add mode row
        self.mode_row = Adw.ActionRow(title="Mode")
        self.mode_row.set_subtitle("-")
        self.connection_group.add(self.mode_row)
        
        # Add bands row
        self.bands_row = Adw.ActionRow(title="Bands")
        self.bands_row.set_subtitle("-")
        self.connection_group.add(self.bands_row)
        
        # Signal Information Group
        self.signal_group = Adw.PreferencesGroup(title="Signal Information")
        self.box.append(self.signal_group)
        
        # Signal strength with progress bar
        self.signal_row = Adw.ActionRow(title="Signal Strength")
        self.signal_row.set_subtitle("-")
        
        self.signal_progress = Gtk.ProgressBar()
        self.signal_progress.set_fraction(0)  # Start empty
        self.signal_progress.set_valign(Gtk.Align.CENTER)
        self.signal_progress.set_size_request(100, 10)
        self.signal_progress.add_css_class("accent")
        self.signal_row.add_suffix(self.signal_progress)
        
        self.signal_group.add(self.signal_row)
        
        # CSQ row
        self.csq_row = Adw.ActionRow(title="CSQ")
        self.csq_row.set_subtitle("-")
        self.signal_group.add(self.csq_row)
        
        # RSSI row
        self.rssi_row = Adw.ActionRow(title="RSSI")
        self.rssi_row.set_subtitle("-")
        
        # Add a small colored indicator for signal quality
        self.rssi_indicator = Gtk.Box()
        self.rssi_indicator.set_size_request(16, 16)
        self.rssi_indicator.add_css_class("circular")
        self.rssi_indicator.add_css_class("warning")  # Default to warning
        self.rssi_indicator.set_margin_start(5)
        self.rssi_indicator.set_margin_end(5)
        self.rssi_row.add_suffix(self.rssi_indicator)
        
        self.signal_group.add(self.rssi_row)
        
        # RSRP row with multiple values
        self.rsrp_row = Adw.ActionRow(title="RSRP")
        self.rsrp_row.set_subtitle("-")
        self.signal_group.add(self.rsrp_row)
        
        # RSRQ row
        self.rsrq_row = Adw.ActionRow(title="RSRQ")
        self.rsrq_row.set_subtitle("-")
        self.signal_group.add(self.rsrq_row)
        
        # SINR row
        self.sinr_row = Adw.ActionRow(title="SINR")
        self.sinr_row.set_subtitle("-")
        
        # Add a small colored indicator for SINR quality
        self.sinr_indicator = Gtk.Box()
        self.sinr_indicator.set_size_request(16, 16)
        self.sinr_indicator.add_css_class("circular")
        self.sinr_indicator.add_css_class("warning")  # Default to warning
        self.sinr_indicator.set_margin_start(5)
        self.sinr_indicator.set_margin_end(5)
        self.sinr_row.add_suffix(self.sinr_indicator)
        
        self.signal_group.add(self.sinr_row)
        
        # Add refresh button
        self.refresh_button = Gtk.Button(label="Refresh")
        self.refresh_button.set_halign(Gtk.Align.START)
        self.refresh_button.set_margin_top(20)
        self.refresh_button.connect("clicked", self.controller.on_refresh_clicked)
        self.box.append(self.refresh_button)
    
    def get_view(self):
        return self.scroll 