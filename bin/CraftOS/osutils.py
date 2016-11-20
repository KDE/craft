import os

if os.name == 'nt':
    from CraftOS.win.osutils import OsUtils
else:
    from CraftOS.unix.osutils import OsUtils
