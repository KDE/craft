import info

class subinfo( info.infoclass ):
    def setTargets( self ):
        self.svnTargets['gitHEAD'] = '[git]kde:libkfbapi'
        
        for ver in ['1.0']:
            self.targets[ ver ] = "http://download.kde.org/stable/libkfbapi/" + ver + "/src/libkfbapi-" + ver + ".tar.bz2"
            self.targetInstSrc[ ver ] = "libkfbapi-" + ver
            self.patchToApply[ver] = [("libkfbapi-1.0-fix-build-on-msvc.diff", 1)] # TODO: commit upstream

        self.targetDigests['1.0'] = 'a04dbca49b3ade2f015ce8d32c9024a5383f4abc'
        
        self.defaultTarget = '1.0'

    def setDependencies( self ):
        self.dependencies['kde/kdepimlibs'] = 'default'
        self.dependencies['kdesupport/qjson'] = 'default'
        self.shortDescription = "KDE library for accessing Facebook services"

from Package.CMakePackageBase import *

class Package( CMakePackageBase ):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )

if __name__ == '__main__':
    Package().execute()
