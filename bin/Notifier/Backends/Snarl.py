from Notifier.NotificationInterface import *
from Notifier.Libs.pysnp import *


class Snarl(NotificationInterface):
    def __init__(self):
        NotificationInterface.__init__(self,"Snarl")
        self.snp = PySNP()
        
    def notify(self,title,message,alertClass):     
        self.snp.register("craft", "craft",icon="http://winkde.org/~pvonreth/other/kde-logo.png")
        if alertClass == None:
            self.snp.notify("craft", title, message ,icon="http://winkde.org/~pvonreth/other/kde-logo.png")
        else:
            self.snp.addclass("craft", alertClass , alertClass)
            self.snp.notify("craft", title, message ,icon="http://winkde.org/~pvonreth/other/kde-logo.png",id=alertClass)
        
