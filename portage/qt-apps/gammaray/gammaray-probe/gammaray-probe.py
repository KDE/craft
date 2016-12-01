import info

class subinfo( info.infoclass ):
    def setTargets( self ):
        self.versionInfo.setDefaultValues()
        self.shortDescription = "GammaRayProbe is only the probe for GammaRay"

    def setDependencies(self):
        self.buildDependencies['virtual/base'] = 'default'
        self.dependencies["libs/qtbase"] = "default"

from Package.CMakePackageBase import *

class Package( CMakePackageBase ):
    def __init__( self ):
        CMakePackageBase.__init__( self )
        self.subinfo.options.configure.defines = "-DGAMMARAY_PROBE_ONLY_BUILD=ON"

