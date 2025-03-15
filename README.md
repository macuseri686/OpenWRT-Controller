# OpenWRT Modem Controller

A GTK4/Adw application for monitoring and controlling cellular modems on OpenWRT devices.

## Overview

OpenWRT Modem Controller provides a graphical interface to manage and monitor modems connected to OpenWRT-based routers. The application allows you to view modem status, signal strength, connection settings, data usage, and perform common management tasks.

## Features

- Monitor modem connection status and signal strength
- Manage connection settings and profiles
- Track data usage statistics
- Configure router and modem settings
- Secure credential storage
- User-friendly tabbed interface
- Toast notifications for important events

![Screenshot from 2025-03-14 23-59-53](https://github.com/user-attachments/assets/bff80ecf-51ed-425f-8c7f-55fc5ad26292)
![Screenshot from 2025-03-15 00-00-10](https://github.com/user-attachments/assets/266c6da4-cf79-45fc-ba9b-c82827c508d2)
![Screenshot from 2025-03-15 00-00-22](https://github.com/user-attachments/assets/a3e487ed-93c7-4d6c-816c-01fddc4d4b3a)

## Installation

### Dependencies

- Python 3.x
- GTK 4.0
- libadwaita 1.0
- Secret Service API (for credential storage)

### Install from source

```
# Clone the repository
git clone https://github.com/yourusername/openwrt-modem-controller.git
cd openwrt-modem-controller

# Install dependencies from requirements.txt
pip install -r requirements.txt

# Install the package
pip install -e .
```

## Usage

### Running the application

After installation, you can run the application with:

```
modem-monitor
```

Or directly with Python:

```
python -m modem_monitor.main
```

### First-time setup

1. Launch the application
2. Go to the Settings tab
3. Enter your OpenWRT router credentials
4. Configure any additional settings as needed

## Development

### Project Structure

- `modem_monitor/` - Main package directory
  - `app.py` - Application entry point
  - `main.py` - CLI entry point
  - `window.py` - Main application window
  - `tabs/` - Different tab views
    - `status/` - Modem status and signal information
    - `connection/` - Connection management
    - `usage/` - Data usage tracking
    - `settings/` - Application settings
  - `services/` - Backend services
    - `auth.py` - Authentication service
    - `settings.py` - Settings management

### Building from Source

```
# Install development dependencies
pip install -e ".[dev]"
```

### Creating requirements.txt

To update the requirements.txt file:

```
pip freeze > requirements.txt
```

## License

[MIT License](LICENSE)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
