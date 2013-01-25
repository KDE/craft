import utils
import os
import info
import emergePlatform
import compiler

class subinfo( info.infoclass ):
    def setTargets( self ):
        for ver in ['2.4.28', '2.4.33']:
            self.targets[ ver ] = ('ftp://ftp.openldap.org/pub/OpenLDAP/'
                                   'openldap-release/openldap-' + ver + '.tgz')
            self.targetInstSrc[ ver ] = 'openldap-' + ver
        self.patchToApply['2.4.28'] = [('openldap-2.4.28-20120212.diff', 1)]
        self.patchToApply['2.4.33'] = [('openldap-2.4.33-20130124.diff', 1)]
        self.targetDigests['2.4.28'] = 'd888beae1723002a5a2ff5509d3040df40885774'
        self.targetDigests['2.4.33'] = '0cea642ba2dae1eb719da41bfedb9eba72ad504d'
        self.shortDescription = "an open source implementation of the Lightweight Directory Access Protocol"
        self.defaultTarget = '2.4.33'

    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'
        self.dependencies[ 'win32libs/cyrus-sasl' ] = 'default'
        self.dependencies[ 'win32libs/pcre' ] = 'default'
        self.dependencies[ 'win32libs/openssl' ] = 'default'

from Package.CMakePackageBase import *

class Package( CMakePackageBase ):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )
#        self.subinfo.options.configure.defines = "-DBUILD_TOOL=ON -DBUILD_TESTS=ON "


if __name__ == '__main__':
    Package().execute()
