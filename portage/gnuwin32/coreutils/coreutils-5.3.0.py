import base
import info

SRC_URI = """
http://downloads.sourceforge.net/sourceforge/gnuwin32/coreutils-5.3.0-bin.zip
http://downloads.sourceforge.net/sourceforge/gnuwin32/coreutils-5.3.0-dep.zip
"""

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['5.3.0'] = SRC_URI
        self.defaultTarget = '5.3.0'
        
class subclass(base.baseclass):
  def __init__( self, **args ):
    base.baseclass.__init__( self, args=args )
    self.subinfo = subinfo()

if __name__ == '__main__':
    subclass().execute()
