import info

class subinfo( info.infoclass ):
    def setTargets( self ):
        self.svnTargets['gitHEAD'] = 'https://github.com/KDAB/KDStateMachineEditor.git'
        for ver in ["1.1.0"]:
            self.targets[ver] = 'https://github.com/KDAB/KDStateMachineEditor/archive/v%s.tar.gz' % ver
            self.archiveNames[ver] = "kdstatemachineeditor-%s.tar.gz" % ver
            self.targetInstSrc[ver] = 'KDStateMachineEditor-%s' % ver

        self.targetDigests['1.1.0'] = (['3dcbb8925d3fc9e1ec760a486477f30856bd66e0086227dc2af0b0afac973a4a'], CraftHash.HashAlgorithm.SHA256)

        self.shortDescription = "The KDAB State Machine Editor Library is a framework that can be used to help develop full-featured State Machine Editing graphical user interfaces and tools."
        self.defaultTarget = "1.1.0"

    def setDependencies( self ):
        self.buildDependencies['frameworks/extra-cmake-modules'] = 'default'
        self.buildDependencies['virtual/base'] = 'default'
        self.dependencies["libs/qtdeclarative"] = "default"
        self.dependencies["libs/qtbase"] = "default"

from Package.CMakePackageBase import *

class Package( CMakePackageBase ):
    def __init__( self ):
        CMakePackageBase.__init__( self )
