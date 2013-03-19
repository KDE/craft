import info

class subinfo( info.infoclass ):
    def setTargets( self ):
        self.svnTargets['gitHEAD'] = '[git]kde:libkgapi'
        self.svnTargets['0.4'] = '[git]kde:libkgapi|LibKGAPI/0.4|'
        for ver in ['0.4.4']:
            self.targets[ ver ] = "http://download.kde.org/stable/libkgapi/" + ver + "/src/libkgapi-" + ver + ".tar.bz2"
            self.targetInstSrc[ ver ] = "libkgapi-" + ver
        self.targetDigests['0.4.4'] = 'bccc767ec189d44912744e2b4c59c2d960c334c6'
        self.patchToApply['0.4.4'] = [("libkgapi-0.4.4-20130306.diff", 1)]
        self.defaultTarget = '0.4.4'

    def setDependencies( self ):
        self.dependencies['kde/kdepimlibs'] = 'default'
        self.shortDescription = "KDE library for Google API"

from Package.CMakePackageBase import *

class Package( CMakePackageBase ):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )

if __name__ == '__main__':
    Package().execute()
