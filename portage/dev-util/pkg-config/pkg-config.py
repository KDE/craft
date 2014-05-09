from Package.BinaryPackageBase import *
import info


class subinfo( info.infoclass ):
    def setTargets( self ):
        self.targets[ "0.28" ] = "http://downloads.sourceforge.net/msys2/mingw-w64-i686-pkgconf-0.9.5-1-any.pkg.tar.xz"
        self.targetDigests[ "0.28" ] = "8fe89c3ac4217beffbb942a2e9da3597d30226e8"
        self.targetInstSrc[ "0.28" ] = "mingw32"
        self.defaultTarget = "0.28"

    def setDependencies( self ):
        self.dependencies[ 'virtual/bin-base' ] = 'default'


class Package( BinaryPackageBase ):
    def __init__( self ):
        BinaryPackageBase.__init__( self )
        self.subinfo.options.merge.destinationPath = 'dev-utils'

