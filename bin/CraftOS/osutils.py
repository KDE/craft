import os

if os.name == "nt":
    from CraftOS.OsUtilsBase import LockFileBase as LockFile  # noqa: F401
    from CraftOS.win.osutils import OsUtils as WinOsUtils  # noqa: F401
else:
    from CraftOS.unix.osutils import LockFile as LockFile  # noqa: F401
    from CraftOS.unix.osutils import OsUtils as UnixOsUtils  # noqa: F401

OsUtils: type["WinOsUtils"] | type["UnixOsUtils"]

if os.name == "nt":
    OsUtils = WinOsUtils
else:
    OsUtils = UnixOsUtils
