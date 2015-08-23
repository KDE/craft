# -*- coding: utf-8 -*-
import info
from Package.VirtualPackageBase import *
from Packager.NullsoftInstallerPackager import *

import os

# This is an example package for building

class subinfo( info.infoclass ):
    def setTargets( self ):
        self.svnTargets[ '5.0.0' ] = ""
        self.defaultTarget = '5.0.0'

    def setDependencies( self ):
        self.dependencies[ 'kde/breeze' ] = 'default'
        self.dependencies[ 'kde/oxygen-icons' ] = 'default'
        self.dependencies[ 'extragear/kdevelop' ] = 'default'
        self.dependencies[ 'libs/runtime' ] = 'default'

class Package( NullsoftInstallerPackager, VirtualPackageBase ):
    def __init__( self, **args ):
#        whitelists = [ 'whitelist.txt' ]
        blacklists = [ NSIPackagerLists.runtimeBlacklist, 'blacklist.txt', 'blacklist-mysql.txt', 'blacklist-virtuoso.txt' ]
        NullsoftInstallerPackager.__init__( self, blacklists=blacklists )
        VirtualPackageBase.__init__( self )
        self.scriptname = os.path.join( os.path.dirname( __file__ ), "kdevelop.nsi" )
        self.defines[ "productname" ] = "KDevelop"
        self.defines[ "executable" ] = "bin\\kdevelop.exe"

    def preArchive(self):
        # TODO: Why is that needed?
        os.mkdir(os.path.join(self.imageDir(), "etc", "dbus-1", "session.d"))

        # TODO: Can we generalize this for other apps?
        # move all plugins to the default plugins path
        binPath = os.path.join(self.imageDir(), "bin")
        pluginsPaths = [
            os.path.join(self.imageDir(), "plugins"),
            os.path.join(self.imageDir(), "lib", "plugins")
        ]
        for pluginsPath in pluginsPaths:
            for filename in os.listdir(pluginsPath):
                src = os.path.join(pluginsPath, filename)
                utils.moveFile(src, binPath)

            os.rmdir(pluginsPath)
