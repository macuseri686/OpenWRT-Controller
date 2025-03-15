import os
import json

class SettingsService:
    def __init__(self, auth_service):
        self.auth_service = auth_service
        self.settings_file = os.path.expanduser("~/.config/modem-monitor/settings.json")
        self.settings = self.load_settings_from_file()
    
    def save_connection_settings(self, apn, username, password, network_mode, roaming_enabled):
        # In a real implementation, this would make API calls to save the settings
        # For now, we'll just return success
        return True
    
    def save_app_settings(self, auto_refresh, refresh_interval, notifications_enabled, 
                         unlimited_plan, data_plan_amount):
        """Save application settings"""
        try:
            self.settings.update({
                'auto_refresh': auto_refresh,
                'refresh_interval': refresh_interval,
                'notifications_enabled': notifications_enabled,
                'unlimited_plan': unlimited_plan,
                'data_plan_amount': data_plan_amount
            })
            
            # Save settings to file
            self.save_settings_to_file()
            
            return True
        except Exception as e:
            print(f"Error saving settings: {e}")
            return False
    
    def get_app_settings(self):
        """Get application settings"""
        return self.settings
    
    def load_settings_from_file(self):
        """Load settings from file"""
        default_settings = {
            'auto_refresh': True,
            'refresh_interval': 30,
            'notifications_enabled': True,
            'unlimited_plan': False,
            'data_plan_amount': 1000  # Default to 1TB (1000 GB)
        }
        
        try:
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(self.settings_file), exist_ok=True)
            
            # Load settings from file if it exists
            if os.path.exists(self.settings_file):
                with open(self.settings_file, 'r') as f:
                    loaded_settings = json.load(f)
                    # Merge with defaults to ensure all keys exist
                    default_settings.update(loaded_settings)
        except Exception as e:
            print(f"Error loading settings from file: {e}")
        
        return default_settings
    
    def save_settings_to_file(self):
        """Save settings to file"""
        try:
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(self.settings_file), exist_ok=True)
            
            # Save settings to file
            with open(self.settings_file, 'w') as f:
                json.dump(self.settings, f, indent=2)
        except Exception as e:
            print(f"Error saving settings to file: {e}")
    
    def reload_settings(self):
        """Reload settings from file"""
        self.settings = self.load_settings_from_file()
        return self.settings 