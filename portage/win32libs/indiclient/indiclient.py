import info

class subinfo( info.infoclass ):
    def setTargets( self ):
        self.svnTargets['gitHEAD'] = "https://github.com/indilib/indi.git"
        self.shortDescription = 'INDI Library'
        self.defaultTarget = 'gitHEAD'
        self.targetInstSrc['gitHEAD'] = "libindi"

    def setDependencies( self ):
        self.buildDependencies['virtual/base']  = 'default'
        self.dependencies['libs/qtbase'] = 'default'
        self.dependencies['win32libs/libnova'] = 'default'

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self ):
        CMakePackageBase.__init__(self)
        self.subinfo.options.configure.defines = "-DENABLE_STATIC=ON"
