import info
import compiler

class subinfo( info.infoclass ):
    def setTargets( self ):
        self.targets[ '1.4.4' ] = ['http://apache.mirror.digionline.de/apr/apr-util-1.3.11.tar.bz2',
                                   'http://apache.mirror.digionline.de/apr/apr-1.4.4.tar.bz2',
                                   'http://apache.mirror.digionline.de/apr/apr-iconv-1.2.1.tar.bz2'
                                   ]
        self.targetDigests['1.4.4'] = ['dc71af7684f76d56f06b4fc8763a8606bd861e84',
                                        'd05cd65ec169c06174ca7c8978179289777f8dae',
                                        'c4707c92472dace3d96dd9d5d161d078b9797608']
        self.patchToApply['1.4.4'] = [('apr-iconv-1.2.1-20110521.diff', 0), ('apr-util-1.3.11-20110521.diff', 0)]
        self.defaultTarget = '1.4.4'
        self.options.make.supportsMultijob = False

    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'

from Package.CMakePackageBase import *

class Package( CMakePackageBase ):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )

    def unpack( self ):
        CMakePackageBase.unpack( self )
        names = ['apr-util', 'apr', 'apr-iconv']
        for i in range(3):
            src = os.path.join( self.sourceDir(), os.path.basename(self.subinfo.targetAt(i)).replace(".tar.bz2", "") )
            dst = os.path.join( self.sourceDir(), names[i] )
            shutil.move( src, dst )
        return True

    def configure( self ):
        return True

    def _getConfig( self ):
        cfg = "Win32"
        # for x64:
        # cfg = "x64"
        if self.buildType() in ["Release", "RelWithDebInfo", "MinSizeRel"]:
            cfg += " Release"
        else:
            cfg += " Debug"
        return cfg

    def make( self ):
        self.enterSourceDir()
        os.chdir("apr-util")

        self.system( "%s -f Makefile.win USEMAK=1 ARCH=\"%s\" PREFIX=\"%s\" buildall" % ( self.makeProgramm, self._getConfig(), self.imageDir() ) )
        return True

    def install( self ):
        self.enterSourceDir()
        os.chdir("apr-util")
        self.system( "%s -f Makefile.win USEMAK=1 ARCH=\"%s\" PREFIX=%s install" % ( self.makeProgramm, self._getConfig(), self.imageDir() ) )
        return True

if __name__ == '__main__':
    Package().execute()
