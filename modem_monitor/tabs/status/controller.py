from modem_monitor.services.modem import ModemService

class StatusTabController:
    def __init__(self, view, window):
        self.view = view
        self.window = window
        self.modem_service = ModemService(window.auth_service)
    
    def on_refresh_clicked(self, button):
        self.refresh_modem_status()
    
    def refresh_modem_status(self):
        self.modem_service.fetch_modem_status(self.window)
    
    def update_status_ui_with_data(self, data):
        # Update modem information
        if 'modem' in data:
            self.view.modem_row.set_subtitle(data['modem'])
        
        if 'imei' in data:
            self.view.imei_row.set_subtitle(data['imei'])
        
        if 'proto' in data:
            self.view.protocol_row.set_subtitle(data['proto'])
        
        # Update provider information
        if 'cops' in data:
            self.view.provider_row.set_subtitle(data['cops'])
        
        if 'phone' in data:
            self.view.phone_row.set_subtitle(data['phone'])
        
        # Update connection status
        if 'mode' in data:
            self.view.mode_row.set_subtitle(data['mode'])
        
        if 'lband' in data:
            # Clean up HTML tags in the band information
            band_info = data['lband'].replace('<br />', ' | ')
            self.view.bands_row.set_subtitle(band_info)
        
        # Update signal information
        if 'per' in data:
            percentage = data['per']
            self.view.signal_row.set_subtitle(percentage)
            
            # Update progress bar
            try:
                # Convert "83%" to 0.83
                fraction = float(percentage.strip('%')) / 100
                self.view.signal_progress.set_fraction(fraction)
            except (ValueError, AttributeError):
                self.view.signal_progress.set_fraction(0)
        
        if 'csq' in data:
            self.view.csq_row.set_subtitle(data['csq'])
        
        if 'rssi' in data:
            self.view.rssi_row.set_subtitle(data['rssi'])
            
            # Update signal quality indicator
            try:
                # Extract dBm value
                rssi_value = int(data['rssi'].split()[0])
                
                # Remove all existing classes except 'circular'
                self.view.rssi_indicator.remove_css_class("success")
                self.view.rssi_indicator.remove_css_class("warning")
                self.view.rssi_indicator.remove_css_class("error")
                
                # Add appropriate class based on signal strength
                if rssi_value > -70:  # Good signal
                    self.view.rssi_indicator.add_css_class("success")
                elif rssi_value > -85:  # Medium signal
                    self.view.rssi_indicator.add_css_class("warning")
                else:  # Poor signal
                    self.view.rssi_indicator.add_css_class("error")
            except (ValueError, IndexError):
                # Default to warning if we can't parse
                self.view.rssi_indicator.add_css_class("warning")
        
        if 'rscp' in data:
            # Clean up HTML tags
            rsrp_info = data['rscp'].replace('<br />', ' | ')
            self.view.rsrp_row.set_subtitle(rsrp_info)
        
        if 'ecio' in data:
            # Clean up HTML tags
            rsrq_info = data['ecio'].replace('<br />', ' | ')
            self.view.rsrq_row.set_subtitle(rsrq_info)
        
        if 'sinr' in data:
            # Clean up HTML tags
            sinr_info = data['sinr'].replace('<br />', ' | ')
            self.view.sinr_row.set_subtitle(sinr_info)
            
            # Update SINR quality indicator
            try:
                # Extract first dB value
                sinr_value = int(data['sinr'].split()[0])
                
                # Remove all existing classes except 'circular'
                self.view.sinr_indicator.remove_css_class("success")
                self.view.sinr_indicator.remove_css_class("warning")
                self.view.sinr_indicator.remove_css_class("error")
                
                # Add appropriate class based on SINR
                if sinr_value > 20:  # Excellent
                    self.view.sinr_indicator.add_css_class("success")
                elif sinr_value > 10:  # Good
                    self.view.sinr_indicator.add_css_class("warning")
                else:  # Poor
                    self.view.sinr_indicator.add_css_class("error")
            except (ValueError, IndexError):
                # Default to warning if we can't parse
                self.view.sinr_indicator.add_css_class("warning")
        
        # Show success toast
        self.window.show_toast("Modem status updated successfully") 