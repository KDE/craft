import info
from shells import *

class subinfo( info.infoclass ):
    def setTargets( self ):
        self.svnTargets['svnHEAD'] = 'https://mingw-w64.svn.sourceforge.net/svnroot/mingw-w64/trunk/mingw-w64-tools/gendef'
  
        self.defaultTarget = 'svnHEAD'

    def setDependencies( self ):
        self.buildDependencies['dev-util/msys'] = 'default'


from Package.AutoToolsPackageBase import *

class Package( AutoToolsPackageBase ):
    def __init__( self ):
        self.subinfo = subinfo()
        AutoToolsPackageBase.__init__( self )


if __name__ == '__main__':
     Package().execute()
