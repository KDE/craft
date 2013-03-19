import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['0.29.6'] = 'http://www.webdav.org/neon/neon-0.29.6.tar.gz'
        self.patchToApply['0.29.6'] = [('neon-cmake.diff', 1)]
        self.targetInstSrc['0.29.6'] = 'neon-0.29.6'
        self.targetDigests['0.29.6'] = 'ae1109923303f67ed3421157927bc4bc29c58961'
        self.shortDescription = "an HTTP and WebDAV client library, with a C interface"
        self.defaultTarget = '0.29.6'

    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__(self, **args):
        self.subinfo = subinfo()
        CMakePackageBase.__init__(self)

        # do not install docs
        self.subinfo.options.configure.defines = "-DINSTALL_DOCS=OFF"

if __name__ == '__main__':
    Package().execute()
