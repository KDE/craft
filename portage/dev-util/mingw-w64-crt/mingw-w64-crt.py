import info
from shells import *

class subinfo( info.infoclass ):
    def setTargets( self ):
        self.svnTargets['gitHEAD'] = 'git://git.code.sf.net/p/mingw-w64/mingw-w64'
        self.defaultTarget = 'gitHEAD'

    def setDependencies( self ):
        self.buildDependencies['dev-util/msys'] = 'default'
        self.dependencies['dev-util/mingw-w64-headers'] = 'default'


from Package.AutoToolsPackageBase import *

class Package( AutoToolsPackageBase ):
    def __init__( self ):
        AutoToolsPackageBase.__init__( self )
        self.supportsCCACHE = False
        if compiler.isX64():
            disable = "--disable-lib32 --enable-lib64"
            self.subinfo.options.merge.destinationPath = 'mingw64/x86_64-w64-mingw32'
        else:
            disable = "--disable-lib64 --enable-lib32"
            self.subinfo.options.merge.destinationPath = 'mingw/i686-w64-mingw32'
        self.subinfo.options.configure.defines = " --with-sysroot=%s --enable-wildcard --without-headers  %s  " % (self.shell.toNativePath(self.mergeDestinationDir()),disable)


