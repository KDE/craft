import os

if os.name == 'nt':
    from EmergeOS.win.osutils import OsUtils
else:
    from EmergeOS.unix.osutils import OsUtils
