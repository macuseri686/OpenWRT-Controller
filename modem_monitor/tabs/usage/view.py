import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw

from modem_monitor.tabs.usage.controller import UsageTabController

class UsageTabView:
    def __init__(self, window):
        self.window = window
        self.controller = UsageTabController(self, window)
        
        # Create a scrolled window for the usage tab
        self.scroll = Gtk.ScrolledWindow()
        self.scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        self.scroll.set_vexpand(True)
        
        # Create a box for the usage content
        self.box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.box.set_margin_top(20)
        self.box.set_margin_bottom(20)
        self.box.set_margin_start(20)
        self.box.set_margin_end(20)
        self.scroll.set_child(self.box)
        
        # Add a title
        title = Gtk.Label()
        title.set_markup("<span size='x-large' weight='bold'>Data Usage</span>")
        title.set_halign(Gtk.Align.START)
        self.box.append(title)
        
        # Current session usage
        self.session_group = Adw.PreferencesGroup(title="Current Session")
        self.box.append(self.session_group)
        
        self.download_row = Adw.ActionRow(title="Downloaded")
        self.download_row.set_subtitle("-")
        self.session_group.add(self.download_row)
        
        self.upload_row = Adw.ActionRow(title="Uploaded")
        self.upload_row.set_subtitle("-")
        self.session_group.add(self.upload_row)
        
        self.total_row = Adw.ActionRow(title="Total")
        self.total_row.set_subtitle("-")
        self.session_group.add(self.total_row)
        
        # Data plan
        self.plan_group = Adw.PreferencesGroup(title="Data Plan")
        self.box.append(self.plan_group)
        
        self.plan_row = Adw.ActionRow(title="Plan")
        self.plan_row.set_subtitle("-")
        self.plan_group.add(self.plan_row)
        
        self.used_row = Adw.ActionRow(title="Used")
        self.used_row.set_subtitle("-")
        self.plan_group.add(self.used_row)
        
        self.remaining_row = Adw.ActionRow(title="Remaining")
        self.remaining_row.set_subtitle("-")
        self.plan_group.add(self.remaining_row)
        
        # Add usage progress bar
        self.usage_progress_row = Adw.ActionRow(title="Usage Percent")
        self.usage_progress_row.set_subtitle("0%")
        
        self.usage_progress = Gtk.ProgressBar()
        self.usage_progress.set_fraction(0)
        self.usage_progress.set_valign(Gtk.Align.CENTER)
        self.usage_progress.set_size_request(150, 10)
        self.usage_progress.add_css_class("accent")
        self.usage_progress_row.add_suffix(self.usage_progress)
        
        self.plan_group.add(self.usage_progress_row)
        
        self.days_row = Adw.ActionRow(title="Days Remaining")
        self.days_row.set_subtitle("-")
        self.plan_group.add(self.days_row)
        
        # Add days progress bar
        self.days_progress_row = Adw.ActionRow(title="Billing Cycle")
        self.days_progress_row.set_subtitle("0%")
        
        self.days_progress = Gtk.ProgressBar()
        self.days_progress.set_fraction(0)
        self.days_progress.set_valign(Gtk.Align.CENTER)
        self.days_progress.set_size_request(150, 10)
        self.days_progress.add_css_class("warning")
        self.days_progress_row.add_suffix(self.days_progress)
        
        self.plan_group.add(self.days_progress_row)
        
        # Device usage
        self.monthly_group = Adw.PreferencesGroup(title="Device Usage")
        self.monthly_group.set_description("Data usage by device")
        self.monthly_group.set_margin_top(10)
        self.box.append(self.monthly_group)
        
        # Add refresh button
        self.refresh_button = Gtk.Button(label="Refresh Usage Data")
        self.refresh_button.set_halign(Gtk.Align.START)
        self.refresh_button.set_margin_top(20)
        self.refresh_button.connect("clicked", self.controller.on_refresh_usage_clicked)
        self.box.append(self.refresh_button)
    
    def get_view(self):
        return self.scroll 

    def recreate_monthly_group(self):
        """Recreate the monthly group from scratch"""
        # Remove the old monthly group
        if hasattr(self, 'monthly_group'):
            self.box.remove(self.monthly_group)
        
        # Create a new monthly group
        self.monthly_group = Adw.PreferencesGroup(title="Device Usage")
        self.monthly_group.set_description("Data usage by device")
        self.monthly_group.set_margin_top(10)
        
        # Add it back to the box, before the refresh button
        self.box.insert_child_after(self.monthly_group, self.plan_group) 