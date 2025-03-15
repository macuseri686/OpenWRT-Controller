class DataFormatter:
    @staticmethod
    def format_bytes(bytes_value):
        """Convert bytes to human-readable format"""
        if bytes_value < 1024:
            return f"{bytes_value} B"
        elif bytes_value < 1024 * 1024:
            return f"{bytes_value / 1024:.2f} KB"
        elif bytes_value < 1024 * 1024 * 1024:
            return f"{bytes_value / (1024 * 1024):.2f} MB"
        else:
            return f"{bytes_value / (1024 * 1024 * 1024):.2f} GB"
    
    @staticmethod
    def parse_data_size(size_str):
        """Parse a data size string like '1000.00 GB' to get the numeric value"""
        try:
            parts = size_str.split()
            if len(parts) == 2:
                value = float(parts[0])
                unit = parts[1].upper()
                
                # Convert to GB for consistency
                if unit == 'KB':
                    return value / (1024 * 1024)
                elif unit == 'MB':
                    return value / 1024
                elif unit == 'GB':
                    return value
                elif unit == 'TB':
                    return value * 1024
                
            return None
        except Exception:
            return None 