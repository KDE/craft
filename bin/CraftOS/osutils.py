import os

if os.name == 'nt':
    from CraftOS.win.osutils import OsUtils as OsUtils
else:
    from CraftOS.unix.osutils import OsUtils as OsUtils
