#!/usr/bin/env python
# A little script to use in conjunction with trash.desktop to display
# trash fullness in any menu, dock or whatever in any desktop environment

# This makes use of trash-empty from the trash-cli package


import hashlib, os, os.path, time, threading
from configparser import ConfigParser

from xdg import BaseDirectory


TRASH_DIR = os.path.join(BaseDirectory.xdg_data_home, 'Trash')
DESKTOP_FILE = os.path.join(BaseDirectory.xdg_data_home, 'applications', 'trash.desktop')

ICON_FULL = 'user-trash-full'
ICON_EMPTY = 'user-trash'

EMPTY_COMMAND = 'trash-empty'

DEFAULT_DESKTOP_FILE = '''[Desktop Entry]
Version=1.1
Type=Application
Name=Trash
Comment=Where the rubbish goes
Icon=user-trash-full
Exec=xdg-open "trash://"
Actions=empty-trash;
Categories=
StartupNotify=false

[Desktop Action empty-trash]
Name=Empty Trash
Exec=trash-empty
'''

SHA256SUM_DESKTOP_FILE = '8b9e6c091826a85cdc544fe91ed6bdd5748c719611f026ea58d70a62d0f2f3e7'

def worker():
    desktop_file = ConfigParser()
    desktop_file.optionxform = str 
    desktop_file.read_file(DESKTOP_FILE)

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


def install_desktop_file():
    with open(DESKTOP_FILE, 'x') as f:
        f.write(DEFAULT_DESKTOP_FILE)


if __name__ == '__main__':
    if not os.path.isfile(DESKTOP_FILE):
        install_desktop_file()
    else:
        sha256 = hashlib.sha256()
        with open(DESKTOP_FILE, 'rb') as f:
            if not hashlib.sha256(f.read()) == SHA256SUM_DESKTOP_FILE:
                # The default (empty) desktop file should always be used on startup
                os.remove(DESKTOP_FILE)
                install_desktop_file()


    while (True):
        t = threading.Thread(target=worker)
        t.start()
        t.join()

        time.sleep(1)
