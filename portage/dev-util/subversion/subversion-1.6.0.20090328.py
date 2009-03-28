import base
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['1.4.6'] = "http://subversion.tigris.org/files/documents/15/41094/svn-win32-1.4.6.zip"
        self.targets['1.5.5'] = "http://subversion.tigris.org/files/documents/15/44589/svn-win32-1.5.5.zip"
        self.targets['1.6.0'] = "http://subversion.tigris.org/files/documents/15/45344/svn-win32-1.6.0.zip"
        self.targetInstSrc['1.4.6'] = "svn-win32-1.4.6"
        self.targetInstSrc['1.5.5'] = "svn-win32-1.5.5"
        self.targetInstSrc['1.6.0'] = "svn-win32-1.6.0"
        self.defaultTarget = '1.6.0'

    def setDependencies( self ):
        self.hardDependencies['gnuwin32/wget'] = 'default'

class subclass(base.baseclass):
  def __init__( self, **args ):
    base.baseclass.__init__( self, args=args )
    self.subinfo = subinfo()

if __name__ == '__main__':
    subclass().execute()
