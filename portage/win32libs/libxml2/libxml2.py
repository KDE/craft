import info
from Package.CMakePackageBase import *

class subinfo(info.infoclass):
    def setTargets( self ):
        for ver in ['2.8.0', '2.9.4']:
            self.targets[ver] = 'ftp://xmlsoft.org/libxml2/libxml2-' + ver + '.tar.gz'
            self.targetInstSrc[ver] = 'libxml2-' + ver
        self.patchToApply['2.8.0'] = [("libxml2-2.8.0-20110105.diff", 1),
                                     ("fix-mingw-catalog.diff", 1)]
        self.targetDigests['2.8.0'] = 'a0c553bd51ba79ab6fff26dc700004c6a41f5250'
        self.shortDescription = "XML C parser and toolkit (runtime and applications)"

        self.defaultTarget = '2.9.4'

    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'
        self.dependencies['win32libs/zlib'] = 'default'
        self.dependencies['win32libs/liblzma'] = 'default'
        self.dependencies['win32libs/win_iconv'] = 'default'

class PackageCMake(CMakePackageBase):
    def __init__( self, **args ):
        CMakePackageBase.__init__( self )
        self.subinfo.options.package.packageName = 'libxml2'
        #self.subinfo.options.configure.defines = "-DBUILD_tests=OFF"


from Package.AutoToolsPackageBase import *

class PackageMSys(AutoToolsPackageBase):
    def __init__(self):
        AutoToolsPackageBase.__init__(self)
        self.subinfo.options.make.supportsMultijob = False
        self.subinfo.options.package.packageName = 'libxml2'
        self.subinfo.options.configure.defines = " --without-python"

if compiler.isMinGW():
    class Package(PackageMSys): pass
else:
    class Package(PackageCMake): pass
