import os
import subprocess

from Notifier.NotificationInterface import *


class Snore(NotificationInterface):
    def __init__(self):
        NotificationInterface.__init__(self,"Snore")
        
    def notify(self,title,message,alertClass):
        path = os.path.dirname(os.path.realpath(__file__))
        icon = os.path.join(path, "..", "kde-logo.png" )
        try:
            subprocess.Popen( """snore-send -t "%s" -m "%s" -i "%s" -a "Emerge" -c "%s" --silent -b Snore""" % (title , message , icon, alertClass))
        except Exception:
            return

