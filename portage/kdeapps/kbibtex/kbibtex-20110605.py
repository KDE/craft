import info
import os

class subinfo( info.infoclass ):
    def setTargets( self ):
        self.svnTargets[ 'svnHEAD' ] = 'svn://svn.gna.org/svn/kbibtex/trunk'
        # no "release" targets defined, yet.
        for ver in ['0.5-beta2']:
            self.targets[ver] = "http://download.gna.org/kbibtex/" + ver[:2] + "/kbibtex-" + ver + ".tar.bz2"
            self.targetInstSrc[ver] = self.package + '-' + ver
        self.targets['0.5-rc2'] = "http://download.gna.org/kbibtex/0.5/kbibtex-0.4.96.tar.xz"
        self.targetInstSrc['0.5-rc2'] = self.package + '-0.4.96'
        self.shortDescription = "a BibTeX editor for KDE"
        self.defaultTarget = 'svnHEAD'

    def setDependencies( self ):
        self.dependencies[ 'virtual/kde-runtime' ] = 'default'

from Package.CMakePackageBase import *

class Package( CMakePackageBase ):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )

if __name__ == '__main__':
    Package().execute()

