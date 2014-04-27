import info

class subinfo( info.infoclass ):
    def setTargets( self ):
        self.svnTargets['gitHEAD'] = '[git]kde:libkgapi'
        self.svnTargets['0.4'] = '[git]kde:libkgapi|LibKGAPI/0.4|'
        
        self.targets[ '0.4.4'] = "http://download.kde.org/stable/libkgapi/0.4.4/src/libkgapi-0.4.4.tar.bz2"
        self.targetInstSrc[ '0.4.4' ] = "libkgapi-0.4.4"
        self.patchToApply[ '0.4.4' ] = [("libkgapi-0.4.4-20130306.diff", 1)]
        
        for ver in ['2.0.2']:
            self.targets[ ver ] = "http://download.kde.org/stable/libkgapi/" + ver + "/src/libkgapi-" + ver + ".tar.xz"
            self.targetInstSrc[ ver ] = "libkgapi-" + ver
            # TODO: check whether really needed (builds without the patch):
            self.patchToApply[ ver ] = [("libkgapi-2.0.2-20131209.diff", 1)]

        self.targetDigests['0.4.4'] = 'bccc767ec189d44912744e2b4c59c2d960c334c6'
        self.targetDigests['2.0.2'] = 'e856381f82741ee58f068070478eb4783704ebcb'
        
        self.defaultTarget = '2.0.2'

    def setDependencies( self ):
        self.dependencies['kde/kdepimlibs'] = 'default'
        self.shortDescription = "KDE library for Google API"

from Package.CMakePackageBase import *

class Package( CMakePackageBase ):
    def __init__( self ):
        CMakePackageBase.__init__( self )

