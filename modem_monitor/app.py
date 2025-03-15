import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Adw

from modem_monitor.window import OpenWRTModemControllerWindow

class OpenWRTModemControllerApp(Adw.Application):
    def __init__(self, **kwargs):
        super().__init__(
            application_id="com.example.openwrtmodemcontroller",
            **kwargs
        )
        self.connect('activate', self.on_activate)

    def on_activate(self, app):
        self.win = OpenWRTModemControllerWindow(application=app)
        self.win.present() 