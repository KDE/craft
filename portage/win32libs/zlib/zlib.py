# -*- coding: utf-8 -*-
import info
from Package.CMakePackageBase import *

class subinfo(info.infoclass):
    def setTargets( self ):
        for ver in [ '1.2.5', '1.2.6', '1.2.7', '1.2.8' ]:
            self.targets[ ver ] = 'http://downloads.sourceforge.net/sourceforge/libpng/zlib-%s.tar.gz' % ver
            self.targetInstSrc[ ver ] = "zlib-" + ver
        self.patchToApply['1.2.5'] = [("zlib-1.2.5-20110629.diff", 1)]
        self.patchToApply['1.2.6'] = [("zlib-1.2.6-20120421.diff", 1)]
        self.patchToApply['1.2.7'] = [("zlib-1.2.7-20130123.diff", 1)]
        if not compiler.isMinGW():
            self.patchToApply['1.2.8'] = [("zlib-1.2.8-20130901.diff", 1)]
        self.targetDigests['1.2.5'] = '8e8b93fa5eb80df1afe5422309dca42964562d7e'
        self.targetDigests['1.2.7'] = '4aa358a95d1e5774603e6fa149c926a80df43559'
        self.targetDigests['1.2.8'] = 'a4d316c404ff54ca545ea71a27af7dbc29817088'

        self.shortDescription = 'The zlib compression and decompression library'
        self.defaultTarget = '1.2.8'

    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'

class PackageCMake(CMakePackageBase):
    def __init__( self, **args ):
        CMakePackageBase.__init__( self )


from Package.AutoToolsPackageBase import *

class PackageMSys(AutoToolsPackageBase):
    def __init__(self):
        AutoToolsPackageBase.__init__(self)
        self.subinfo.options.make.supportsMultijob = False
        self.buildInSource = True

    def configure(self):
        return "all";

    def make(self, dummyBuildType=None):
        return self.shell.execute(self.sourceDir(), self.makeProgram, "-fwin32/Makefile.gcc")

    def install(self):
        self.enterSourceDir()
        self.shell.environment[ "BINARY_PATH" ] = "%s/bin" % (self.shell.toNativePath(self.imageDir()))
        self.shell.environment[ "LIBRARY_PATH"] = "%s/lib" % (self.shell.toNativePath(self.imageDir()))
        self.shell.environment[ "INCLUDE_PATH"] = "%s/include" % (self.shell.toNativePath(self.imageDir()))
        self.shell.execute(self.sourceDir(), self.makeProgram, "install -fwin32/Makefile.gcc SHARED_MODE=1")
        utils.copyFile(os.path.join(self.imageDir(), "bin", "zlib1.dll"), os.path.join(self.imageDir(), "bin", "libz.dll"), False)
        return True

if compiler.isMinGW():
    class Package(PackageMSys): pass
else:
    class Package(PackageCMake): pass
