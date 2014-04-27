import info


class subinfo(info.infoclass):
    def setTargets( self ):
        for ver in ['1.9', '1.10', '1.12']:
            self.targets[ver] = 'ftp://ftp.gnupg.org/gcrypt/libgpg-error/libgpg-error-' + ver + '.tar.bz2'
            self.targetInstSrc[ver] = 'libgpg-error-' + ver
        self.patchToApply['1.9'] = ('libgpg-error-1.9-20100801.diff', 1)
        self.patchToApply['1.10'] = [('libgpg-error-cmake.diff', 1), ('wince-fixes.diff', 0), ('libgpg-error-1.10-20101031.diff', 1)]
        self.targetDigests['1.9'] = '6836579e42320b057a2372bbcd0325130fe2561e'
        self.targetDigests['1.10'] = '95b324359627fbcb762487ab6091afbe59823b29'
        self.targetDigests['1.12'] = '259f359cd1440b21840c3a78e852afd549c709b8'
        self.patchToApply['1.12'] = [('libgpg-error-r267-20101205.diff', 1),
                                     ('libgpg-error-cmake-1.12.diff', 1)]
        # NOTE: the libgpg-error-cmake*.diff file contains the package number
        # in ConfigureChecks.cmake and must thus be changed with every version change!

        self.targets['267'] = "http://download.sourceforge.net/kde-windows/libgpg-error-r267.tar.bz2"
        self.targetInstSrc['267'] = "libgpg-error-r267"
        self.targetDigests['267'] = '001d8ec3b2b922664a0730e9dddac87f03c23f5f'
        self.patchToApply['267'] = [('libgpg-error-r267-20101205.diff', 1),
                                    ('libgpg-error-cmake.diff', 1)]

        self.shortDescription = "Small library with error codes and descriptions shared by most GnuPG related software"
        self.defaultTarget = '1.12'

    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'
        self.buildDependencies['gnuwin32/grep'] = 'default'
        self.buildDependencies['gnuwin32/gawk'] = 'default'

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self, **args ):
        CMakePackageBase.__init__( self )
        self.subinfo.options.configure.defines = "-DBUILD_TOOL=ON -DBUILD_TESTS=ON "


