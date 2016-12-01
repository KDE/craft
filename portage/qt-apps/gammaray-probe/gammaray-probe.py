import info

class subinfo( info.infoclass ):
    def setTargets( self ):
        self.shortDescription = "GammaRayProbe is only the probe for GammaRay"

from Package.CMakePackageBase import *

class Package( CMakePackageBase ):
    def __init__( self ):
        CMakePackageBase.__init__( self )
        gammaray = portage.getPackageInstance('qt-apps', 'gammaray').subinfo
        # TODO: omg
        for var in vars(gammaray):
            if var in ["parent", "_CraftBase__evilHack", "shortDescription"]:
                continue
            setattr(self.subinfo, var, getattr(gammaray, var))
        self.subinfo.options.configure += "-DGAMMARAY_PROBE_ONLY_BUILD=ON"

