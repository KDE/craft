import os
import subprocess
import ctypes
import EmergeConfig

from Notifier.NotificationInterface import *


class Snore(NotificationInterface):
    def __init__(self):
        NotificationInterface.__init__(self,"Snore")
        
    def notify(self,title,message,alertClass):
        path = os.path.dirname(os.path.realpath(__file__))
        icon = os.path.join(path, "..", "kde-logo.png" )
        wid = ctypes.windll.kernel32.GetConsoleWindow()
        try:
            subprocess.Popen( """snoresend -t "%s" -m "%s" -i "%s" -a "Emerge" -c "%s" --silent --bring-window-to-front %s""" % (title , message , icon, alertClass, wid),
                              cwd = EmergeConfig.EmergeStandardDirs.emergeRoot())# make sure that nothing is spawned in a build dir
        except Exception:
            return

