import info


class subinfo( info.infoclass ):
    def setTargets( self ):
        self.targets[ '1.4.5' ] = ['http://apache.mirror.digionline.de/apr/apr-util-1.3.12.tar.bz2',
                                   'http://apache.mirror.digionline.de/apr/apr-1.4.5.tar.bz2',
                                   'http://apache.mirror.digionline.de/apr/apr-iconv-1.2.1.tar.bz2'
                                   ]
        self.targets[ '1.4.8' ] = ['http://apache.mirror.digionline.de/apr/apr-util-1.3.12.tar.bz2',
                                   'http://apache.mirror.digionline.de/apr/apr-1.4.8.tar.bz2',
                                   'http://apache.mirror.digionline.de/apr/apr-iconv-1.2.1.tar.bz2'
                                   ]
        self.targets[ '1.5.0' ] = ['http://apache.mirror.digionline.de/apr/apr-util-1.5.3.tar.bz2',
                                   'http://apache.mirror.digionline.de/apr/apr-1.5.0.tar.bz2',
                                   'http://apache.mirror.digionline.de/apr/apr-iconv-1.2.1.tar.bz2'
                                   ]
        self.targetDigests['1.4.5'] = ['4902165fc5f2f077afbcc7ddf7ebbf61556a1cda',
                                       '517de5e3cc1e3be810d9bc95508ab66bb8ebe7cb',
                                       'c4707c92472dace3d96dd9d5d161d078b9797608']
        self.targetDigests['1.5.0'] = ['de0184ee03dfdc6dec4d013970d1862251e86925',
                                       'cae122be79070645a7ab36a53148487c84ce8bf0',
                                       'c4707c92472dace3d96dd9d5d161d078b9797608']
        self.patchToApply['1.4.5'] = [('apr-iconv-1.2.1-20110521.diff', 0), ('apr-util-1.3.12-20110524.diff', 0)]
        self.patchToApply['1.4.8'] = [('apr-iconv-1.2.1-20110521.diff', 0), ('apr-util-1.3.12-20110524.diff', 0)]
        self.patchToApply['1.5.0'] = [('apr-iconv-1.2.1-20110521.diff', 0), ('apr-util-1.5.3-20131125.diff', 0)]
        self.defaultTarget = '1.5.0'
        self.options.make.supportsMultijob = False

    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'

from Package.CMakePackageBase import *

class Package( CMakePackageBase ):
    def __init__( self, **args ):
        CMakePackageBase.__init__( self )

    def unpack( self ):
        CMakePackageBase.unpack( self )
        names = ['apr-util', 'apr', 'apr-iconv']
        for i in range(3):
            src = os.path.join( self.sourceDir(), os.path.basename(self.subinfo.targetAt(i)).replace(".tar.bz2", "") )
            dst = os.path.join( self.sourceDir(), names[i] )
            shutil.move( src, dst )
        src = os.path.join( self.sourceDir(), "apr", "include", "apr.hw" )
        dst = os.path.join( self.sourceDir(), "apr", "include", "apr.h" )
        shutil.copyfile( src, dst )
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

