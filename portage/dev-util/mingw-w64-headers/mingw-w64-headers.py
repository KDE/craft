import info
from shells import *

class subinfo( info.infoclass ):
    def setTargets( self ):
        self.svnTargets['svnHEAD'] = 'https://mingw-w64.svn.sourceforge.net/svnroot/mingw-w64/trunk/mingw-w64-headers'
  
        self.defaultTarget = 'svnHEAD'

    def setDependencies( self ):
        self.buildDependencies['dev-util/msys'] = 'default'


from Package.AutoToolsPackageBase import *

class Package( AutoToolsPackageBase ):
    def __init__( self ):
        AutoToolsPackageBase.__init__( self )
        if compiler.isX64():
            self.subinfo.options.merge.destinationPath = 'mingw64/x86_64-w64-mingw32'
        else:
            self.subinfo.options.merge.destinationPath = 'mingw/i686-w64-mingw32'
        self.subinfo.options.configure.defines = " --enable-sdk=all "


if __name__ == '__main__':
     Package().execute()
