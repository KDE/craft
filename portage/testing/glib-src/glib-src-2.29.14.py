# This package is in testing for a good reason it installs
# several things into your emerge root directory which will
# include openssl for example and can break your builds!

from Package.CMakePackageBase import *
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets["2.29.14"] = "http://ftp.acc.umu.se/pub/GNOME/sources/glib/2.29/glib-2.29.14.tar.bz2"
        self.targetInstSrc["2.29.14"] = "glib-2.29.14"
        self.patchToApply["2.29.14"] = ('glib-2.29.14-20110723.diff', '1')
        self.targetDigests['2.29.14'] = 'bd993994e9d6262c19d241f6a6f781f11b840831'
        self.shortDescription = "some of the glib libraries"
        self.defaultTarget = "2.29.14"

    def setDependencies( self ):
        self.buildDependencies['virtual/bin-base'] = 'default'
        self.dependencies['testing/libffi-src'] = 'default'


class Package(CMakePackageBase):
    def __init__(self):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )

    def configure( self ):
        return True

    def make( self ):
        return True

    def compile( self ):
        self.enterSourceDir()
        cmd = "msbuild build\\win32\\vs10\\glib.sln"
        return self.system( cmd )

    def install( self ):
        self.enterSourceDir()
        os.putenv("INSTALLDIR", self.imageDir() )
        print self.imageDir()
        cmd = "msbuild /target:install build\\win32\\vs10\\glib.sln"
        return self.system( cmd )

if __name__ == '__main__':
    Package().execute()
