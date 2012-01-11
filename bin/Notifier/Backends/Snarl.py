import os
from Notifier.NotificationInterface import *
from Notifier.Libs.pysnp import *


class Snarl(NotificationInterface):
    def __init__(self):
        NotificationInterface.__init__(self,"Snarl")
        self.snp = PySNP()
        
    def notify(self,title,message):     
        self.snp.register("emerge", "emerge")
        self.snp.notify("emerge", title, message ,icon="http://upload.wikimedia.org/wikipedia/commons/thumb/8/8d/KDE_logo.svg/100px-KDE_logo.svg.png")
        
