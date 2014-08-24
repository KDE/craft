import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['v0.48'] = 'https://github.com/libical/libical/tarball/v0.48'
        self.archiveNames['v0.48'] = 'libical-v0.48.tar.gz'
        self.targetInstSrc['v0.48'] = 'libical-libical-b80a19e'
        self.targets['v1.0.0'] = 'https://github.com/libical/libical/tarball/v1.0.0'
        self.archiveNames['v1.0.0'] = 'libical-v1.0.0.tar.gz'
        self.targetInstSrc['v1.0.0'] = 'libical-libical-866647f'

        self.svnTargets['gitHEAD'] = '[git]https://github.com/libical/libical.git'
        self.defaultTarget = 'v0.48'
        self.shortDescription = "reference implementation of the icalendar data type and serialization format"

    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'
        if emergePlatform.isCrossCompilingEnabled():
            self.dependencies['win32libs/wcecompat'] = 'default'

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )
        self.subinfo.options.configure.defines = " -DUSE_BUILTIN_TZDATA=true -DICAL_UNIX_NEWLINE=false "

        if emergePlatform.isCrossCompilingEnabled() and self.isTargetBuild():
            self.subinfo.options.configure.defines += " -DSTATIC_LIBRARY=ON "

if __name__ == '__main__':
    Package().execute()
