import base
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['3.0.3'] = "http://www.winkde.org/pub/kde/ports/win32/repository/other/upx-3.0.3-bin.zip"
        self.defaultTarget = '3.0.3'
    
class subclass(base.baseclass):
  def __init__(self, **args):
    base.baseclass.__init__( self, args=args )
    self.subinfo = subinfo()

  def unpack(self):
    res = base.baseclass.unpack( self )
    return res

if __name__ == '__main__':
    subclass().execute()
