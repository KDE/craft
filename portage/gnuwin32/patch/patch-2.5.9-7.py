import gnuwin32
import info

SRC_URI = """
http://heanet.dl.sourceforge.net/sourceforge/gnuwin32/patch-2.5.9-7-bin.zip
"""

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['2.5.9'] = SRC_URI
        self.defaultTarget = '2.5.9'
    
    def setDependencies( self ):
        self.hardDependencies['gnuwin32/wget'] = 'default'

class subclass(gnuwin32.gnuwin32class):
  def __init__(self):
    gnuwin32.gnuwin32class.__init__( self, SRC_URI )
    self.subinfo = subinfo()

if __name__ == '__main__':
    subclass().execute()
