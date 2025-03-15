import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw, GLib
from modem_monitor.services.usage import UsageService
from modem_monitor.utils.formatters import DataFormatter

class UsageTabController:
    def __init__(self, view, window):
        self.view = view
        self.window = window
        self.usage_service = UsageService(window.auth_service)
        self.formatter = DataFormatter()
        
        # Schedule initial data fetch after a short delay to ensure UI is ready
        GLib.timeout_add(500, self.refresh_usage_data)
        
        # Connect to tab selection signal if possible
        try:
            window.stack.connect("notify::visible-child", self.on_tab_selected)
        except Exception as e:
            print(f"Could not connect to tab selection signal: {e}")
    
    def on_refresh_usage_clicked(self, button):
        self.refresh_usage_data()
    
    def refresh_usage_data(self):
        # Always reload settings before refreshing data
        if hasattr(self.window, 'settings_service'):
            self.window.settings_service.reload_settings()
        
        # Recreate the monthly group to ensure it's completely fresh
        self.view.recreate_monthly_group()
        
        # Now fetch the usage data
        self.usage_service.fetch_usage_data(self.window)
        return False
    
    def update_usage_ui_with_data(self, data):
        # No need to clear device rows since we recreated the group
        
        # Update current session usage
        if 'totaldown' in data:
            # Convert bytes to human-readable format
            download_bytes = int(data['totaldown'])
            download_str = self.formatter.format_bytes(download_bytes)
            self.view.download_row.set_subtitle(download_str)
        
        if 'totalup' in data:
            # Convert bytes to human-readable format
            upload_bytes = int(data['totalup'])
            upload_str = self.formatter.format_bytes(upload_bytes)
            self.view.upload_row.set_subtitle(upload_str)
        
        if 'total' in data:
            # Convert bytes to human-readable format
            total_bytes = int(data['total'])
            total_str = self.formatter.format_bytes(total_bytes)
            self.view.total_row.set_subtitle(total_str)
        
        # Update device usage
        if 'maclist' in data and data['maclist']:
            # Add device rows
            device_count = 0
            total_device_usage = 0
            device_usages = []
            
            # First pass to calculate total usage and collect data
            for device_id, device_info in data['maclist'].items():
                try:
                    # Parse device info (format: "IP|MAC|DOWN|UP|TOTAL|NAME")
                    parts = device_info.split('|')
                    if len(parts) >= 6:
                        total = parts[4]
                        # Extract numeric value (e.g., "1.23 GB" -> 1.23)
                        usage_value = self.formatter.parse_data_size(total)
                        if usage_value:
                            total_device_usage += usage_value
                            device_usages.append((device_id, device_info, usage_value))
                except Exception as e:
                    print(f"Error parsing device info: {e}")
            
            # Second pass to create UI with proportional progress bars
            for device_id, device_info, usage_value in sorted(device_usages, key=lambda x: x[2], reverse=True):
                try:
                    # Parse device info again
                    parts = device_info.split('|')
                    ip = parts[0]
                    mac = parts[1]
                    down = parts[2]
                    up = parts[3]
                    total = parts[4]
                    name = parts[5]
                    
                    # Create a row for this device
                    device_row = Adw.ActionRow(title=name)
                    device_row.set_subtitle(f"IP: {ip} • Down: {down} • Up: {up}")
                    
                    # Add usage as suffix
                    usage_label = Gtk.Label(label=total)
                    usage_label.add_css_class("numeric")
                    usage_label.add_css_class("caption")
                    usage_label.set_margin_end(10)
                    device_row.add_suffix(usage_label)
                    
                    # Add a progress bar to show relative usage
                    if total_device_usage > 0:
                        device_progress = Gtk.ProgressBar()
                        device_progress.set_fraction(usage_value / total_device_usage)
                        device_progress.set_valign(Gtk.Align.CENTER)
                        device_progress.set_size_request(100, 8)
                        device_progress.add_css_class("accent")
                        device_row.add_suffix(device_progress)
                    
                    # Add directly to the preferences group
                    self.view.monthly_group.add(device_row)
                    device_count += 1
                except Exception as e:
                    print(f"Error creating device row: {e}")
            
            # Only add the empty message if no devices were added
            if device_count == 0:
                # For empty message, we need to use a row instead of a plain label
                empty_row = Adw.ActionRow()
                empty_row.set_title("No device usage data available")
                empty_row.add_css_class("dim-label")
                self.view.monthly_group.add(empty_row)
        
        # Update data plan information
        settings = self.window.settings_service.get_app_settings()
        unlimited_plan = settings.get('unlimited_plan', False)
        data_plan_amount = settings.get('data_plan_amount', 1000)
        
        if unlimited_plan:
            self.view.plan_row.set_subtitle("Unlimited")
            # Hide or reset progress bars for unlimited plans
            self.view.usage_progress.set_fraction(0)
            self.view.usage_progress_row.set_subtitle("N/A")
            self.view.remaining_row.set_subtitle("Unlimited")
        else:
            # Format the data plan amount
            plan_total_str = f"{data_plan_amount:.2f} GB"
            self.view.plan_row.set_subtitle(plan_total_str)
            
            if 'ctotal' in data:
                self.view.used_row.set_subtitle(data['ctotal'])
                
                # Try to calculate remaining data
                try:
                    # Parse values to get numeric value
                    plan_total = data_plan_amount  # Already in GB
                    current_total = self.formatter.parse_data_size(data['ctotal'])
                    
                    if current_total is not None:
                        remaining = plan_total - current_total
                        remaining_str = self.formatter.format_bytes(remaining * 1024 * 1024 * 1024)  # Convert GB to bytes
                        self.view.remaining_row.set_subtitle(remaining_str)
                        
                        # Update usage progress bar
                        usage_percentage = min(current_total / plan_total, 1.0) if plan_total > 0 else 0
                        self.view.usage_progress.set_fraction(usage_percentage)
                        self.view.usage_progress_row.set_subtitle(f"{usage_percentage:.1%}")
                        
                        # Change color based on usage
                        self.view.usage_progress.remove_css_class("accent")
                        self.view.usage_progress.remove_css_class("success")
                        self.view.usage_progress.remove_css_class("warning")
                        self.view.usage_progress.remove_css_class("error")
                        
                        if usage_percentage < 0.7:
                            self.view.usage_progress.add_css_class("success")
                        elif usage_percentage < 0.9:
                            self.view.usage_progress.add_css_class("warning")
                        else:
                            self.view.usage_progress.add_css_class("error")
                except Exception as e:
                    print(f"Error calculating remaining data: {e}")
                    self.view.remaining_row.set_subtitle("Calculation error")
        
        if 'days' in data:
            days_text = f"{data['days']} days"
            self.view.days_row.set_subtitle(days_text)
            
            # Update days progress bar
            try:
                # Assuming a 30-day billing cycle
                days_remaining = int(data['days'])
                days_percentage = min(1.0 - (days_remaining / 30.0), 1.0) if days_remaining >= 0 else 0
                self.view.days_progress.set_fraction(days_percentage)
                self.view.days_progress_row.set_subtitle(f"{days_percentage:.1%}")
            except (ValueError, TypeError):
                self.view.days_progress.set_fraction(0)
                self.view.days_progress_row.set_subtitle("0%")
        
        # Show success toast
        self.window.show_toast("Usage data updated successfully")
    
    def on_tab_selected(self, stack, param):
        """Called when a tab is selected"""
        if stack.get_visible_child_name() == "usage":
            # Save current scroll position
            adjustment = self.view.scroll.get_vadjustment()
            current_position = adjustment.get_value()
            
            # Refresh data when the usage tab is selected
            self.refresh_usage_data()
            
            # Restore scroll position after a short delay to allow UI to update
            GLib.timeout_add(100, self.restore_scroll_position, current_position)
    
    def restore_scroll_position(self, position):
        """Restore the scroll position"""
        adjustment = self.view.scroll.get_vadjustment()
        adjustment.set_value(position)
        return False  # Don't repeat the timeout
    
    def clear_device_rows(self):
        """Clear all device rows from the monthly group"""
        # More aggressive approach to ensure all rows are removed
        try:
            # First, get a reference to the monthly group
            group = self.view.monthly_group
            
            # Get all children
            children = []
            child = group.get_first_child()
            while child:
                # Check if it's a row we want to remove
                if isinstance(child, Adw.ActionRow):
                    children.append(child)
                child = child.get_next_sibling()
            
            # Now remove all the collected rows
            for child in children:
                group.remove(child)
            
            # Debug output
            print(f"Cleared {len(children)} device rows")
        except Exception as e:
            print(f"Error clearing device rows: {e}") 