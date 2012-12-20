# -*- coding: utf-8 -*-
import info
import compiler
from Package.VirtualPackageBase import *
from Packager.NullsoftInstallerPackager import *

# This is an example package for building

class subinfo( info.infoclass ):
    def setTargets( self ):
        self.svnTargets[ '0.14.5' ] = ""
        self.defaultTarget = '0.14.5'

    def setDependencies( self ):
        self.dependencies[ 'kdesupport/poppler' ] = 'default'
        if compiler.isMinGW_XX():
            self.dependencies[ 'dev-util/mingw-w64' ] = 'default'

class Package( NullsoftInstallerPackager, VirtualPackageBase ):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        whitelists = [ 'whitelist.txt' ]
        blacklists = [ 'blacklist.txt', 'blacklist-mysql.txt' ]
        NullsoftInstallerPackager.__init__( self, whitelists, blacklists )
        VirtualPackageBase.__init__( self )

if __name__ == '__main__':
    Package().execute()
