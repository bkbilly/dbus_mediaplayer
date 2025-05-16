# DBus MediaPlayer

[![PyPI](https://img.shields.io/pypi/v/dbus-mediaplayer.svg)](https://pypi.python.org/pypi/dbus-mediaplayer)
![Python versions](https://img.shields.io/pypi/pyversions/dbus-mediaplayer.svg)
![License](https://img.shields.io/pypi/l/dbus-mediaplayer.svg)

The `dbus-mediaplayer` library empowers Python applications to interact with media players on your system through the D-Bus communication protocol. This enables you to retrieve metadata (like song titles and artists), control playback (play, pause, next, etc.), and potentially even access features specific to certain media players.


## Key Features

* **Media Player Discovery:** Enumerate available media players on your system.
* **Metadata Access:** Retrieve current song information (title, artist, album, etc.).
* **Playback Control:** Play, Pause, Skip tracks, Volume, Position.
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


### Command-Line Interaction (Optional)

If you prefer a quick way to view information or control playback, you can potentially execute the dbus-mediaplayer script directly. For more extensive programmatic control, I would recommend using the library within your Python code.
The script supports the following optional arguments for media control:

#### Status (Default):
If no argument is provided, the script defaults to retrieving media player information.
```bash
dbus-mediaplayer get-info
```

#### Volume Control:
You can set the volume level (between 0.0 and 1.0).
```bash
dbus-mediaplayer control --volume 0.5   # Sets volume to 50%
```

#### Set Media Position:
Adjust the playback position in seconds.
```bash
dbus-mediaplayer control --position 120  # Sets position to 2 minutes
```

#### Playback Control:
Perform media control actions: Play, Pause, PlayPause, Stop, Next, Previous.
``` bash
dbus-mediaplayer command Pause  # Pauses playback
dbus-mediaplayer command Play   # Plays playback
```

This flexible command-line approach offers a straightforward way to control media playback directly from the terminal.


## Inspiration
This library was inspired by the MPRIS2 library, which utilizes the `dbus-python` library. However, `dbus-mediaplayer` aims to offer a more widely deployable solution, removing reliance on external dependencies.
