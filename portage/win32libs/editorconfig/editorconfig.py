import info


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ['0.12.1']:
            self.targets[ver] = 'https://github.com/editorconfig/editorconfig-core-c/archive/v%s.tar.gz' % ver
            self.targetInstSrc[ver] = 'editorconfig-core-c-%s' % ver
        self.targetDigests['0.12.1'] = 'c6e91fd86f93974d88abbf1ddba080dab07ff239'

        self.description = "EditorConfig core library written in C"
        self.defaultTarget = '0.12.1'

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = "default"
        self.runtimeDependencies["win32libs/pcre"] = "default"


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self, **args):
        CMakePackageBase.__init__(self)
