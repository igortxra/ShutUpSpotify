"""
This script can be runned every time you open spotify; 
You can kill it when quit spotify;
I did not figure out how to do it yet;
PS.: This was the best i could do unitl now, I believe that alredy exists
better ways, but i wanted to give me a try first.
"""

import subprocess
import dbus
from dbus.mainloop.glib import DBusGMainLoop
from gi.repository import GLib

# Please, let this here in the beggining
DBusGMainLoop(set_as_default=True)


def get_volume():
    output = subprocess.run(['playerctl', 'volume'],
                            capture_output=True, text=True)
    return float(output.stdout.strip())


# Stores current volume; Scale is >= 0 <= 1.0
volume = 1.0


def handler_function(*args):
    """ Mute spotify when the ads starts and unmute when stops."""
    global volume
    try:

        # All ads has this metadata
        if str(args[1]["Metadata"]["xesam:title"]) == "Advertisement":

            # Get actual volume before mute it
            volume = get_volume()

            # Use Playerctl to mute spotify
            subprocess.run(["playerctl", "-p", "spotify", "volume", "0"])
        else:

            # Use Playerctl to unmute spotify
            subprocess.run(
                [f"playerctl", "-p", "spotify", "volume", f"{volume}"])
    except:
        # I just wanted to silence the ignorable errors with this try except
        pass


# When spotify is communicating with dbus, it uses this bus_name and this object path
# I discovered them running dbus-monitor while used play/pause/next in spotfiy GUI
bus_name = "org.freedesktop.DBus"
object_path = "/org/mpris/MediaPlayer2"

# Connect to SessionBus (Which spotify uses to communicate changes in its player)
session_bus = dbus.SessionBus()
session_bus.add_signal_receiver(
    handler_function,
    path=object_path,
)

# This loop is necessary to keep capturing dbus signals form spotfiy
loop = GLib.MainLoop()
loop.run()
