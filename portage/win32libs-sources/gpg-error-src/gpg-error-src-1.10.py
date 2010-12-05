import utils
import os
import info
import emergePlatform
import compiler

class subinfo(info.infoclass):
    def setTargets( self ):
        for ver in ['1.9', '1.10']:
            self.targets[ver] = 'ftp://ftp.gnupg.org/gcrypt/libgpg-error/libgpg-error-' + ver + '.tar.bz2'
            self.targetInstSrc[ver] = 'libgpg-error-' + ver
        self.patchToApply['1.9'] = ('libgpg-error-1.9-20100801.diff', 1)
        self.patchToApply['1.10'] = [('libgpg-error-cmake.diff', 1), ('wince-fixes.diff', 0), ('libgpg-error-1.10-20101031.diff', 1)]
        self.targetDigests['1.9'] = '6836579e42320b057a2372bbcd0325130fe2561e'
        self.targetDigests['1.10'] = '95b324359627fbcb762487ab6091afbe59823b29'
        self.targets['267'] = "http://download.sourceforge.net/kde-windows/libgpg-error-r267.tar.bz2"
        self.targetInstSrc['267'] = "libgpg-error-r267"
        self.targetDigests['267'] = '001d8ec3b2b922664a0730e9dddac87f03c23f5f'
        self.patchToApply['267'] = [('libgpg-error-r267-20101205.diff', 1), ('libgpg-error-cmake.diff', 1)]
        self.shortDescription = "a small library with error codes and descriptions shared by most GnuPG related software"
        self.defaultTarget = '1.10'

    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'
        self.buildDependencies['gnuwin32/grep'] = 'default'
        self.buildDependencies['gnuwin32/gawk'] = 'default'

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )
        self.subinfo.options.configure.defines = "-DBUILD_TOOL=ON -DBUILD_TESTS=OFF "
        if emergePlatform.isCrossCompilingEnabled():
            self.subinfo.options.configure.defines += "-DTARGET_CPP:STRING=\"" + os.getenv("VCINSTALLDIR").replace("\\", "/") + "/ce/bin/x86_arm/cl.exe\" "
            if self.isTargetBuild():
                self.subinfo.options.configure.defines += "-DBUILD_CROSS_TOOLS=OFF "


if __name__ == '__main__':
    Package().execute()
