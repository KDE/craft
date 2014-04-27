import os

import info


class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['1.6.16'] = "http://subversion.tigris.org/downloads/subversion-1.6.16.zip "\
                                 "http://subversion.tigris.org/downloads/subversion-deps-1.6.16.zip"
#        self.targetDigests['1.6.16'] = 'c4be34aaa3bddd8740b6ff692b864dd913e9951a'
        self.defaultTarget = '1.6.16'

    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'
        self.dependencies['testing/apr-src'] = 'default'
        self.dependencies['win32libs/openssl'] = 'default'

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self, **args ):
        CMakePackageBase.__init__(self)

    def configure( self ):
        self.enterSourceDir()
        os.chdir("subversion-1.6.16")

        self.apr = portage.getPackageInstance('testing', 'apr')
        self.openssl = portage.getPackageInstance('win32libs', 'openssl')
        cmd = "python gen-make.py -t vcproj"
#        if compiler.isMSVC():          # doesn't work for 2k10
#            cmd += " --vsnet-version=" + compiler.getCompilerName()[-4:]
        cmd += " --vsnet-version=2008"
        for aprpac in ['apr', 'apr-iconv', 'apr-util']:
            cmd += " --with-" + aprpac + "=" + os.path.join( self.apr.sourceDir(), aprpac )
        cmd += " --without-neon"
        cmd += " --with-openssl=" + self.openssl.buildDir()
        return self.system( cmd )

    def make( self ):
        libs = """
        libsvn_fs_fs
        libsvn_fs_util
        libsvn_ra_local
        libsvn_ra_svn
        svn_client
        svn_delta
        svn_diff
        svn_fs
        svn_ra
        svn_repos
        svn_subr
        svn_wc
        """
        self.enterSourceDir()
        os.chdir("subversion-1.6.16")
        
        print(libs.split())
        cmd = "msbuild /target:Libraries\\" + ":rebuild,Libraries\\".join(libs.split()) + ":rebuild subversion_vcnet.sln"
        print(cmd)
        return self.system( cmd )


if __name__ == '__main__':
    Package().execute()
