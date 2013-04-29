# -*- coding: utf-8 -*-
# This is not a portable kleopatra package but instead a binary
# that is included among others in the gpg4win installer
# Qt for example is another package in there

import info
from Package.CMakePackageBase import *

from Package.VirtualPackageBase import *
from Packager.PortablePackager import *

class subinfo( info.infoclass ):
    def setTargets( self ):
        self.svnTargets[ 'default' ] = ""
        self.defaultTarget = 'default'

    def setDependencies( self ):
        self.dependencies[ 'kde/kdepim' ] = 'default'
        self.dependencies[ 'libs/runtime' ] = 'default'
        self.dependencies[ 'kde/kde-l10n-de' ] = 'default'

from Packager.PortablePackager import *
class Package( PortablePackager, VirtualPackageBase ):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        whitelists = [ 'whitelist.txt' ]
        VirtualPackageBase.__init__( self )
        PortablePackager.__init__(self , whitelists)

if __name__ == '__main__':
    Package().execute()
