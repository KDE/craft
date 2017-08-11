import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets["master"] = 'https://github.com/zaphoyd/websocketpp.git'

        self.description = 'WebSocket++ is a header only C++ library that implements RFC6455 The WebSocket Protocol'
        self.defaultTarget = 'master'

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = "default"


class Package(CMakePackageBase):
    def __init__(self, **args):
        CMakePackageBase.__init__(self)
