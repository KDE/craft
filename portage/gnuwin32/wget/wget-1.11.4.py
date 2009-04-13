import base
import info

SRC_URI = """
http://downloads.sourceforge.net/sourceforge/gnuwin32/wget-%s-bin.zip
http://downloads.sourceforge.net/sourceforge/gnuwin32/wget-%s-dep.zip
"""

class subinfo(info.infoclass):
    def setTargets( self ):
        for t in ( '1.10.1', '1.11.4' ):
          self.targets[ t ] = SRC_URI % ( t, t )
        self.defaultTarget = '1.11.4'
        
class subclass(base.baseclass):
  def __init__( self, **args ):
    base.baseclass.__init__( self, SRC_URI, args=args )
    self.instdestdir = "dev-utils"
    self.subinfo = subinfo()

if __name__ == '__main__':
    subclass().execute()
