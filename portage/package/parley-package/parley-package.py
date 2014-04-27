# -*- coding: utf-8 -*-
import info
from Package.VirtualPackageBase import *
from Packager.MSInstallerPackager import *

# This is an example package for building a kdeedu application

class subinfo( info.infoclass ):
    def setTargets( self ):
        self.svnTargets[ '4.6' ] = ""
        self.defaultTarget = '4.6'

    def setDependencies( self ):
        self.dependencies[ 'kde/parley' ] = 'default'

class Package( MSInstallerPackager, VirtualPackageBase ):
    def __init__( self, **args ):
#        whitelists = [ 'whitelist.txt' ]
        blacklists = [ PackagerLists.runtimeBlacklist, 'blacklist.txt', 'blacklist-mysql.txt', 'blacklist-virtuoso.txt' ]
        MSInstallerPackager.__init__( self, blacklists=blacklists )
        VirtualPackageBase.__init__( self )
        self.defines[ "executable" ] = "bin\\parley.exe"

