import info
from Package.MakeFilePackageBase import *

class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets["master"] = "https://github.com/auriamg/macdylibbundler.git"
        self.targetInstallPath["master"] = "dev-utils"
        self.description = "Utility to ease bundling libraries into executables for OSX"
        self.webpage = "https://github.com/auriamg/macdylibbundler/"
        self.defaultTarget = 'master'

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = "default"

class Package(MakeFilePackageBase):
    def __init__(self, **args):
        MakeFilePackageBase.__init__(self)
        self.subinfo.options.useShadowBuild = False
