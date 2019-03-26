#!/usr/bin/env python
# A little script to use in conjunction with trash.desktop to display
# trash fullness in any menu, dock or whatever in any desktop environment

# This makes use of trash-empty from the trash-cli package


import shutil, os.path

from xdg import BaseDirectory


TRASH_DIR = os.path.join(BaseDirectory.xdg_data_home, 'Trash')


def fallback_empty():
    # TODO: If trash-cli isn't installed we have to do something different
    pass

