import info


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ['2.4.28', '2.4.33', '2.4.36', '2.4.45']:
            self.targets[ver] = ('ftp://ftp.openldap.org/pub/OpenLDAP/'
                                 'openldap-release/openldap-' + ver + '.tgz')
            self.targetInstSrc[ver] = 'openldap-' + ver
        self.patchToApply['2.4.28'] = [('openldap-2.4.28-20120212.diff', 1)]
        self.patchToApply['2.4.33'] = [('openldap-2.4.33-20130124.diff', 1)]
        self.patchToApply['2.4.36'] = [('openldap-2.4.36-20131003.diff', 1)]
        # self.patchToApply['2.4.36'] = [('openldap-2.4.36-20170627.diff', 1)]
        self.patchToApply['2.4.45'] = [('openldap-2.4.45-20170628.diff', 1)]
        self.targetDigests['2.4.28'] = 'd888beae1723002a5a2ff5509d3040df40885774'
        self.targetDigests['2.4.33'] = '0cea642ba2dae1eb719da41bfedb9eba72ad504d'
        self.targetDigests['2.4.36'] = 'da0e18a28a5dade5c98d9a382fd8f0a676a12aca'

        self.description = "an open source implementation of the Lightweight Directory Access Protocol"
        self.defaultTarget = '2.4.45'

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = "default"
        self.runtimeDependencies["win32libs/cyrus-sasl"] = "default"
        self.runtimeDependencies["win32libs/pcre"] = "default"
        self.runtimeDependencies["win32libs/openssl"] = "default"


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self, **args):
        CMakePackageBase.__init__(self)

# self.subinfo.options.configure.args = "-DBUILD_TOOL=ON -DBUILD_TESTS=ON "
