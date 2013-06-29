import os
from Notifier.NotificationInterface import *
import subprocess

#use https://github.com/nels-o/toaster to generate windows 8 toast notifications
class Toaster(NotificationInterface):
    def __init__(self):
        NotificationInterface.__init__(self,"Toaster")
        
    def notify(self,title,message,alertClass):
        path = os.path.dirname(os.path.realpath(__file__))
        subprocess.Popen( "%s\\..\Libs\\toaster\\toast.exe -t \"%s\" -m \"%s\" -p \"%s\\..\\kde-logo.png\"" % (path,  title , message ,path ),shell=True)
        
