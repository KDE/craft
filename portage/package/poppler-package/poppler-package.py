# -*- coding: utf-8 -*-
import info
from Package.VirtualPackageBase import *
from Packager.NullsoftInstallerPackager import *

# This is an example package for building

class subinfo( info.infoclass ):
    def setTargets( self ):
        self.svnTargets[ '0.14.5' ] = ""
        self.defaultTarget = '0.14.5'

    def setDependencies( self ):
        self.dependencies[ 'qt-libs/poppler' ] = 'default'

class Package( NullsoftInstallerPackager, VirtualPackageBase ):
    def __init__( self, **args ):
        whitelists = [ 'whitelist.txt' ]
        blacklists = [ 'blacklist.txt', 'blacklist-mysql.txt' ]
        NullsoftInstallerPackager.__init__( self, whitelists, blacklists )
        VirtualPackageBase.__init__( self )

