import os

if os.name == 'nt':
    from CraftOS.win.osutils import OsUtils as OsUtils
    from CraftOS.OsUtilsBase import LockFileBase as LockFile
else:
    from CraftOS.unix.osutils import OsUtils as OsUtils
    from CraftOS.unix.osutils import LockFile as LockFile
