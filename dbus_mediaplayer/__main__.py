import json
import argparse
from . import DBusMediaPlayers


def main():
    parser = argparse.ArgumentParser(
        prog="dbus-mediaplayer",
        description="Gets a list of Media Players from DBus")
    args = parser.parse_args()

    players = DBusMediaPlayers(oneshot=True)
    print(json.dumps(players.players, indent=2))
