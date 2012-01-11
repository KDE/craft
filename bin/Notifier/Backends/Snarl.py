import os
from Notifier.NotificationInterface import *
from Notifier.Libs.pysnp import *


class Snarl(NotificationInterface):
    def __init__(self):
        NotificationInterface.__init__(self,"Snarl")
        self.snp = PySNP()
        
    def notify(self,title,message):     
        self.snp.register("emerge", "emerge",icon="http://winkde.org/~pvonreth/other/kde-logo.png")
        self.snp.notify("emerge", title, message ,icon="http://winkde.org/~pvonreth/other/kde-logo.png")
        
