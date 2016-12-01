import info

class subinfo( info.infoclass ):
    def setTargets( self ):
        self.svnTargets['gitHEAD'] = 'https://github.com/KDAB/GammaRay.git'
        for ver in ["2.6.0"]:
            self.targets[ver] = 'https://github.com/KDAB/GammaRay/archive/v%s.tar.gz' % ver
            self.archiveNames[ver] = "gammaray-%s.tar.gz" % ver
            self.targetInstSrc[ver] = 'gammaray-%s' % ver
        self.targetDigests['2.6.0'] = (['762fc1e61fb141462e72fe048b4a7bbf1063eea6a2209963c8aa1ad7696b0217'], CraftHash.HashAlgorithm.SHA256)

        self.defaultTarget = '2.6.0'

        self.shortDescription = "GammaRay is a tool to poke around in a Qt-application and also to manipulate the application to some extent"

    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'
        self.dependencies["libs/qtbase"] = "default"
        self.dependencies['qt-apps/kdstatemachineeditor'] = 'default'

from Package.CMakePackageBase import *

class Package( CMakePackageBase ):
    def __init__( self ):
        CMakePackageBase.__init__( self )

