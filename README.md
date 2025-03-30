# DBus MediaPlayer

[![PyPI](https://img.shields.io/pypi/v/dbus-mediaplayer.svg)](https://pypi.python.org/pypi/dbus-mediaplayer)
![Python versions](https://img.shields.io/pypi/pyversions/dbus-mediaplayer.svg)
![License](https://img.shields.io/pypi/l/dbus-mediaplayer.svg)

The `dbus-mediaplayer` library empowers Python applications to interact with media players on your system through the D-Bus communication protocol. This enables you to retrieve metadata (like song titles and artists), control playback (play, pause, next, etc.), and potentially even access features specific to certain media players.

## Key Features

* **Media Player Discovery:** Enumerate available media players on your system.
* **Metadata Access:** Retrieve current song information (title, artist, album, etc.).
* **Playback Control:** Play, pause, skip tracks.
* **Real-time Updates:** Utilizes callback functions to provide instant notifications of media player state changes, ensuring your application stays up-to-date.

## Requirements

* Python 3.7 or later
* `jeepney` library

## Installation

Install the library using pip:

```bash
pip install dbus-mediaplayer
```

## Usage

This library offers two primary usage approaches:

### Command-Line Interaction (Optional)

If you prefer a quick way to view information or control playback, you can potentially execute the dbus-mediaplayer script directly. For more extensive programmatic control, I would recommend using the library within your Python code.

### Programmatic Control

Import the DBusMediaPlayers class from your Python code:

```python
from dbus_mediaplayer import DBusMediaPlayers

def callback(players):
    # Handle the list of media player objects here
    print(players)

# Create an instance of the class
media_player = DBusMediaPlayers(callback)

# Control media playback (replace "PlayPause" with desired methods like "Play", "Pause", "Next", etc.)
media_player.control_media("PlayPause")

# Keep the app running
while True:
    time.sleep(1)
```

## Inspiration
This library was inspired by the MPRIS2 library, which utilizes the `dbus-python` library. However, `dbus-mediaplayer` aims to offer a more widely deployable solution, removing reliance on external dependencies.

## Future Features
While dbus-mediaplayer provides a solid foundation for interacting with media players, there's room for growth. Here are some features it is missing and could be implemented in future development:

 * **Seek Position Control:** Allow users to set the playback position within a media track.
 * **Volume Control:** Implement methods for adjusting media player volume. Note that volume control support may vary across different media players and platforms.
 * **Playback Capabilities:** Provide methods to determine if a media player supports specific playback actions like next, previous, stop, and seek. This will allow users to tailor their interactions based on player capabilities.
