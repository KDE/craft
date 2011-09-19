import info
import os

class subinfo( info.infoclass ):
    def setTargets( self ):
        self.svnTargets[ 'svnHEAD' ] = 'svn://svn.gna.org/svn/kbibtex/trunk'
        for ver in ['0.4-beta1']:
            self.targets[ ver ] = 'http://download.gna.org/kbibtex/0.4/kbibtex-' + ver + '.tar.bz2'
            self.targetInstSrc[ ver ] = 'kbibtex-' + ver

        self.shortDescription = "a BibTeX editor to edit bibliographies used with LaTeX"
        self.defaultTarget = 'svnHEAD'

    def setDependencies( self ):
        self.runtimeDependencies[ 'kde/kde-runtime' ] = 'default'
        self.dependencies[ 'kde/kdelibs' ] = 'default'
        self.dependencies[ 'kdesupport/poppler' ] = 'default'
        self.dependencies[ 'win32libs-bin/libxslt' ] = 'default'

from Package.CMakePackageBase import *

class Package( CMakePackageBase ):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )

if __name__ == '__main__':
    Package().execute()

