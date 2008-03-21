import gnuwin32
import info

SRC_URI= """
http://downloads.sourceforge.net/kde-windows/gettext-tools-0.17-1-bin.zip
"""

DEPEND = """
dev-util/win32libs
"""

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['0.17-1'] = SRC_URI
        self.defaultTarget = '0.17-1'
    
class subclass(gnuwin32.gnuwin32class):
    def __init__(self):
        gnuwin32.gnuwin32class.__init__( self, SRC_URI )
        self.subinfo = subinfo()


#class subclass(base.baseclass):
#  def __init__(self):
#    base.baseclass.__init__( self, SRC_URI )
#    if self.traditional:
#        self.instdestdir = "win32libs"
#    else:
#        self.instdestdir = ""

if __name__ == '__main__':
    subclass().execute()
