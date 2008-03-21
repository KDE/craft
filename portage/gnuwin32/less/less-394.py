import gnuwin32
import info

SRC_URI = """
http://downloads.sf.net/sourceforge/gnuwin32/less-394-bin.zip
http://downloads.sf.net/sourceforge/gnuwin32/less-394-dep.zip
"""

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['394'] = SRC_URI
        self.defaultTarget = '394'
    
    def setDependencies( self ):
        self.hardDependencies['gnuwin32/wget'] = 'default'
    
class subclass(gnuwin32.gnuwin32class):
  def __init__(self):
    gnuwin32.gnuwin32class.__init__( self, SRC_URI )
    self.subinfo = subinfo()

if __name__ == '__main__':
    subclass().execute()
