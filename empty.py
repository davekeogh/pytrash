#!/usr/bin/env python
# A little script to use in conjunction with trash.desktop to display
# trash fullness in any menu, dock or whatever in any desktop environment

# This makes use of trash-empty from the trash-cli package


import os, os.path, subprocess

from xdg import BaseDirectory


TRASH_DIR = os.path.join(BaseDirectory.xdg_data_home, 'Trash')


def empty():
    try:
        subprocess.Popen('trash-empty').run()
    except FileNotFoundError:
        fallback_empty()
        
    

def fallback_empty():
    # TODO: If trash-cli isn't installed we have to do something different
    # This is probably a dumb way to delete everything and will probably miss
    # any mounted volumes' trash
    
    for item in os.listdir(TRASH_DIR):
        try:
            os.remove(item)
        except OSError:
            os.rmdir(item)
