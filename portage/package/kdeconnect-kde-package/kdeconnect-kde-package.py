# -*- coding: utf-8 -*-
import info
from Package.VirtualPackageBase import *
from Packager.PortablePackager import *

class subinfo( info.infoclass ):
    def setTargets( self ):
        for pack in installdb.getInstalledPackages('qt-apps','kdeconnect-kde'):
            version = pack.getVersion()
            if version:
                self.targets[ version ] = ""
                self.defaultTarget = version
            gitVersion = pack.getRevision()
            if gitVersion:
                self.svnTargets[ gitVersion  ] = ""
                self.defaultTarget = gitVersion


    def setDependencies( self ):
        self.dependencies[ 'qt-apps/kdeconnect-kde' ] = 'default'
        self.dependencies[ 'kde/kde-cli-tools' ] = 'default'

class Package( PortablePackager, VirtualPackageBase ):
    def __init__( self, **args ):
        whitelists = [ 'whitelist.txt' ]
        blacklists = [ 'blacklist.txt']
        PortablePackager.__init__( self, whitelists, blacklists )
        VirtualPackageBase.__init__( self )

