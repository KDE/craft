import os
import subprocess
import ctypes

from Notifier.NotificationInterface import *


class Snore(NotificationInterface):
    def __init__(self):
        NotificationInterface.__init__(self,"Snore")
        
    def notify(self,title,message,alertClass):
        path = os.path.dirname(os.path.realpath(__file__))
        icon = os.path.join(path, "..", "kde-logo.png" )
        wid = ctypes.windll.kernel32.GetConsoleWindow()
        try:
            subprocess.Popen( """snore-send -t "%s" -m "%s" -i "%s" -a "Emerge" -c "%s" --silent --bring-window-to-front %s""" % (title , message , icon, alertClass, wid))
        except Exception as e:
            print(e)
            return

