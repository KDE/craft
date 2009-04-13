import base
import info

SRC_URI = """
http://downloads.sourceforge.net/sourceforge/gnuwin32/grep-%s-bin.zip
http://downloads.sourceforge.net/sourceforge/gnuwin32/grep-%s-dep.zip
"""

class subinfo(info.infoclass):
    def setTargets( self ):
        for t in ( '2.5.1a', '2.5.4' ):
          self.targets[ t ] = SRC_URI % ( t, t )
        self.defaultTarget = '2.5.4'
    
    def setDependencies( self ):
        self.hardDependencies['gnuwin32/wget'] = 'default'
    
class subclass(base.baseclass):
  def __init__( self, **args ):
    base.baseclass.__init__( self, args=args )
    self.subinfo = subinfo()

if __name__ == '__main__':
    subclass().execute()
