import info


class subinfo(info.infoclass):
    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = "default"
        self.runtimeDependencies["win32libs/zlib"] = "default"
        self.descriptions = "audio meta-data library"

    def setTargets(self):
        self.targets["1.9.1"] = 'https://taglib.github.io/releases/taglib-1.9.1.tar.gz'
        self.targetInstSrc["1.9.1"] = 'taglib-1.9.1'
        self.targetDigests['1.9.1'] = '4fa426c453297e62c1d1eff64a46e76ed8bebb45'
        self.svnTargets['svnHEAD'] = 'trunk/kdesupport/taglib'
        self.description = "audio metadata library"
        self.defaultTarget = '1.9.1'


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
        self.subinfo.options.configure.args = ""
        #        self.subinfo.options.configure.args += " -DBUILD_TESTS=ON"
        #        self.subinfo.options.configure.args += " -DBUILD_EXAMPLES=ON"
        #        self.subinfo.options.configure.args += " -DNO_ITUNES_HACKS=ON"
        self.subinfo.options.configure.args += " -DWITH_ASF=ON"
        self.subinfo.options.configure.args += " -DWITH_MP4=ON"
