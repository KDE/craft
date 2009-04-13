import base
import info

SRC_URI = """
http://downloads.sourceforge.net/sourceforge/gnuwin32/diffutils-2.8.7-1-bin.zip
http://downloads.sourceforge.net/sourceforge/gnuwin32/diffutils-2.8.7-1-dep.zip
"""

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['2.8.7-1'] = SRC_URI
        self.defaultTarget = '2.8.7-1'
    
    def setDependencies( self ):
        self.hardDependencies['gnuwin32/wget'] = 'default'
    
class subclass(base.baseclass):
  def __init__( self, **args ):
    base.baseclass.__init__( self, args=args )
    self.subinfo = subinfo()

if __name__ == '__main__':
    subclass().execute()
