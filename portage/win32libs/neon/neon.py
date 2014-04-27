import info

class subinfo(info.infoclass):
    def setTargets( self ):
        for ver in [ '0.29.6', '0.30.0' ]:
            self.targets[ver] = 'http://www.webdav.org/neon/neon-' + ver + '.tar.gz'
            self.targetInstSrc[ver] = 'neon-' + ver
        self.targetDigests['0.29.6'] = 'ae1109923303f67ed3421157927bc4bc29c58961'
        self.patchToApply['0.29.6'] = [('neon-cmake.diff', 1)]
        self.targetDigests['0.30.0'] = '9e6297945226f90d66258b7ee05f757ff5cea10a'
        self.patchToApply['0.30.0'] = [('neon-0.30.0-cmake.diff', 1)]

        self.shortDescription = "an HTTP and WebDAV client library, with a C interface"
        self.defaultTarget = '0.30.0'

    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__(self, **args):
        CMakePackageBase.__init__(self)

        # do not install docs
        self.subinfo.options.configure.defines = "-DINSTALL_DOCS=OFF"

