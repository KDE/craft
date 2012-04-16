import os
import info

class subinfo( info.infoclass ):
    def setTargets( self ):
        for ver in ['4.8.0', '4.8.1', '4.8.2']:
          self.targets[ ver] = ''

        self.defaultTarget = '4.8.2'

    def setDependencies( self ):
        self.dependencies['kde/kde4-l10n-ru'] = 'default'


from Package.VirtualPackageBase import *
from Packager.NullsoftInstallerPackager import *
class Package( NullsoftInstallerPackager, VirtualPackageBase ):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        NullsoftInstallerPackager.__init__( self )
        VirtualPackageBase.__init__( self )


if __name__ == '__main__':
    Package().execute()
