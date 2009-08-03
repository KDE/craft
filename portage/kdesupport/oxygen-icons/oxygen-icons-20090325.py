import info

class subinfo(info.infoclass):
    def setDependencies( self ):
        self.hardDependencies['virtual/base'] = 'default'

    def setTargets( self ):
        self.svnTargets['svnHEAD'] = 'trunk/kdesupport/oxygen-icons'
        for i in ['4.3.0', '4.3.1', '4.3.2', '4.3.3', '4.3.4', '4.3']:
            self.svnTargets[ i ] = 'tags/kdesupport-for-4.3/kdesupport/oxygen-icons'
            self.targetInstSrc[ i ] = "oxygen-icons"
            
        self.defaultTarget = 'svnHEAD'

from Package.CMakePackageBase import *

class Package(CMakePackageBase, KDEWinPackager):
    def __init__( self ):
        self.subinfo = subinfo()
        self.createCombinedPackage = True
        CMakePackageBase.__init__( self )

if __name__ == '__main__':
    Package().execute()
