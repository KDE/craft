# -*- coding: utf-8 -*-
import info
from Package.VirtualPackageBase import *
from Packager.NullsoftInstallerPackager import *

import os

class subinfo( info.infoclass ):
    def setTargets( self ):
        self.svnTargets[ '5.0.0' ] = ""
        self.defaultTarget = '5.0.0'

    def setDependencies( self ):
        self.dependencies[ 'kde/breeze' ] = 'default'
        self.dependencies[ 'kde/oxygen-icons' ] = 'default'
        self.dependencies[ 'extragear/kdevelop' ] = 'default'

class Package( NullsoftInstallerPackager, VirtualPackageBase ):
    def __init__( self, **args ):
#        whitelists = [ 'whitelist.txt' ]
        blacklists = [ NSIPackagerLists.runtimeBlacklist, 'blacklist.txt', 'blacklist-mysql.txt', 'blacklist-virtuoso.txt' ]
        NullsoftInstallerPackager.__init__( self, blacklists=blacklists )
        VirtualPackageBase.__init__( self )
        self.scriptname = os.path.join( os.path.dirname( __file__ ), "kdevelop.nsi" )
        self.defines[ "productname" ] = "KDevelop"
        self.defines[ "executable" ] = "bin\\kdevelop.exe"
        self.defines[ "vcredist" ] = "none"
        if compiler.isX64():
            self.defines[ "defaultinstdir" ] = "$PROGRAMFILES64"
            self.defines[ "vcredist" ] = "C:\\Program Files (x86)\\Microsoft Visual Studio 14.0\\VC\\redist\\1033\\vcredist_x64.exe"
        if compiler.isX86():
            self.defines[ "defaultinstdir" ] = "$PROGRAMFILES"
            self.defines[ "vcredist" ] = "C:\\Program Files (x86)\\Microsoft Visual Studio 14.0\\VC\\redist\\1033\\vcredist_x86.exe"

    def preArchive(self):
        # TODO: Why is that needed?
        os.mkdir(os.path.join(self.imageDir(), "etc", "dbus-1", "session.d"))

        # TODO: Can we generalize this for other apps?
        # move everything to the location where Qt expects it
        binPath = os.path.join(self.imageDir(), "bin")

        utils.mergeTree(os.path.join(self.imageDir(), "plugins"), binPath)
        utils.mergeTree(os.path.join(self.imageDir(), "lib", "plugins"), binPath)
        utils.mergeTree(os.path.join(self.imageDir(), "qml"), os.path.join(self.imageDir(), binPath))
        utils.mergeTree(os.path.join(self.imageDir(), "lib", "qml"), os.path.join(self.imageDir(), binPath))
        
        # TODO: Just blacklisting this doesn't work. WTF?
        utils.rmtree(os.path.join(self.imageDir(), "dev-utils"))
