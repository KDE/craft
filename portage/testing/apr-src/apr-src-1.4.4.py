import info
import compiler

class subinfo( info.infoclass ):
    def setTargets( self ):
        for ver in ['1.4.4']:
            self.targets[ ver ] = 'http://apache.mirror.digionline.de/apr/apr-' + ver + '.tar.bz2'
            self.targetInstSrc[ ver ] = 'apr-' + ver
        self.targetDigests['1.4.4'] = 'd05cd65ec169c06174ca7c8978179289777f8dae'
        self.defaultTarget = '1.4.4'

    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'

from Package.CMakePackageBase import *

class Package( CMakePackageBase ):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )

    def configure( self ):
        return True

    def make( self ):
        self.enterSourceDir()
        cfg = "Win32"
        # for x64:
        # cfg = "x64"
        if self.buildType() in ["Release", "RelWithDebInfo", "MinSizeRel"]:
            cfg += " Release"
        else:
            cfg += " Debug"

        self.system( "%s -f Makefile.win USEMAK=1 CFG=\"%s\" PREFIX=\"%s\" buildall" % ( self.makeProgramm, cfg, self.imageDir() ) )
        return True

    def install( self ):
        self.enterSourceDir()
        self.system( "%s -f Makefile.win PREFIX=%s install" % ( self.makeProgramm, self.imageDir() ) )
        return True

if __name__ == '__main__':
    Package().execute()
