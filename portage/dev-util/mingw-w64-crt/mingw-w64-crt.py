import info
from shells import *

class subinfo( info.infoclass ):
    def setTargets( self ):
        self.svnTargets['svnHEAD'] = 'https://mingw-w64.svn.sourceforge.net/svnroot/mingw-w64/trunk/mingw-w64-crt'
  
        self.defaultTarget = 'svnHEAD'

    def setDependencies( self ):
        self.buildDependencies['dev-util/msys'] = 'default'
        self.dependencies['dev-util/mingw-w64-headers'] = 'default'


from Package.AutoToolsPackageBase import *

class Package( AutoToolsPackageBase ):
    def __init__( self ):
        self.subinfo = subinfo()
        AutoToolsPackageBase.__init__( self )
        if compiler.isX64():
            disable = "--disable-lib32"
            self.subinfo.options.merge.destinationPath = 'mingw64/x86_64-w64-mingw32'
        else:
            disable = "--disable-lib64"
            self.subinfo.options.merge.destinationPath = 'mingw/i686-w64-mingw32'
        self.subinfo.options.configure.defines = " --with-sysroot=%s  %s " % (MSysShell().toNativePath(self.mergeDestinationDir()),disable)

    def install( self ):
        if not AutoToolsPackageBase.install( self ):
            return False
        if compiler.isX64():
            shutil.move( os.path.join( self.installDir() , "lib64" ) , os.path.join( self.installDir(), "lib" ) )
        return True

if __name__ == '__main__':
     Package().execute()
