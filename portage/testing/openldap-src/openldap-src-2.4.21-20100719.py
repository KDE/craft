# OpenLDAP source package for MinGW builds
#
# This package provides the OpenLDAP libraries.
# Building of the OpenLDAP server is disabled.

# TODO: (for integration into win32libs-sources)
#      Provide a bin package for MSVC

import base
import os
import shutil
import utils
import info
import emergePlatform
import compiler
from Package.PackageBase import *
from Source.MultiSource import *
from BuildSystem.AutoToolsBuildSystem import *
from Packager.KDEWinPackager import *;

class subinfo(info.infoclass):
    def setTargets( self ):
        for ver in [ '2.4.23' , '2.4.21']:
            self.targets[ver] = 'ftp://ftp.openldap.org/pub/OpenLDAP/openldap-release/openldap-' +\
                                 ver + '.tgz'
            self.targetInstSrc[ver] = 'openldap-' + ver
            self.targetDigestUrls[ver] = 'ftp://ftp.openldap.org/pub/OpenLDAP/openldap-release/' +\
                                         'openldap-'+ver+'.sha1'
            self.defaultTarget = '2.4.21'

    def setDependencies( self ):
        self.hardDependencies['virtual/base'] = 'default'
        self.hardDependencies['dev-util/msys'] = 'default'
        self.hardDependencies['testing/regex'] = 'default'
        self.hardDependencies['win32libs-bin/gettext'] = 'default'


    def setBuildOptions( self ):
        self.disableHostBuild = False
        self.disableTargetBuild = True

class PackageMSys(PackageBase, MultiSource, AutoToolsBuildSystem, KDEWinPackager):
    def __init__( self ):
        self.subinfo = subinfo()
        PackageBase.__init__(self)
        MultiSource.__init__(self)
        AutoToolsBuildSystem.__init__(self)
        KDEWinPackager.__init__(self)
        self.subinfo.options.package.packageName = 'openldap'
        self.subinfo.options.package.withCompiler = False
        self.subinfo.options.package.packSources = True
        self.subinfo.options.install.useDestDir = False
        self.shell = MSysShell()

        self.buildInSource=True

        # Only build the client and libraries and not the OpenLDAP server
        self.subinfo.options.configure.defines = "--disable-slapd --with-cyrus_sasl=no"

    def install (self):
        self.enterSourceDir()
        self.shell.execute(self.sourceDir(), self.makeProgram, "install" )
        return True

class Package(PackageMSys):
    def __init__( self ):
        PackageMSys.__init__( self )

if __name__ == '__main__':
      Package().execute()
