import base
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['20080511'] = "http://www.winkde.org/pub/kde/ports/win32/repository/other/md5sums-20080511-bin.zip"
        self.defaultTarget = '20080511'
    
class subclass(base.baseclass):
  def __init__(self, **args ):
    base.baseclass.__init__( self, args=args )
    self.subinfo = subinfo()

if __name__ == '__main__':
    subclass().execute()
