import base
import info

SRC_URI = "http://subversion.tigris.org/files/documents/15/41094/svn-win32-1.4.6.zip"

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['1.4.6'] = SRC_URI
        self.targetInstSrc['1.4.6'] = "svn-win32-1.4.6"
        self.defaultTarget = '1.4.6'
    
    def setDependencies( self ):
        self.hardDependencies['gnuwin32/wget'] = 'default'
    
class subclass(base.baseclass):
  def __init__(self):
    base.baseclass.__init__( self, SRC_URI )
    if self.traditional:
        self.instdestdir = "subversion"
    self.subinfo = subinfo()

if __name__ == '__main__':
    subclass().execute()
