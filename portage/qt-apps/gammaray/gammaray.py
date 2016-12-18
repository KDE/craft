import info

class subinfo( info.infoclass ):
    def setTargets( self ):
        self.svnTargets["gitHEAD"] = "[git]https://github.com/KDAB/GammaRay.git"
        for ver in ["2.6.0"]:
            self.targets[ver] = "https://github.com/KDAB/GammaRay/archive/v%s.tar.gz" % ver
            self.targetInstSrc[ver] = "gammaray-%s" % ver
            self.archiveNames[ver] = "gammaray-%s.tar.gz" % ver
        self.targetDigests['2.6.0'] = (['762fc1e61fb141462e72fe048b4a7bbf1063eea6a2209963c8aa1ad7696b0217'], CraftHash.HashAlgorithm.SHA256)

        self.shortDescription = "GammaRay is a tool to poke around in a Qt-application and also to manipulate the application to some extent"

        self.defaultTarget = "2.6.0"

    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'
        self.dependencies["libs/qtbase"] = "default"
        self.dependencies['qt-apps/kdstatemachineeditor'] = 'default'
        self.dependencies['win32libs/openssl'] = 'default'

from Package.CMakePackageBase import *

class Package( CMakePackageBase ):
    def __init__( self ):
        CMakePackageBase.__init__( self )
        self.changePackager(NullsoftInstallerPackager)


    def createPackage(self):
        self.defines["productname"] = "GammaRay"
        self.defines["website"] = "http://www.kdab.com/gammaray"
        self.defines["executable"] = "bin\\gammaray.exe"
#            self.defines["icon"] = os.path.join(os.path.dirname(__file__), "kdevelop.ico")
        if craftSettings.getboolean("QtSDK", "Enabled", False):
            self.defines["defaultinstdir"] = os.path.join(craftSettings.get("QtSDK", "Path"),
                                                          craftSettings.get("QtSDK", "Version"),
                                                          craftSettings.get("QtSDK", "Compiler"))

        self.ignoredPackages.append("binary/mysql-pkg")

        return TypePackager.createPackage(self)


