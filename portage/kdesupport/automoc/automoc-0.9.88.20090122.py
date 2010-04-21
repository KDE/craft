import info

class subinfo(info.infoclass):
    def setDependencies( self ):
        self.hardDependencies['virtual/base'] = 'default'
        self.hardDependencies['libs/qt'] = 'default'

    def setTargets( self ):
        self.svnTargets['svnHEAD'] = 'trunk/kdesupport/automoc'
        self.svnTargets['0.9.83'] = 'tags/automoc4/0.9.83'
        self.svnTargets['0.9.84'] = 'tags/automoc4/0.9.84'
        self.svnTargets['0.9.87'] = 'tags/automoc4/0.9.87'
        self.svnTargets['0.9.88'] = 'tags/automoc4/0.9.88'
        for i in ['4.3.0', '4.3.1', '4.3.2', '4.3.3', '4.3.4', '4.3']:
            self.svnTargets[ i ] = 'tags/kdesupport-for-4.3/kdesupport/automoc'
        self.defaultTarget = 'svnHEAD'
        
    def setBuildOptions( self ):
        self.disableHostBuild = False
        self.disableTargetBuild = True

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )

if __name__ == '__main__':
    Package().execute()
