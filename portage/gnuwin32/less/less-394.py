import base
import info

SRC_URI = """
http://downloads.sourceforge.net/sourceforge/gnuwin32/less-394-bin.zip
http://downloads.sourceforge.net/sourceforge/gnuwin32/less-394-dep.zip
"""

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['394'] = SRC_URI
        self.defaultTarget = '394'
    
    def setDependencies( self ):
        self.hardDependencies['gnuwin32/wget'] = 'default'
    
class subclass(base.baseclass):
  def __init__( self, **args ):
    base.baseclass.__init__( self, args=args )
    self.subinfo = subinfo()

if __name__ == '__main__':
    subclass().execute()
