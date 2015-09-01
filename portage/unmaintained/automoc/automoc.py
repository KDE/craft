import info

class subinfo( info.infoclass ):
    def setDependencies( self ):
        self.buildDependencies[ 'virtual/base' ] = 'default'
        self.buildDependencies[ 'dev-util/upx' ] = 'default'

    def setTargets( self ):
        self.svnTargets[ 'gitHEAD' ] = '[git]kde:automoc|no-qt|'
        for ver in ['20130507']:
            self.targets[ ver ] = "http://www.winkde.org/pub/kde/ports/win32/repository/other/automoc-" + ver + ".tar.xz"
            self.targetInstSrc[ ver ] = "automoc-" + ver
        self.defaultTarget = '20130507'


from Package.CMakePackageBase import *

class Package( CMakePackageBase ):
    def __init__( self ):
        CMakePackageBase.__init__( self )
        self.subinfo.options.package.version = "20130507"

