import info

class subinfo( info.infoclass ):
    def setTargets( self ):
        self.svnTargets['gitHEAD'] = 'https://github.com/KDAB/KDStateMachineEditor.git'
        self.defaultTarget = 'gitHEAD'

    def setDependencies( self ):
        self.shortDescription = "The KDAB State Machine Editor Library is a framework that can be used to help develop full-featured State Machine Editing graphical user interfaces and tools."
        self.dependencies["libs/qtbase"] = "default"
        self.dependencies["libs/qtdeclarative"] = "default"
        self.buildDependencies['virtual/base'] = 'default'

from Package.CMakePackageBase import *

class Package( CMakePackageBase ):
    def __init__( self ):
        CMakePackageBase.__init__( self )
