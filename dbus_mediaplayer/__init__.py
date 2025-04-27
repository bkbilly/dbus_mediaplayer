import json
import time
import logging
import traceback
import threading
from jeepney import DBusAddress, MessageType, new_method_call
from jeepney.io.blocking import open_dbus_connection, Proxy


logger = logging.getLogger("dbus_mediaplayer")
logging.basicConfig(level=logging.ERROR)


class DBusMediaPlayers:
    """Connects to Session DBus to find the available media players, controlls them and sends the current playng media"""

    def __init__(self, callback=lambda a: None, oneshot=False):
        """The data is returned on the callback method"""
        self.callback = callback
        self.players = {}
        self.prev_send = None
        self.init_players()
        if oneshot:
            self.conn.receive()
            self.players = self.get_players()
        else:
            self.watch_changes()

    def init_players(self):
        self.conn =  open_dbus_connection(bus='SESSION')
            
        # Register our match rule with DBus
        dbus_addr = DBusAddress(
            object_path="/org/freedesktop/DBus",
            bus_name="org.freedesktop.DBus",
            interface="org.freedesktop.DBus",
        )

        add_match_msg = new_method_call(
            remote_obj=dbus_addr,
            method="AddMatch",
            signature="s",
            body=("type='signal',path='/org/mpris/MediaPlayer2'",)
        )
        self.conn.send(add_match_msg)

    def get_players(self):
        dbus_addr = DBusAddress(
            object_path="/org/freedesktop/DBus",
            bus_name="org.freedesktop.DBus",
            interface="org.freedesktop.DBus",
        )

        msg = new_method_call(remote_obj=dbus_addr, method="ListNames")
        reply = self.conn.send_and_get_reply(msg)
        players = []
        for service in reply.body[0]:
            if "MediaPlayer2" in service:
                media_addr = DBusAddress(
                    object_path="/org/mpris/MediaPlayer2",
                    bus_name=service,
                    interface="org.freedesktop.DBus.Properties"
                )

                get_prop_msg = new_method_call(
                    remote_obj=media_addr,
                    method="Get",
                    signature="ss",  # Two strings (interface, property)
                    body=(
                        "org.mpris.MediaPlayer2.Player",  # Interface
                        "PlaybackStatus"  # Property name
                    )
                )
                self.conn.send(get_prop_msg)
                reply = self.conn.receive()
                playback_status = reply.body[0][1]

                if playback_status != "Stopped":
                    get_prop_msg = new_method_call(
                        remote_obj=media_addr,
                        method="Get",
                        signature="ss",  # Two strings (interface, property)
                        body=(
                            "org.mpris.MediaPlayer2.Player",  # Interface
                            "Metadata"  # Property name
                        )
                    )
                    self.conn.send(get_prop_msg)
                    reply = self.conn.receive()
                    metadata = reply.body[0][1]
                    if isinstance(metadata, dict):
                        get_prop_msg = new_method_call(
                            remote_obj=media_addr,
                            method="Get",
                            signature="ss",  # Two strings (interface, property)
                            body=(
                                "org.mpris.MediaPlayer2.Player",  # Interface
                                "Position"  # Property name
                            )
                        )
                        self.conn.send(get_prop_msg)
                        reply = self.conn.receive()
                        try:
                            position = round(reply.body[0][1] / 1000 / 1000)
                        except:
                            position = 0
                        try:
                            duration = round(metadata.get("mpris:length", ["", 0])[1] / 1000 / 1000)
                        except:
                            duration = 0
                        players.append({
                            "dbus_uri": service,
                            "title": metadata.get("xesam:title", ["", ""])[1],
                            "artist": ", ".join(metadata.get("xesam:artist", ["", ""])[1]),
                            "album": metadata.get("xesam:album", ["", ""])[1],
                            "arturl": metadata.get("mpris:artUrl", ["", ""])[1],
                            "duration": duration,
                            "position": position,
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

    def watch_changes(self):
        """Subscribes to the DBus to get any change"""
        threading.Thread(target=self.watch_changes_bg, daemon=True).start()

    def watch_changes_bg(self):
        while True:
            msg = self.conn.receive()
            try:
                self.players = self.get_players()
                if self.players != self.prev_send:
                    self.callback(self.players)
                    self.prev_send = self.players
            except Exception as err:
                logger.error("DBus MediaPlayer: %s, %s", err, traceback.format_exc())

    def control_media(self, action, player=None):
        """Sends a custom message call for controlling the media"""
        if player is None:
            player = self.players[0]["dbus_uri"]

        msg = new_method_call(
            remote_obj=DBusAddress(
                object_path="/org/mpris/MediaPlayer2",
                bus_name=player,
                interface="org.mpris.MediaPlayer2.Player",
            ),
            method=action
        )
        self.conn.send(msg)


def mycallback(players):
    print(players)

if __name__ == "__main__":
    dbusplayer = DBusMediaPlayers(mycallback)
    while True:
        time.sleep(1.1)
        # dbusplayer.control_media("PlayPause")
