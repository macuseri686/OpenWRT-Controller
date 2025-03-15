#!/usr/bin/env python3

from modem_monitor.app import OpenWRTModemControllerApp

def main():
    app = OpenWRTModemControllerApp()
    return app.run(None)

if __name__ == "__main__":
    main() 