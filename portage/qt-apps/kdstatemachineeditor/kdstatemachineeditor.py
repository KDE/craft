import info

class subinfo( info.infoclass ):
    def setTargets( self ):
        self.svnTargets['master'] = 'https://github.com/KDAB/KDStateMachineEditor.git'
        for ver in ["1.2.0"]:
            self.targets[ver] = 'https://github.com/KDAB/KDStateMachineEditor/archive/v%s.tar.gz' % ver
            self.archiveNames[ver] = "kdstatemachineeditor-%s.tar.gz" % ver
            self.targetInstSrc[ver] = 'KDStateMachineEditor-%s' % ver

        self.targetDigests['1.2.0'] = (['c43b864e60c025b1d4eb03f0b3073e00ebb642aecf10dd8b5b29f4a2da2b1c07'], CraftHash.HashAlgorithm.SHA256)

        self.shortDescription = "The KDAB State Machine Editor Library is a framework that can be used to help develop full-featured State Machine Editing graphical user interfaces and tools."
        self.defaultTarget = "1.2.0"

    def setDependencies( self ):
        self.buildDependencies['frameworks/extra-cmake-modules'] = 'default'
        self.dependencies['virtual/base'] = 'default'
        self.dependencies["libs/qtdeclarative"] = "default"
        self.dependencies["libs/qtbase"] = "default"

from Package.CMakePackageBase import *

class Package( CMakePackageBase ):
    def __init__( self ):
        CMakePackageBase.__init__( self )
