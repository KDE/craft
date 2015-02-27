# -*- coding: utf-8 -*-
import info
from Package.VirtualPackageBase import *
from Packager.NullsoftInstallerPackager import *

class subinfo( info.infoclass ):
    def setTargets( self ):
        self.svnTargets[ 'frameworks' ] = ""
        self.defaultTarget = 'frameworks'

    def setDependencies( self ):
        self.dependencies[ 'extragear/kmymoney' ] = 'default'
        self.dependencies[ 'libs/runtime' ] = 'default'

class Package( NullsoftInstallerPackager, VirtualPackageBase ):
    def __init__( self, **args ):
        blacklists = [ NSIPackagerLists.runtimeBlacklist]
        NullsoftInstallerPackager.__init__( self, blacklists=blacklists )
        VirtualPackageBase.__init__( self )
        self.defines[ "executable" ] = "bin\\kmymoney.exe"
        self.defines[ "productname" ] = "KMyMoney"
        self.defines[ "icon" ] = os.path.join(self.packageDir(), "kmymoney.ico")

if __name__ == '__main__':
    Package().execute()
