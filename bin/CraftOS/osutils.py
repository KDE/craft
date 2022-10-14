import os

if os.name == "nt":
    from CraftOS.OsUtilsBase import LockFileBase as LockFile
    from CraftOS.win.osutils import OsUtils as OsUtils
else:
    from CraftOS.unix.osutils import LockFile as LockFile
    from CraftOS.unix.osutils import OsUtils as OsUtils
