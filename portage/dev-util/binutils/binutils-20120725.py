import info
from shells import *

class subinfo( info.infoclass ):
    def setTargets( self ):
        self.targets['svnHEAD'] = 'ftp://sourceware.org/pub/binutils/snapshots/binutils-2.22.52.tar.bz2'
        self.targetInstSrc['svnHEAD'] = 'binutils-2.22.52'
        self.targetDigests['svnHEAD'] = 'ce5e58008e3e8be7c7e9fce03def27a3480ac28b'
        self.patchToApply[ 'svnHEAD' ] = [('binutils-2.22.52-20120726.diff',1)]
  
        self.defaultTarget = 'svnHEAD'

    def setDependencies( self ):
        self.buildDependencies['dev-util/msys'] = 'default'


from Package.AutoToolsPackageBase import *

class Package( AutoToolsPackageBase ):
    def __init__( self ):
        self.subinfo = subinfo()
        AutoToolsPackageBase.__init__( self )        
        self.subinfo.options.merge.destinationPath = 'mingw64'
        if os.getenv("EMERGE_ARCHITECTURE") == "x64":
            target = "x86_64-w64-mingw32"
        else:
            target = "i686-w64-mingw32"
        self.subinfo.options.configure.defines = " --with-sysroot=%s  --target=%s --build=%s --host=%s --disable-nls" % (MSysShell().toNativePath(self.mergeDestinationDir()),target,target,target)


if __name__ == '__main__':
     Package().execute()
