import os
import subprocess
import ctypes
import EmergeConfig

from EmergeOS.osutils import OsUtils

from Notifier.NotificationInterface import *


class Snore(NotificationInterface):
    def __init__(self):
        NotificationInterface.__init__(self,"Snore")
        
    def notify(self,title,message,alertClass):
        path = os.path.dirname(os.path.realpath(__file__))
        icon = os.path.join(path, "..", "kde-logo.png" )
        try:
            command = """snoresend -t "%s" -m "%s" -i "%s" -a "Emerge" -c "%s" --silent """ % (title , message , icon, alertClass)
            if OsUtils.isWin():
                command += " --bring-window-to-front %s" % ctypes.windll.kernel32.GetConsoleWindow()
            subprocess.Popen( command,
                              shell = True,
                              cwd = EmergeConfig.EmergeStandardDirs.emergeRoot())# make sure that nothing is spawned in a build dir
        except Exception as e:
            return

