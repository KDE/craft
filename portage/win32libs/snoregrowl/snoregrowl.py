import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets['master'] = 'https://github.com/Snorenotify/SnoreGrowl.git'

        for ver in ['0.4.0', '0.5.0']:
            self.targets[ver] = 'https://github.com/Snorenotify/SnoreGrowl/archive/v%s.tar.gz' % ver
            self.archiveNames[ver] = "snoregrowl-%s.tar.gz" % ver
            self.targetInstSrc[ver] = 'SnoreGrowl-%s' % ver
        self.targetDigests['0.4.0'] = '16b84d2fb673438c8250cefd95f7e4c145e4cf22'
        self.targetDigests['0.5.0'] = (
            ['5180628ce1c732abfc1001db48302b0d63534a3d62dc50a4655e0b4675a918be'], CraftHash.HashAlgorithm.SHA256)

        self.description = "SnoreGrowl is a library providing Growl network notifications"
        self.webpage = "https://github.com/Snorenotify/SnoreGrowl"
        self.defaultTarget = '0.5.0'

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = "default"


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self, **args):
        CMakePackageBase.__init__(self)
        self.subinfo.options.configure.staticArgs = "-DSNOREGROWL_STATIC=ON"
