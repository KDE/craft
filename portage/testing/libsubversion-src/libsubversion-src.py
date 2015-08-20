import os

import info


class subinfo(info.infoclass):
    def setTargets( self ):
        baseUrl = "http://mirror.netcologne.de/apache.org/subversion/"
        self.targets['1.8.14'] = baseUrl + "subversion-1.8.14.tar.gz"
        self.targetDigests['1.8.14'] = 'cf29fd809927727300a083f7d14028b52258a190'
        self.defaultTarget = '1.8.14'

    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'
        self.buildDependencies['win32libs/sqlite'] = 'default'
        self.dependencies['testing/apr-src'] = 'default'
        self.dependencies['win32libs/openssl'] = 'default'

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self, **args ):
        CMakePackageBase.__init__(self)

    def configure( self ):
        self.enterSourceDir()
        os.chdir("subversion-1.8.14")

        self.apr = portage.getPackageInstance('testing', 'apr-src')
        self.openssl = portage.getPackageInstance('win32libs', 'openssl')
        self.sqlite = portage.getPackageInstance('win32libs', 'sqlite')

        includeDir = os.path.join(EmergeStandardDirs.emergeRoot(), "include")

        pythonPath = emergeSettings.get("Paths","PYTHON27")
        python = os.path.join(emergeSettings.get("Paths","PYTHON27"), "python")
        cmd = python
        cmd += " gen-make.py -t vcproj"
#        if compiler.isMSVC():          # doesn't work for 2k10
#            cmd += " --vsnet-version=" + compiler.getCompilerName()[-4:]
        cmd += " --vsnet-version=2008"
        for aprpac in ['apr', 'apr-iconv', 'apr-util']:
            cmd += " --with-" + aprpac + "=" + os.path.join( self.apr.sourceDir(), aprpac )
        cmd += " --with-openssl=" + self.openssl.buildDir()
        cmd += " --with-sqlite=" + self.sqlite.sourceDir()
        cmd += " --with-zlib=" + includeDir
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
        os.chdir("subversion-1.8.14")

        print(libs.split())
        cmd = "msbuild /m /p:Platform=Win32 /target:Libraries\\" + ":rebuild,Libraries\\".join(libs.split()) + ":rebuild subversion_vcnet.sln"
        print(cmd)
        return self.system( cmd )

    def install(self):
        sourceDir = os.path.join(self.sourceDir(), "subversion-1.8.14")
        imageDir = self.imageDir()

        utils.copyDir(os.path.join(sourceDir, "subversion", "include"), os.path.join(imageDir, "include", "subversion-1"))

        # copy libs
        libdir = os.path.join(sourceDir, "Debug", "subversion")
        for dirpath, dirnames, filenames in os.walk(libdir):
            for filename in filenames:
                if filename.endswith(".lib") or filename.endswith(".pdb"):
                    utils.copyFile(os.path.join(dirpath, filename), os.path.join(imageDir, "lib", filename))

        return True
