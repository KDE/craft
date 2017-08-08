import info


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ['1.19', '1.30']:
            self.targets[ver] = 'ftp://ftp.gnu.org/gnu/libidn/libidn-%s.tar.gz' % ver
            self.targetInstSrc[ver] = 'libidn-%s' % ver
        self.patchToApply['1.19'] = ("libidn-1.19-20101213.diff", 1)
        self.patchToApply['1.30'] = ("libidn-1.30-20150407.diff", 1)
        self.targetDigests['1.19'] = '2b6dcb500e8135a9444a250d7df76f545915f25f'
        self.targetDigests['1.30'] = '557e1e37f0978e975b21bcdc243c198cb708bb75'
        self.description = "libidn internationalized domain names library"
        self.defaultTarget = ver

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = "default"


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self, **args):
        CMakePackageBase.__init__(self)
