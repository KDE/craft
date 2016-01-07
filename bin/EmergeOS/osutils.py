import os

if os.name == 'nt':
    from EmergeOS.win.osutils import OsUtils
else:
    from EmergeOs.unix.osutils import OSUtils