import info


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ['2.0.0']:
            self.targets[ver] = f'https://github.com/libical/libical/archive/v{ver}.tar.gz'
            self.targetInstSrc[ver] = f'libical-{ver}'
            self.archiveNames[ver] = f'libical-{ver}.tar.gz'

        self.patchToApply['2.0.0'] = [('001-libical-2.0.0-search-snprintf.diff', 1)]
        self.targetDigests['2.0.0'] = (
            ['20f4a98475052e1200d2691ba50b27969e4bedc6e50bffd5e2fa81f4ac90de9a'], CraftHash.HashAlgorithm.SHA256)

        self.description = "Reference implementation of the icalendar data type and serialization format"
        self.defaultTarget = '2.0.0'

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = "default"


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self, **args):
        CMakePackageBase.__init__(self)
        self.subinfo.options.configure.args = " -DUSE_BUILTIN_TZDATA=true -DICAL_UNIX_NEWLINE=false "
