import json
import argparse
from . import DBusMediaPlayers


def main():
    parser = argparse.ArgumentParser(
        prog="dbus-mediaplayer",
        description="Controls Media Players from DBus")

    parser.add_argument(
        "command",
        nargs="?",
        default="get-info",
        choices=["get-info", "control"],
        help="Operation to perform (default: get-info)",
    )
    parser.add_argument(
        "--volume",
        type=float,
        help="Set volume level (0.0 to 1.0)",
    )
    parser.add_argument(
        "--position",
        type=int,
        help="Set media playback position in seconds",
    )
    parser.add_argument(
        "--action",
        choices=["Play", "Pause", "PlayPause", "Stop", "Next", "Previous"],
        help="Media control action",
    )
    args = parser.parse_args()

    players = DBusMediaPlayers(oneshot=True)
    if args.command == "get-info":
        print(json.dumps(players.players, indent=2))
    elif args.command == "control":
        if args.position is not None:
            players.control_setposition(args.position)
        if args.action is not None:
            players.control_media(args.action)
        if args.volume is not None:
            players.control_volume(args.volume)

