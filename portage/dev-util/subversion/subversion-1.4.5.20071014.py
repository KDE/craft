import base
import info

SRC_URI = "http://subversion.tigris.org/downloads/1.4.5-win32/apache-2.0/svn-win32-1.4.5.zip"

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['1.4.5'] = SRC_URI
        self.targetInstSrc['1.4.5'] = "svn-win32-1.4.5"
        self.defaultTarget = '1.4.5'
    
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
