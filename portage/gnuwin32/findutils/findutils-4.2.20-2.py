import base
import info

SRC_URI = """
http://www.winkde.org/pub/kde/ports/win32/repository/gnuwin32/findutils-4.2.20-2-bin.zip
"""

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['4.2.20-2'] = SRC_URI
        self.defaultTarget = '4.2.20-2'
        
class subclass(base.baseclass):
  def __init__( self, **args ):
    base.baseclass.__init__( self, args=args )
    self.subinfo = subinfo()

if __name__ == '__main__':
    subclass().execute()
