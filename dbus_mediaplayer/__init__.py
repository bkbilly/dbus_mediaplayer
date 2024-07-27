import time
import logging
import threading
import multiprocessing
from gi.repository import Gio
from dasbus.loop import EventLoop
from dasbus.connection import SessionMessageBus


logger = logging.getLogger("dbus_mediaplayer")
logging.basicConfig(level=logging.ERROR)


class DBusMediaPlayers:
    """Connects to Session DBus to find the available media players, controlls them and sends the current playng media"""

    def __init__(self, callback=lambda a: None, debounce=0):
        """The data is returned on the callback method"""
        self.callback = callback
        self.players = {}
        self.debounce = debounce
        self.debounce_proc = None
        self.prev_send = None
        self.bus = SessionMessageBus()
        self.players = self.get_players()
        self.send_changes()
        self.watch_changes()

    def get_players(self):
        """Find available media players and their metadata"""
        players = []
        for service in self.bus.proxy.ListNames():
            if 'MediaPlayer2' in service:
                proxy = self.bus.get_proxy(service, "/org/mpris/MediaPlayer2")
                playback_status = proxy.Get("org.mpris.MediaPlayer2.Player", "PlaybackStatus").get_string()
                if playback_status != "Stopped":
                    metadata = dict(proxy.Get("org.mpris.MediaPlayer2.Player", "Metadata"))
                    position = proxy.Get("org.mpris.MediaPlayer2.Player", "Position").get_int64()
                    players.append({
                        "dbus_uri": service,
                        "title": metadata.get("xesam:title"),
                        "artist": ", ".join(metadata.get("xesam:artist")),
                        "album": metadata.get("xesam:album"),
                        "arturl": metadata.get("mpris:artUrl"),
                        "duration": round(metadata.get("mpris:length", 0) / 1000 / 1000),
                        "position": round(position / 1000 / 1000),
                        "status": playback_status,
                    })

        # Order the players so that the most important to be first
        custom_order = {
            "Playing": 1,
            "Paused": 2,
            "Idle": 3,
        }
        players = sorted(players, key=lambda x: custom_order.get(x.get("status"), 100))
        return players

    def send_changes(self):
        """If new changes on players is found, it is sent to the callback"""
        if self.debounce is not None and self.debounce > 0:
            time.sleep(self.debounce)
        if self.players != self.prev_send:
            self.callback(self.players)
            self.prev_send = self.players

    def watch_changes(self):
        """Subscribes to the DBus to get any change"""
        watch_proxy = self.bus.get_proxy(
            service_name=None,
            object_path="/org/mpris/MediaPlayer2",
        )
        watch_proxy.PropertiesChanged.connect(self.dbus_callback)

        loop = EventLoop()
        threading.Thread(target=loop.run, daemon=True).start()

    def dbus_callback(self, iface, prop_changed, prop_invalidated):
        """Callback method of watch_changes"""
        if self.debounce is not None and self.debounce > 0:
            if self.debounce_proc is not None and self.debounce_proc.is_alive():
                self.debounce_proc.terminate()
            self.players = self.get_players()
            self.debounce_proc = multiprocessing.Process(target=self.send_changes, daemon=True)
            self.debounce_proc.start()
        else:
            self.players = self.get_players()
            self.send_changes()

    def control_media(self, action, player=None):
        """Sends a custom message call for controlling the media"""
        if player is None:
            player = self.players[0]["dbus_uri"]
        self.bus.connection.call(
            bus_name=player,
            object_path="/org/mpris/MediaPlayer2",
            interface_name="org.mpris.MediaPlayer2.Player",
            method_name=action,
            parameters=None,
            reply_type=None,
            flags=Gio.DBusCallFlags.NONE,
            timeout_msec=1,
            cancellable=None,
            callback=None,
            user_data=None,
        )
