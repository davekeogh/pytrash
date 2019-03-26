#!/usr/bin/env python
# A little script to use in conjunction with trash.desktop to display
# trash fullness in any menu, dock or whatever in any desktop environment

# This makes use of trash-empty from the trash-cli package


import os, os.path, time, threading
from configparser import ConfigParser

from xdg import BaseDirectory


TRASH_DIR = os.path.join(BaseDirectory.xdg_data_home, 'Trash')
DESKTOP_FILE = os.path.join(BaseDirectory.xdg_data_home, 'applications', 'trash.desktop')

ICON_FULL = 'user-trash-full'
ICON_EMPTY = 'user-trash'

EMPTY_COMMAND = 'trash-empty'


def worker():
    desktop_file = ConfigParser()
    desktop_file.optionxform = str 
    desktop_file.read(DESKTOP_FILE)

    items = os.listdir(TRASH_DIR + '/files')

    if len(items) == 1:
        desktop_file.set('Desktop Entry', 'Icon', ICON_FULL)
        desktop_file.set('Desktop Entry', 'Name', 'Trash - 1 item')
    elif len(items) > 1:
        desktop_file.set('Desktop Entry', 'Icon', ICON_FULL)
        desktop_file.set('Desktop Entry', 'Name', 'Trash - %s items' % len(items))
    else:
        desktop_file.set('Desktop Entry', 'Icon', ICON_EMPTY)
        desktop_file.set('Desktop Entry', 'Name', 'Trash')
    
    with open(DESKTOP_FILE, 'w') as f:
        desktop_file.write(f)


if __name__ == '__main__':
    if not os.path.isfile(DESKTOP_FILE):
        # TODO: Install the desktop file
        pass

    while (True):
        t = threading.Thread(target=worker)
        t.start()
        t.join()

        time.sleep(1)

