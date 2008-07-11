import base
import info

SRC_URI = "http://subversion.tigris.org/files/documents/15/41094/svn-win32-1.4.6.zip"

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['1.4.6'] = SRC_URI
        self.targets['1.5.0'] = "http://subversion.tigris.org/files/documents/15/43074/svn-win32-1.5.0.zip"
        self.targetInstSrc['1.4.6'] = "svn-win32-1.4.6"
        self.targetInstSrc['1.5.0'] = "svn-win32-1.5.0"
        self.defaultTarget = '1.5.0'
    
    def setDependencies( self ):
        self.hardDependencies['gnuwin32/wget'] = 'default'
    
class subclass(base.baseclass):
  def __init__( self, **args ):
    base.baseclass.__init__( self, SRC_URI, args=args )
    if self.traditional:
        self.instdestdir = "subversion"
    self.subinfo = subinfo()

if __name__ == '__main__':
    subclass().execute()
